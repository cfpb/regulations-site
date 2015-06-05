#!/bin/sh

set -ev

if [ ! -f config.json ]; then
  cp example-config.json config.json
fi

npm install
bower install
grunt build
