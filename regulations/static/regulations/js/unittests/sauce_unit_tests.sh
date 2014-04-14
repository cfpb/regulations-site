curl -X POST https://saucelabs.com/rest/v1/$SAUCE_USERNAME/js-tests -u $SAUCE_USERNAME:$SAUCE_ACCESS_KEY -H 'Content-Type: application/json' \
    --data '{                                                     
        "platforms": [["Windows 7", "firefox", "20"],                          
                      ["Linux", "googlechrome", ""]],                          
        "url": "http://localhost:8000/static/regulations/js/unittests/runner.html",
        "framework": "mocha"}'
