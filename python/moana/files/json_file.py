import json

from pathlib2 import Path

from moana.utilities.logging_setup import logger
from moana import constants


class MoanaJSONFile(object):
    base_path = Path(constants.BASE_DIR)

    def __init__(self, asset):
        self.asset = asset
        self.file_name = self.get_file_name()
        self.json_path = self.get_asset_path()
        self.data = self.load_data(self.json_path)

        mat_file = self.data.get('matFile')
        if mat_file:
            self.materials_json = MoanaMaterialJSONFile(self.asset)
        else:
            self.materials_json = None

    def __repr__(self):
        return '{0} <{1}>'.format(type(self).__name__, self.json_path)

    def get_file_name(self):
        return self.asset + '.json'

    def get_asset_path(self):
        logger.debug('Getting JSON path for %s', self.asset)

        json_path = self.base_path / 'json' / self.asset / self.file_name

        if not json_path.is_file():
            logger.error('Could not find %s', json_path)
        else:
            logger.debug('JSON Path for %s is %s', self.asset, json_path)
            return json_path

    def get_project_path(self, path):
        logger.debug('Getting project path for %s', path)

        file_path = self.base_path / path

        if file_path:
            logger.error('Could not find %s', file_path)
        else:
            logger.debug('Full Path is %s', file_path)
            return file_path

    def load_data(self, path):
        logger.debug('Loading JSON data for %s from %s', self.asset, path)
        try:
            with open(unicode(path), 'r') as f:
                data = json.load(f)
        except (IOError, WindowsError):
            logger.error('Unable to load %s!', path)
            data = None

        return data

class MoanaMaterialJSONFile(MoanaJSONFile):
    def get_file_name(self):
        return 'materials.json'


def main():
    return MoanaJSONFile('isLavaRocks')
