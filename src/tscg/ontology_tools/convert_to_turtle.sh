#!/bin/bash
################################################################################
# TSCG JSON-LD to OWL Turtle Converter - Unix/Linux/Mac Shell Script
################################################################################
# Author: Echopraxium with the collaboration of Claude AI
# Date: 2026-02-15
# Version: 1.0.0
################################################################################

set -e  # Exit on error

echo ""
echo "======================================================================"
echo "TSCG JSON-LD to OWL Turtle Converter"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check if rdflib is installed
if ! python3 -c "import rdflib" &> /dev/null; then
    echo "WARNING: rdflib not found. Installing..."
    echo ""
    pip3 install rdflib
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install rdflib"
        echo "Please run manually: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Run conversion
echo "Starting conversion..."
echo ""

python3 jsonld_to_turtle.py --skip-errors

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "SUCCESS: Conversion completed!"
    echo "======================================================================"
    echo ""
    echo "All .jsonld files have been converted to .ttl format."
    echo "You can now open them in Protégé or use with OWL reasoners."
    echo ""
else
    echo ""
    echo "======================================================================"
    echo "WARNING: Conversion completed with errors"
    echo "======================================================================"
    echo ""
    echo "Check the log file for details."
    echo ""
fi
