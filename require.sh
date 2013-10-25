rm -f regserver/regulations/static/regulations/js/source/require.config.js
echo 'var require = { "paths" :' >> regserver/regulations/static/regulations/js/source/require.config.js
cat require.paths.json >> regserver/regulations/static/regulations/js/source/require.config.js
echo ', "shim":' >> regserver/regulations/static/regulations/js/source/require.config.js
cat require.shim.json >> regserver/regulations/static/regulations/js/source/require.config.js
echo '}' >> regserver/regulations/static/regulations/js/source/require.config.js
