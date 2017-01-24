$(document).ready(function() {
  var $page = $('.embed-page');
  var $modal = $('.embed-modal');
  var state = {};
  var popup;
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

  var setState = function(newState, ignoreHistory) {
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
      if (!ignoreHistory) {
        history.pushState(newState, '');
      }
      if (state.modal) {
        $modal.removeClass('is-hidden');
        $modal.attr('aria-hidden', false);
      } else {
        $modal.addClass('is-hidden');
        $modal.attr('aria-hidden', true);
      }
    });
  }

  var clickHandler = function(event) {
    if (event.target.href && !event.target.target) {
      event.preventDefault();
      var target = event.target.dataset.embedTarget;
      if (target === 'popup') {
        popup = window.open(event.target.href, "_blank", "width=1000,height=750");
      } else if (target === 'page' || (!target && !state.modal)) {
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

  window.addEventListener('message', function(event) {
    var message = JSON.parse(event.data);
    if (message.name === "popup-close" && event.origin === location.origin) {
      popup.close();
      popup = null;
      location.reload();
    }
  });

  window.addEventListener('popstate', function(event) {
    setState(event.state, true);
  });

  if (window.opener) {
    window.opener.postMessage(JSON.stringify({
      name: "popup-close",
    }), location.origin);
  } else {
    $(document).on('click', clickHandler);
    setState({
      url: 'http://localhost:8000/projects/project1/'
    });
  }
});
