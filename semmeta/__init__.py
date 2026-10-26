# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# semmeta/__init__.py
# __init__.py makes a folder behave like a Python package. 
# It runs when the package is imported and helps prepare tools or settings.

# Core imports
from .metadata_extractor_module import SEMMetaData
from .json_cleaner_module import JsonCleaner
from .visualizer_module import SEMVisualizer

# Instantiate reusable objects (optional)
SEMMeta = SEMMetaData()
CLEANER = JsonCleaner()

# Allow users to cleanly import these classes and objects directly
__all__ = ['SEMMetaData', 'JsonCleaner', 'SEMVisualizer', 'SEMMeta', 'CLEANER']
