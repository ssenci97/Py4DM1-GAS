# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import PIL image module for reading TIFF metadata
from PIL import Image

import re

# Import JSON module for exporting metadata
import json


# SEMMetaData Class Initialization
class SEMMetaData:
    def __init__(self, semext=(".tif", ".tiff", ".TIF", ".TIFF"), semInsTag=34118):

        # Store accepted SEM image file extensions
        self.semext = semext

        # Store SEM-specific instrument metadata tag identifier
        self.semInsTag = semInsTag

        # Initialize dictionary to hold extracted image metadata
        self.image_metadata = {}

    def OpenCheckImage(self, image):
        """
        Opens an image file and verifies its accessibility and format.
        Returns:
            PIL Image object if successful
            False otherwise
        """

        # TODO (Task 1): implement this method
        raise NotImplementedError("OpenCheckImage is not implemented yet")       


    def ImageMetadata(self, img):
        """
        Extracts TIFF metadata from an opened SEM image.

        Returns:
            TIFF tags of the image
            empty dict if the tags cannot be read
        """

        try:

            # Store all TIFF tags of the opened image
            self.image_metadata = img.tag

            return self.image_metadata

        except Exception as e:
            print("Error reading image metadata:", str(e))

            # Reset metadata so tags from a previous image are not reused
            self.image_metadata = {}
            return self.image_metadata


    @property
    def GetInsMetadata(self):
        """
        Extracts instrument-specific metadata from TIFF tag 34118.

        The tag contains a numeric preamble of variable length,
        followed by alternating lines of parameter keys and values,
        and ends with the 'END' marker.

        Returns:
            list containing alternating keys and values
            empty list if tag 34118 is not found
        """

        try:

            # Retrieve instrument metadata stored in tag 34118
            raw_metadata = self.image_metadata[self.semInsTag][0]

            # Pattern of instrument parameter keys (e.g. AP_WD, DP_DETECTOR_CHANNEL, DP_DETECTOR_TYPE, ...)
            SEM_KEY_PATTERN = re.compile(r"^[A-Z]{2}_[A-Z0-9_]+$")

            # Marker indicating the end of the instrument metadata
            SEM_END_MARKER = "END"

            # Split metadata into lines and remove surrounding spaces
            lines = [line.strip() for line in raw_metadata.splitlines()]

            # Initialize list to hold alternating keys and values
            instrument_metadata = []

            # Initialize line index
            i = 0
            
            # Iterate over the metadata lines
            while i < len(lines) - 1:

                # Stop when the end marker is reached
                if lines[i] == SEM_END_MARKER:
                    break

                # Check if the current line is a parameter key
                if SEM_KEY_PATTERN.match(lines[i]):

                    # Store the key and the value in the following line
                    instrument_metadata.extend([lines[i], lines[i + 1]])

                    # Move to the next key
                    i += 2

                else:
                    # Skip header, empty or unexpected lines
                    i += 1

            return instrument_metadata

        except (KeyError, IndexError, AttributeError):
            return []


    def InsMetaDict(self, metadata_list):
        """
        Converts instrument metadata list into a dictionary.

        Example:

            ['AP_WD', '3.18 mm',
             'AP_BEAM_CURRENT', '13 pA']

        becomes

            {
                'AP_WD': '3.18 mm',
                'AP_BEAM_CURRENT': '13 pA'
            }
        """

        try:

            # Extract alternating keys
            keys = metadata_list[0::2]

            # Extract alternating values
            values = metadata_list[1::2]

            # Create dictionary
            metadata_dict = dict(zip(keys, values))

            return metadata_dict

        except Exception as e:

            print("Error parsing instrument metadata:", str(e))
            return {}


    def ExtractMetadata(self, image_path):
        """
        Performs the full metadata extraction workflow.

        Returns:
            dict containing instrument metadata
        """

        # Verify image accessibility and keep the opened image object
        img = self.OpenCheckImage(image_path)

        if not img:
            return {}

        # Extract TIFF tags from the opened image
        self.ImageMetadata(img)

        # Extract instrument metadata
        instrument_metadata = self.GetInsMetadata

        # Convert to dictionary
        metadata_dict = self.InsMetaDict(instrument_metadata)
        return metadata_dict

    def WriteSEMJson(self, file, semdict):
        """
        Open the file in write mode and serialize the metadata dictionary.

        Parameters:
            file    : str or pathlib.Path - output path
            semdict : dict - metadata dictionary

        Behaviour:
            Writes semdict to file as JSON with an indentation of 2 spaces.

        Returns:
            None
        """

        # TODO (Task 1): implement this method
        raise NotImplementedError("WriteSEMJson is not implemented yet")    
        
    def WriteProcessingReport(self, file, records):
        """
        Saves the processing status of all SEM images as a text report.

        Parameters:
            file    : str or pathlib.Path - output report path
            records : list of dict, each with the keys
                      "image" (path) and "status" ("OK" or "ERROR")

        Behaviour:
            Writes a title, a line of 60 "=", an empty line, a header row,
            a line of 60 "-", and one aligned row per record
            (status column 10 characters wide, left-aligned).
            See README.md for the expected layout.

        Returns:
            None
        """

        # TODO (Task 1): implement this method
        raise NotImplementedError("WriteProcessingReport is not implemented yet")

 
 
        
