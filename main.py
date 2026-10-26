# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#

# Import modules for file system operations (os), command-line
# arguments (sys), and recursive file search (glob)
import os
import sys
import glob

# Import SEM processing classes: metadata extractor, cleaner, and visualizer
from semmeta import SEMMeta, CLEANER, SEMVisualizer


# Define the main function of the script
def main():

    # Ensure the user provides the root folder of the SEM images as a command-line argument
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <SEM images root folder>")

    # Get the root folder of the SEM images from the command-line arguments
    sem_root = sys.argv[1]

    # Build a search pattern matching all files in the root folder and its subfolders
    sem_path = os.path.join(sem_root, "**", "*")

    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Initialize the list storing the processing status of each image
    processing_report = []

    # Iterate over all files and folders found recursively in the root folder
    for semimage in glob.iglob(sem_path, recursive=True):

        # Skip directories (only files are processed)
        if not os.path.isfile(semimage):
            continue

        # Process only files with a supported SEM extension (.tif, .tiff, .TIF, .TIFF)
        if semimage.endswith(SEMMeta.semext):

            # Extract the image name (without extension) for output naming
            image_name = os.path.splitext(os.path.basename(semimage))[0]

            # Print the image currently being processed
            print("\nProcessing SEM IMAGE:", semimage)

            # Extract SEM instrument metadata
            sem_metadata = SEMMeta.ExtractMetadata(semimage)

            # Continue only if instrument metadata was extracted
            if sem_metadata:

                print("Good image for processing", semimage)

                # Record the image as successfully processed
                processing_report.append(
                    {
                        "image": semimage,
                        "status": "OK" })

                # Define output paths for raw and cleaned metadata JSON files
                output_path_raw = os.path.join("output", f"{image_name}_raw.json")
                output_path_cleaned = os.path.join("output", f"{image_name}_cleaned.json")

                # Save raw metadata
                SEMMeta.WriteSEMJson(output_path_raw, sem_metadata)

                # Clean metadata and save the cleaned JSON file
                CLEANER.process(output_path_raw)
                CLEANER.save_cleaned(output_path_cleaned)

                # Create the visualizer for the image and its cleaned metadata
                visualizer = SEMVisualizer(json_path=output_path_cleaned, image_path=semimage )

                # Display the image with the metadata table and save the figure
                visualizer.show_image_with_table()

            # Image could not be opened or contains no instrument metadata
            else:

                print("Bad image for processing", semimage)

                # Record the image as failed
                processing_report.append(
                    {
                        "image": semimage,
                        "status": "ERROR" })

    # Define the path of the processing report
    report_file = os.path.join("output", "processing_report.txt" )

    # Save the processing status of all images
    SEMMeta.WriteProcessingReport(report_file, processing_report )

    # Print the location of the saved report
    print("\nProcessing report saved to:")
    print(report_file)


# Run the main function only if this script is executed directly (not imported)
if __name__ == "__main__":
    main()
