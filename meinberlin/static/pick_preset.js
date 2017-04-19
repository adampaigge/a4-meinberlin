/* eslint-disable no-undef */
$('[data-map="choose_polygon"]').each(function (i, e) {
  var name = e.getAttribute('data-name')

  $('#select_' + name).on('change', function (event) {
    var geoJson = event.target.value
    drawnItems.clearLayers()
    if (geoJson) {
      var group = L.geoJson(JSON.parse(geoJson))
      group.eachLayer(function (layer) {
        drawnItems.addLayer(layer)
      })
    }
    $('#id_' + name).val(geoJson)
  })
})
