#!/bin/bash

# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Update pip
python -m pip install --upgrade pip

# Install wheel and setuptools
pip install wheel setuptools

# Install the requirements
pip install -r requirements.txt

# Run the program
python copy_selected.py

echo "Setup complete!"
read -p "Press enter to continue"