import json

from pathlib2 import Path

from moana.utilities.loggingSetup import logger
from moana import constants


class MoanaJSONFile(object):
    basePath = Path(constants.BASE_DIR)
    def __init__(self, asset):
        self.asset = asset
        self.jsonPath = self.getPath()
        # Todo: Rename this function
        self.data = self.getData()


    def getPath(self):
        logger.debug('Getting JSON path for %s', self.asset)

        jsonPath = self.basePath / 'json' / self.asset / (self.asset + '.json')

        if not jsonPath.is_file():
            logger.error('Could not find %s', jsonPath)
            return

        logger.debug('JSON Path for %s is %s', self.asset, jsonPath)
        return jsonPath


    def getData(self):
        logger.debug('Getting JSON data for %s', self.asset)
        with open(unicode(self.jsonPath), 'r') as f:
            data = json.load(f)

        return data


def main():
    return MoanaJSONFile('isLavaRocks')
