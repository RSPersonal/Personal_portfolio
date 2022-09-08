#!/usr/bin/env bash
source env/scripts/activate
coverage run -m unittest discover
coverage report