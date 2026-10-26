# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import JSON module for reading and writing metadata files
import json

# Import regular expressions module for parsing numeric values and units
import re


# Class for cleaning and formatting SEM metadata from JSON files
class JsonCleaner:
    def __init__(self, cleaned_data=None): 
        # Never use a mutable default argument ({}): it would be shared by every instance.                      
        # Initialize the cleaned_data dictionary to store processed metadata
        self.cleaned_data = cleaned_data if cleaned_data is not None else {}


    def load_json(self, jsfile):
        """
        Reads a JSON file and returns its content as a Python dict.
        """

        # TODO (Task 2): implement this method
        raise NotImplementedError("load_json is not implemented yet")


    def clean_value(self, value):
        """
        Extracts the numeric value and its unit from a string.

        Only the part after the '=' sign is parsed, and it must be
        a (signed) number followed by a unit. Otherwise the original
        value is returned unchanged.

        Examples:
            "AP_WD = 3.18 mm"              ->  "3.18 mm"
            "Conjugate posn. = -164.00 mm" ->  "-164.00 mm"
            "Opt.Aperture = 2"             ->  "Opt.Aperture = 2"   (unchanged)
            "Detector = InLens"            ->  "Detector = InLens"  (unchanged)

        Returns:
            "<number> <unit>" (one space) if a number followed by a unit
            is found, otherwise value unchanged.
        """

        # Keep only the part after the first '=' (the parameter name is ignored)
        if "=" in value:
            value_part = value.split("=", 1)[1].strip()
        else:
            value_part = value.strip()

        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-164.00 mm', '13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', value_part)

        # If a match is found, return the formatted value and unit
        if match:
            return match.group(1) + ' ' + match.group(2)

        # If no match is found, return the original value unchanged
        return value    


    def clean_dict(self, data):
        """
        Cleans a metadata dictionary.

        String values are cleaned with clean_value(), entries with
        None values are removed, and all other values are kept as-is.

        Example:
            {"AP_WD": "WD = 3.18 mm", "AP_X": None, "AP_N": 5}
            ->  {"AP_WD": "3.18 mm", "AP_N": 5}

        Returns:
            a new dictionary with the cleaned entries
        """
        
        # TODO (Task 2): implement this method
        raise NotImplementedError("clean_dict is not implemented yet")



    def process(self, jsfile):
        """
        Runs the full cleaning workflow on a raw metadata JSON file.

        Loads the raw metadata, cleans it with clean_dict(), and
        stores the result in self.cleaned_data.

        Example:
            cleaner.process("output/image_raw.json")
            ->  {"AP_WD": "3.18 mm", "AP_BEAM_CURRENT": "13 pA", ...}

        Returns:
            the cleaned metadata dictionary
        """    
        # TODO (Task 2): implement this method
        raise NotImplementedError("process is not implemented yet")


    def save_cleaned(self, output_path):
        """
        Saves the cleaned metadata to a JSON file.

        Writes self.cleaned_data (filled by process()) to output_path
        in JSON format with 2-space indentation, so that it can be
        read again later with load_json().

        Example:
            cleaner.process("output/image_raw.json")
            cleaner.save_cleaned("output/image_cleaned.json")

        Returns:
            None
        """    
    
        # TODO (Task 2): implement this method
        raise NotImplementedError("save_cleaned is not implemented yet")
