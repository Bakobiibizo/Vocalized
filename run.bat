@ECHO OFF
REM Activate Environment
"./.venv/bin/activate"
echo "Environment Activated"

REM Copy selected text
python copy_selected.py
echo "Text copier running, ctrl+alt+s to copy the selected text and generate voice"

