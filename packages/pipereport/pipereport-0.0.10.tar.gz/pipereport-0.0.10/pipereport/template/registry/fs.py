import os

import yaml

from pipereport.base.templateregistry import BaseTemplateRegistry


class FSTemplateRegistry(BaseTemplateRegistry):

    def __init__(self, *args, path=".", **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def get_template_by_name(self, template_name: str) -> dict:
        with open(os.path.join(self.path, template_name + ".json")) as tmpl:
            template = yaml.safe_load(tmpl)
        return template
