import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import loader

from adhocracy4.maps import widgets as maps_widgets
from apps.mapideas.models import MapPreset


class MapChoosePolygonPresetsWidget(maps_widgets.MapChoosePolygonWidget):
    class Media(maps_widgets.MapChoosePolygonWidget.Media):
        js = maps_widgets.MapChoosePolygonWidget.Media.js + (
            staticfiles_storage.url('pick_preset.js'),
        )

    def render(self, name, value, attrs):
        presets = [
            {
                'name': preset.name,
                'preset': json.dumps(preset.preset)
            }
            for preset in MapPreset.objects.all()
        ]

        context = {
            'presets': presets,
            'map': super().render(name, value, attrs),
            'name': name,
        }

        return loader.render_to_string(
            'meinberlin_mapideas/map_choose_polygon_presets_widget.html',
            context
        )
