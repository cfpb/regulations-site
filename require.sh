#!/bin/bash
UICONF=regserver/regulations/static/regulations/js/source/require.config.js
TESTCONF=regserver/regulations/static/regulations/js/tests/browser/test.config.js
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
echo '}' >> $TESTCONF
