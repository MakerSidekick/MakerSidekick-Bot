#!/usr/bin/bash

# Cleanup old
rm -rf lib

# Download lib with git
git clone https://github.com/stlehmann/micropython-ssd1306 lib/

# cleanup
rm -rf lib/.git lib/.gitignore lib/README.md lib/sdist_upip.py lib/setup.py
