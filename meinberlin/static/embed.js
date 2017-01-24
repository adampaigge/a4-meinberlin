$(document).ready(function() {
  var $page = $('.embed-page');
  var $modal = $('.embed-modal');
  var $platformLink = $('.platform-link');
  var state = {};
  var popup;
  window.a4state = state;

  var onReady = function($target) {
    adhocracy4.onReady($target);

    $target.find('form[action]').submit(function(event) {
      event.preventDefault();
      var form = this;

      setTimeout(function() {
        loadHtml($.ajax({
          url: form.action,
          method: form.method,
          data: $(form).serialize(),
        }), $target);
      });
    });

    $target.find('.messages > *').each(function(index, el) {
      setTimeout(function() {
        $(el).remove();
      }, 10000);
    });
  };

  var loadHtml = function(promise, $target) {
    return promise.then(function(html) {
      var $main = $(html).filter('main');
      $target.empty();
      $target.append($main.children());
      onReady($target);
    });
  };

  var setHidden = function($element, hidden) {
    // see https://www.paciellogroup.com/blog/2012/05/html5-accessibility-chops-hidden-and-aria-hidden/
    if (hidden) {
      $element.addClass('is-hidden');
      setTimeout(function() {
        $element.attr('hidden', true)
        $element.hide();
      }, 500);  // transition takes 0.5s
    } else {
      $element.attr('hidden', null);
      $element.show();
      $element.removeClass('is-hidden');
    }
  };

  var setState = function(newState, ignoreHistory) {
    var promises = [];

    if (state.url !== newState.url) {
      promises.push(loadHtml($.ajax(newState.url), $page));
    }
    if (state.modal !== newState.modal && newState.modal) {
      promises.push(loadHtml($.ajax(newState.modal), $modal));
    }

    return Promise.all(promises).then(function() {
      state.url = newState.url;
      state.modal = newState.modal;
      if (!ignoreHistory) {
        history.pushState(newState, '');
      }
      $platformLink.attr('href', state.modal || state.url);
      setHidden($modal, !state.modal);
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

  window.addEventListener('popstate', function(event) {
    setState(event.state, true);
  });

  window.addEventListener('message', function(event) {
    var message = JSON.parse(event.data);
    if (message.name === "popup-close" && event.origin === location.origin) {
      popup.close();
      popup = null;
      location.reload();
    }
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
