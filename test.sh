#!/usr/bin/env bash

export FLASK_APP=flaskr
export FLASK_ENV=development
export PYTHONPATH="$PWD/flaskr"

# Run the tests using pytest
pytest --ignore=env