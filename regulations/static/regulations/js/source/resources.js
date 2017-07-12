// Resources.js pulls out pieces tied to the DOM
// for easier testing.

'use strict';

module.exports = {
  // These are elements for the findVersion and findBaseVersion
  // functions in helpers.js
  versionElements: {
    toc: 'nav#toc',
    regLandingPage: 'section[data-base-version]',
    timelineList: '#timeline li.current',
    diffToc: '#table-of-contents'
  }
};
