'use strict';
var $ = require('jquery');

module.exports = {
  versionElements: {
    toc: $('nav#toc'),
    regLandingPage: $('section[data-base-version]'),
    timelineList: $('#timeline li.current'),
    diffToc: $('#table-of-contents'),
  }
};