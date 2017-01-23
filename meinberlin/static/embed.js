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
      adhocracy4.onReady($target);
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
        $popup.show();
      } else {
        $popup.hide();
      }
    });
  }

  var clickHandler = function(event) {
    if (event.target.href) {
      event.preventDefault();
      var target = event.target.dataset.embedTarget;
      if (target === 'page' || (!target && !state.popup)) {
        setState({
          url: event.target.href,
        });
      } else {
        setState({
          url: state.url,
          popup: event.target.href,
        });
      }
    }
  };

  setState({
    url: 'http://localhost:8000/projects/project1/'
  });
});
