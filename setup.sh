#!/bin/bash
echo "Installing sentence-tranformers"
pip install sentence-transformers
echo "Downloading Model and saving it"
python init.py