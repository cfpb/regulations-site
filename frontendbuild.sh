#!/bin/sh

set -ev

if [ ! -f config.json ]; then
  cp example-config.json config.json
fi

npm install
npm run test:js
grunt
