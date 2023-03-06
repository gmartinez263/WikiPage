#!/usr/bin/env bash

export FLASK_APP=flaskr
export FLASK_ENV=development
export PYTHONPATH="$PWD/flaskr"
flask run -p 8080