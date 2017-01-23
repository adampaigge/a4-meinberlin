$(document).ready(function() {
  var $page = $('.embed-page');
  var $modal = $('.embed-modal');
  var state = {};
  window.a4state = state;

  var clickHandler;

  var load = function(url, $target) {
    return $.ajax(url).then(function(html) {
      var $main = $(html).filter('main');
      $target.empty();
      $target.append($main.children());
      adhocracy4.onReady($target);
    });
  };

  var setState = function(newState) {
    var promises = [];

    if (state.url !== newState.url) {
      promises.push(load(newState.url, $page));
    }
    if (state.modal !== newState.modal && newState.modal) {
      promises.push(load(newState.modal, $modal));
    }

    return Promise.all(promises).then(function() {
      state.url = newState.url;
      state.modal = newState.modal;
      if (state.modal) {
        $modal.show();
      } else {
        $modal.hide();
      }
    });
  }

  var clickHandler = function(event) {
    if (event.target.href) {
      event.preventDefault();
      var target = event.target.dataset.embedTarget;
      if (target === 'page' || (!target && !state.modal)) {
        setState({
          url: event.target.href,
        });
      } else {
        setState({
          url: state.url,
          modal: event.target.href,
        });
      }
    }
  };

  $page.on('click', clickHandler);
  $modal.on('click', clickHandler);
  setState({
    url: 'http://localhost:8000/projects/project1/'
  });
});
