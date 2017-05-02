/* global $ */
var init = function () {
  $('[data-toggle="popover"]').popover()
}

$(init)
$(document).on('a4.embed.ready', init)

$('body').on('click', function (e) {
  $('[data-toggle="popover"]').each(function () {
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
      $(this).popover('hide')
    }
  })
})
