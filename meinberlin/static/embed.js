/* global $ */
$(document).ready(function () {
  var $main = $('main')
  var currentPath

  var loadHtml = function (html, textStatus, xhr) {
    var $root = $(html).filter('main')
    currentPath = xhr.getResponseHeader('x-ajax-path')
    $main.empty()
    $main.append($root.children())
    onReady()
  }

  var onReady = function () {
    // adhocracy4.onReady($main)
  }

  var getEmbedTarget = function ($element, url) {
    var embedTarget = $element.data('embedTarget')

    if (embedTarget) {
      return embedTarget
    } else if (!url || url[0] === '#' || $element.attr('target')) {
      return 'ignore'
    } else if ($element.is('.rich-text a')) {
      return 'external'
    } else {
      return 'internal'
    }
  }

  $(document).on('click', 'a[href]', function (event) {
    // NOTE: event.target.href is resolved against /embed/
    var url = event.target.getAttribute('href')
    var $link = $(event.target)
    var embedTarget = getEmbedTarget($link, url)

    if (embedTarget === 'internal') {
      event.preventDefault()

      if (url[0] === '?') {
        url = currentPath + url
      }

      $.ajax({
        url: url,
        success: loadHtml
      })
    }
  })

  $(document).on('submit', 'form[action]', function (event) {
    var form = event.target
    var $form = $(form)
    var embedTarget = getEmbedTarget($form, form.method)

    if (embedTarget === 'internal') {
      event.preventDefault()

      $.ajax({
        url: form.action,
        method: form.method,
        data: $form.serialize(),
        success: loadHtml
      })
    }
  })

  $.ajax({
    url: $('body').data('url'),
    success: loadHtml
  })
})
