var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings
var initDropdown = require('./dropdown');

// make jquery available for non-webpack js
window.jQuery = window.$ = require('jquery');

var onReady = function($wrapper) {
  initDropdown($wrapper);
};

$(document).ready(function() {
  onReady($(document));
});

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings,
  'onReady': onReady
}
