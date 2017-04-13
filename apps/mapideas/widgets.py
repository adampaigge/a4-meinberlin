from django.contrib.staticfiles.storage import staticfiles_storage
from adhocracy4.maps import widgets as maps_widgets


class MapChoosePolygonPresetsWidget(maps_widgets.MapChoosePolygonWidget):
    class Media(maps_widgets.MapChoosePolygonWidget.Media):
        js = maps_widgets.MapChoosePolygonWidget.Media.js + (
            staticfiles_storage.url('pick_preset.js'),
        )

    def render(self, name, value, attrs):
        html = '<select><option value="">polygon</option></select>'
        html += super().render(name, value, attrs)

        return html
