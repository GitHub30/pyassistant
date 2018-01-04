import os
import json
import logging
import traceback
logger = logging.getLogger('pi-assistant')

class Assistant():

    def __init__(self):
        self.home = os.environ['HOME']

    def __enter__(self):
        self.config_dir = os.path.join(self.home, '.pi-assistant')
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        self.setting_file = os.path.join(self.config_dir, 'setting.json')
        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'r') as f:
                self.setting = json.load(f)
        else:
            self.setting = {
            }

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.error(exc_type)
        logger.error(exc_val)
        traceback.print_tb(exc_tb)
        with open(self.setting_file, 'w') as f:
            json.dump(self.setting,f)

        return True