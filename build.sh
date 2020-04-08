#! /bin/bash

echo "Build wheel"
python3.7 ${PWD}/setup.py sdist bdist_wheel

echo "Validate the build"
if [ $(python3.7 -m twine check ${PWD}/dist/* | grep FAIL | wc -l) -gt 0 ]; then
    echo "twine validation failed"
    exit
fi
echo "OK"
