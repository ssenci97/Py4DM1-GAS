# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Pytest configuration file.
#
# This file is automatically discovered by pytest before running tests.
#
# Purpose:
#     Make the semmeta package visible to the test suite.
#
# Project structure:
#
#     .
#     ├── main.py
#     ├── semmeta
#     │   ├── __init__.py
#     │   ├── metadata_extractor_module.py
#     │   ├── json_cleaner_module.py
#     │   └── visualizer_module.py
#     └── tests
#         ├── conftest.py
#         └── test_semmeta.py
#
# Without this configuration pytest may fail with:
#
#     ModuleNotFoundError: No module named 'semmeta'
#
# because the project root directory is not automatically
# added to Python's import path.
#

import sys
from pathlib import Path

# Get project root directory
ROOT = Path(__file__).resolve().parents[1]

# Add project root directory to Python path
sys.path.insert(0, str(ROOT))
