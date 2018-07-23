import pymel.core as pm

from moana.files import jsonFile
from moana.utilities.loggingSetup import logger

reload(jsonFile)


class MayaJSONFile(jsonFile.MoanaJSONFile):
    safeTypes = ['transform', 'mesh']

    def __init__(self, asset):
        super(MayaJSONFile, self).__init__(asset)


    def loadGeometry(self):
        try:
            objPath = self.basePath / self.data['geomObjFile']
        except KeyError:
            logger.error('Could not find geomObjFile in %s data', self.asset)
            return

        if not objPath.is_file():
            logger.error('%s could not be found or is not a file.', objPath)
            return

        parent = self.createHierarhcy()

        logger.info('Loading %s', objPath)
        # Todo: Import using cmds for speed in loading objcts and filtering
        #   convert to PyMel at the group level.
        importedObjects = pm.importFile(unicode(objPath), returnNewNodes=True)
        importedObjects = self.cleanupImport(importedObjects)

        objGroup = self.regroupImport(importedObjects, parent)

        self.applyTransform(objGroup)

        self.applyInstances(objGroup)

        return objGroup


    def createHierarhcy(self):
        path = self.data['geomObjFile']
        parts = path.split('/')[:-1]
        try:
            return pm.PyNode('|'.join(parts))
        except pm.MayaNodeError:
            pass

        pastParts = []
        for name in parts:
            pastPart = '|'.join(pastParts)
            selName = '{0}|{1}'.format(pastPart, name)
            try:
                grp = pm.PyNode(selName)
            except pm.MayaNodeError:
                logger.debug('Could not find %s, creating it.', selName)
                grp = pm.group(name=name, world=True, empty=True)
                if pastPart:
                    pm.parent(grp, pm.PyNode(pastPart))

            pastParts.append(unicode(grp))

        return grp


    def cleanupImport(self, importedObjects):
        retList = []
        for obj in importedObjects:
            try:
                if obj.type() in self.safeTypes:
                    retList.append(obj)
                else:
                    pm.delete(obj)
            except pm.MayaNodeError:
                pass

        return retList


    def regroupImport(self, importedObjects, parent):
        groupObjs = [x for x in importedObjects if x.type() == 'transform']
        topLevelGrp = pm.group(groupObjs, world=True, name=self.data['name'])
        pm.parent(topLevelGrp, parent)
        return topLevelGrp


    def applyTransform(self, transform, matrix=None):
        if not matrix:
            transform.setMatrix(self.data['transformMatrix'])
        else:
            transform.setMatrix(matrix)


    def applyInstances(self, master):
        try:
            self.data['instancedCopies']
        except KeyError:
            return

        for instance in self.data['instancedCopies']:
            instanceObj = pm.instance(master, name=self.data['instancedCopies'][instance]['name'])[0]
            self.applyTransform(instanceObj, self.data['instancedCopies'][instance]['transformMatrix'])


def main():
    x = MayaJSONFile('isBayCedarA1')
    y = x.loadGeometry()
    return y
