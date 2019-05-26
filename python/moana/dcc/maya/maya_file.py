import pymel.core as pm

from moana.files import json_file
from moana.utilities.logging_setup import logger

reload(json_file)


class MoanaMayaFile(json_file.MoanaJSONFile):
    safe_types = ['transform', 'mesh']

    def load_geometry(self, apply_transform=True,
                            apply_instances=True,
                            apply_materials=True):
        try:
            obj_path = self.base_path / self.data['geomObjFile']
        except KeyError:
            logger.error('Could not find geomObjFile in %s data', self.asset)
            return

        if not obj_path.is_file():
            logger.error('%s could not be found or is not a file.', obj_path)
            return

        parent = self.create_hierarhcy()

        logger.info('Loading %s', obj_path)
        # Todo: Import using cmds for speed in loading objcts and filtering
        #   convert to PyMel at the group level.
        imported_objects = pm.importFile(unicode(obj_path), returnNewNodes=True)
        imported_objects = self.cleanup_import(imported_objects)

        object_group = self.regroup_import(imported_objects, parent)

        if apply_transform:
            self.apply_transform(object_group)

        if apply_instances:
            self.apply_instances(object_group)

        if apply_materials:
            self.apply_materials(object_group)

        return object_group

    def create_hierarhcy(self):
        path = self.data['geomObjFile']
        parts = path.split('/')[:-1]
        try:
            return pm.PyNode('|'.join(parts))
        except pm.MayaNodeError:
            pass

        past_parts = []
        for name in parts:
            pastPart = '|'.join(past_parts)
            selName = '{0}|{1}'.format(pastPart, name)
            try:
                grp = pm.PyNode(selName)
            except pm.MayaNodeError:
                logger.debug('Could not find %s, creating it.', selName)
                grp = pm.group(name=name, world=True, empty=True)
                if pastPart:
                    pm.parent(grp, pm.PyNode(pastPart))

            past_parts.append(unicode(grp))

        return grp

    def cleanup_import(self, imported_objects):
        result = []
        for obj in imported_objects:
            try:
                if obj.type() in self.safe_types:
                    result.append(obj)
                else:
                    pm.delete(obj)
            except pm.MayaNodeError:
                pass

        return result

    def regroup_import(self, imported_objects, parent):
        group_objects = [x for x in imported_objects if x.type() == 'transform']
        top_level_group = pm.group(group_objects, world=True, name=self.data['name'])
        pm.parent(top_level_group, parent)
        return top_level_group

    def apply_transform(self, transform, matrix=None):
        if not matrix:
            transform.setMatrix(self.data['transformMatrix'])
        else:
            transform.setMatrix(matrix)

    def apply_instances(self, master):
        for instance in self.data.get('instancedCopies', []):
            instance_object = pm.instance(master, name=self.data['instancedCopies'][instance]['name'])[0]
            self.apply_transform(instance_object, self.data['instancedCopies'][instance]['transformMatrix'])

    def apply_materials(self, objects):
        print self.materials_json


def main():
    x = MoanaMayaFile('isLavaRocks')
    y = x.load_geometry(apply_transform=True, apply_instances=True)
    return y
