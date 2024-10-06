#!/bin/bash

python3 setup.py build_ext --inplace
exec python3 main.py

