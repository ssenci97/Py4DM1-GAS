# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Unit tests for the SEM metadata extraction exercise.
#
# Run using:
#
#     pytest -v
#
# The tests verify:
#
#     1. Instrument metadata can be converted
#        from a list into a dictionary.
#
#     2. Empty metadata is handled correctly.
#
#     3. Metadata values are cleaned correctly.
#
#     4. Dictionary entries containing None
#        are removed during cleaning.
#
#     5. Missing or invalid image files are
#        handled without crashing the pipeline.
#
# These tests help validate the most important
# components of the workflow before running the
# full SEM metadata extraction pipeline.
#





import sys
from pathlib import Path

# Add project root directory to Python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Import SEM processing classes
from semmeta import SEMMeta
from semmeta import CLEANER
from semmeta import JsonCleaner


# Test conversion of instrument metadata into a dictionary
def test_instrument_metadata_dictionary():

    # Simulated metadata extracted from tag 34118
    metadata_list = [
        "AP_WD", "3.18 mm",
        "AP_BEAM_CURRENT", "13 pA",
        "AP_HOLDER_HEIGHT", "10 mm"]

    # Convert list into dictionary
    metadata_dict = SEMMeta.InsMetaDict(metadata_list)

    # Verify expected values
    assert metadata_dict["AP_WD"] == "3.18 mm"
    assert metadata_dict["AP_BEAM_CURRENT"] == "13 pA"
    assert metadata_dict["AP_HOLDER_HEIGHT"] == "10 mm"


# Test behavior when metadata list is empty
def test_empty_instrument_metadata():

    metadata_dict = SEMMeta.InsMetaDict([])

    assert metadata_dict == {}


# Test extraction of value and unit from metadata string
def test_clean_value():

    cleaner = JsonCleaner()

    result = cleaner.clean_value(
        "AP_WD = 3.18 mm" )

    assert result == "3.18 mm"


# Test removal of entries containing None values
def test_clean_dictionary():

    cleaner = JsonCleaner()

    raw_metadata = {
        "AP_WD": "3.18 mm",
        "AP_BEAM_CURRENT": "13 pA",
        "AP_NULL_PARAMETER": None }

    cleaned_metadata = cleaner.clean_dict(
        raw_metadata )

    assert "AP_WD" in cleaned_metadata
    assert "AP_BEAM_CURRENT" in cleaned_metadata
    assert "AP_NULL_PARAMETER" not in cleaned_metadata


# Test handling of non-existing image files
def test_non_existing_image():

    metadata = SEMMeta.ExtractMetadata(
        "this_file_does_not_exist.tif" )

    assert metadata == {}
    

# Test the complete metadata extraction workflow
def test_processing_pipeline(tmp_path):

    # Select one known SEM image
    image_path = "imgs/1/12_50_vero_09.tif"

    # Extract metadata
    metadata = SEMMeta.ExtractMetadata(image_path)

    # Verify metadata was extracted
    assert metadata != {}

    # Define temporary JSON files
    raw_json = tmp_path / "raw.json"
    cleaned_json = tmp_path / "cleaned.json"

    # Save raw metadata
    SEMMeta.WriteSEMJson(
        raw_json,
        metadata )

    # Verify raw JSON file exists
    assert raw_json.exists()

    # Clean metadata
    CLEANER.process(raw_json)
    CLEANER.save_cleaned(cleaned_json)

    # Verify cleaned JSON file exists
    assert cleaned_json.exists()
