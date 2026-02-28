#!/bin/bash
python -m flask --app app db upgrade
python -m flask --app app run --host=0.0.0.0 --port=${PORT:-5000}
