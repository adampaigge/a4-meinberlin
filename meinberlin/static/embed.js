$(document).ready(function() {
  var $page = $('.page');
  var $popup = $('.popup');
  var state = {};

  var clickHandler;

  var load = function(url, $target) {
    return $.ajax(url).then(function(html) {
      var $main = $(html).filter('main');
      $target.empty();
      $target.append($main.children());
      $target.on('click', clickHandler);
    });
  };

  var setState = function(newState) {
    var promises = [];

    if (state.url !== newState.url) {
      promises.push(load(newState.url, $page));
    }
    if (state.popup !== newState.popup) {
      promises.push(load(newState.popup, $popup));
    }

    return Promise.all(promises).then(function() {
      if (newState.popup) {
        $popup.hide();
      } else {
        $popup.show();
      }
    });
  }

  var clickHandler = function(event) {
    if (event.target.href) {
      event.preventDefault();
      setState({
        url: event.target.href
      });
    }
  };

  setState({
    url: 'http://localhost:8000/projects/project1/'
  });
});
