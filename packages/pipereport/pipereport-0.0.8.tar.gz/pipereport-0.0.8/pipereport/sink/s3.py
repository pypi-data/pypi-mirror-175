import os
import tempfile
from typing import Iterator, List, Optional, Tuple

import boto3

from pipereport.base.sink import BaseSink


class S3Sink(BaseSink):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        client_args = {"service_name": "s3"}
        endpoint_url = kwargs.pop("endpoint_url", None)
        if endpoint_url is not None:
            client_args["endpoint_url"] = endpoint_url
        client_args["aws_access_key_id"] = self.required_credential("aws_access_key_id")
        client_args["aws_secret_access_key"] = self.required_credential(
            "aws_secret_access_key"
        )
        self.client_args = client_args

        self.bucket = self.required_field("bucket")

        self.session = None
        self.s3 = None

    def connect(self):
        self.session = boto3.session.Session()
        self.s3 = self.session.client(**self.client_args)

    def write_block(
        self,
        source_iterator: Iterator[Tuple],
        object_id: str,
        blocksize: int = -1,
        columns: Optional[List[str]] = None,
        sep: str = "\t",
    ):
        self.telemetry.add_object(object_id, columns)
        with tempfile.TemporaryDirectory() as tmpdirname:
            cachefile = os.path.join(tmpdirname, object_id)
            with open(cachefile, "w") as cache:
                block_written = 0
                for entry in source_iterator:
                    cache.write(sep.join(entry) + "\n")
                    block_written += 1
                    if block_written == blocksize:
                        break
                self.telemetry.add_entries(object_id, block_written)
            self.s3.upload_file(cachefile, self.bucket, object_id)
