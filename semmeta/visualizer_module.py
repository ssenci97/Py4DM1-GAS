# Written by Ahmed Khalil ahmed.khalil@areasciencepark.it
# Thank you Ahmed
#
# Import modules for file system operations (os), JSON parsing (json), 
# and regular expressions -- regex (re)
import os, json, re

# Import PIL for image loading and matplotlib for visualization
from PIL import Image
import matplotlib.pyplot as plt

# Class for visualizing SEM images alongside selected metadata
class SEMVisualizer:
    def __init__(self, json_path, image_path):
        # Store the path to the cleaned metadata JSON file
        self.json_path = json_path
        # Store the path to the SEM image file
        self.image_path = image_path
        # Define the list of metadata variables to extract and display
        self.variables = [
            "AP_WD",
            "AP_BEAM_TIME",
            "AP_IMAGE_PIXEL_SIZE",
            "AP_HOLDER_HEIGHT",
            "AP_BEAM_CURRENT",
            "AP_HOLDER_DIAMETER"]        
        # Initialize an empty dictionary to hold loaded metadata
        self.metadata = {}

    # Load metadata from JSON file into self.metadata
    def load_metadata(self):
        """
        Reads the cleaned JSON file into metadata.
        """
        fp = self.json_path
        if not os.path.exists(fp):
            raise ValueError(f"{fp} is missing")
        # Open the file object and use json.load()
        with open(fp, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        if not metadata:
            metadata = {}
            print("[semmeta-INFO] Empty Metadata")            
        return metadata

    def clean_value(self, raw_value, variable_name=None):
        """
        Splits a cleaned metadata value into its number and unit.
        The value must be a (signed) number, optionally in scientific
        notation, followed by a unit. Otherwise ("N/A", "N/A") is returned.
        Examples:
            "3.18 mm"         ->  ("3.18", "mm")
            "-13 pA"          ->  ("-13", "pA")
            "2.34e-006 mbar"  ->  ("2.34e-006", "mbar")
            "InLens" or None  ->  ("N/A", "N/A")
        Returns:
            (value, unit) as strings, or ("N/A", "N/A") if no
            number followed by a unit is found
        """
        # Ensure the input is a string before applying regex
        if not isinstance(raw_value, str):
            return ("N/A", "N/A")
        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', raw_value.strip())
        # If a match is found, return the value and the unit
        if match:
            value, unit = match.groups()
            return (value, unit)
        # Return fallback values (Not Available) if no match is found
        return ("N/A", "N/A")

    def extract_variables(self):
        """
        Extracts selected metadata variables and formats
        them into (name, value, unit) tuples for display.        
        Missing variables give (name, "N/A", "N/A").
        Return the list of formatted metadata rows
        """
        metadata = self.load_metadata()
        rows = []
        for var_key in self.variables:
            # Get the raw value from the metadata dictionary (defaults to None if missing)
            raw_value = metadata.get(var_key)    
            # Clean the value and get (value, unit) using self.clean_value
            value, unit = self.clean_value(raw_value)
            # Append the formatted tuple (name, value, unit)
            rows.append((var_key, value, unit))
            
        # Fixed: return rows OUTSIDE the loop so all variables are processed
        return rows

    def show_image_with_table(self):
        """
        Displays the SEM image alongside a formatted metadata
        table and saves the combined output as a figure.

        1. Loads the metadata/extracted variables.
        2. Builds an A4-sized figure with two vertically stacked panels:
           the grayscale SEM image (top) and a table with the
           column labels "Variable", "Value", "Unit" (bottom).
        3. Creates the folder ./output if needed.
        4. Displays the figure, then closes it.
        """
        rows = self.extract_variables()
        fig, axes = plt.subplots(2, 1, figsize=(8.27, 11.69), gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.3})
        ax_img, ax_table = axes
        if os.path.exists(self.image_path):
            img = Image.open(self.image_path)
            ax_img.imshow(img, cmap='gray')
        else:
            ax_img.text(0.5, 0.5, f"Image not found:\n{self.image_path}", ha='center', va='center', fontsize=12, color='red')
        ax_img.axis('off')
        ax_img.set_title("SEM Image & Metadata Summary", fontsize=14, fontweight='bold', pad=15)
        ax_table.axis('off')
        col_labels = ["Variable", "Value", "Unit"]
        table_data = [[r[0], r[1], r[2]] for r in rows]
        table = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.0, 1.8)
        for (row_idx, col_idx), cell in table.get_celld().items():
            if row_idx == 0:
                cell.set_facecolor('#eaeaea')
                cell.set_text_props(weight='bold')
        plt.tight_layout()
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)