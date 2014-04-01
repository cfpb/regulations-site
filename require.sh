#!/bin/bash
UICONF=regulations/static/regulations/js/source/require.config.js
TESTCONF=regulations/static/regulations/js/unittests/test.config.js
rm -f $UICONF
touch $UICONF
echo 'var require = { "paths" :' >> $UICONF
cat require.paths.json >> $UICONF
echo ', "shim":' >> $UICONF
cat require.shim.json >> $UICONF
echo '}' >> $UICONF
rm -f $TESTCONF
touch $TESTCONF
echo 'require.config({"baseUrl": "/static/regulations/js/source", "paths":' >> $TESTCONF
cat require.paths.json >> $TESTCONF
echo ', "shim":' >> $TESTCONF
cat require.shim.json >> $TESTCONF
echo '});' >> $TESTCONF
echo "require(['specs/helpers-spec.js'], function() {
            if (window.mochaPhantomJS) { mochaPhantomJS.run(); }
            else { mocha.run(); }
        });" >> $TESTCONF
