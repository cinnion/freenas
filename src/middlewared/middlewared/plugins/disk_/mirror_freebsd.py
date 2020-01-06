import os

from bsd import geom
from copy import deepcopy

from middlewared.service import Service

from .mirror_base import DiskMirrorBase


class DiskService(Service, DiskMirrorBase):

    def get_mirrors(self):
        mirrors = []
        geom.scan()
        klass = geom.class_by_name('MIRROR')
        if not klass:
            return mirrors
        for g in klass.geoms:
            mirror_data = {
                **deepcopy(self.mirror_base),
                'name': g.name,
                'config_type': g.config.get('Type') if g.config else None,
                'path': os.path.join('/dev/mirror', g.name),
                'real_path': os.path.join('/dev/mirror', g.name),
            }
            if os.path.exists(f'{mirror_data["path"]}.eli'):
                mirror_data['path'] = f'{mirror_data["path"]}.eli'
            for c in g.consumers:
                mirror_data['providers'].append({
                    'name': c.provider.name, 'id': c.provider.id, 'disk': c.provider.geom.name
                })
            mirrors.append(mirror_data)

        return mirrors