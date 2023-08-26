import os
import time
import json
from pptx import Presentation
import openai
from PowerPointReader import read_powerpoint  # Import your read_powerpoint function


def main():
    uploads_folder = r'C:\Users\aviga\Documents\Ofek\Year 3\semester 2\Excelentim\pythonProject\final_prodj\final-projects-avigayilm\uploads'
    outputs_folder = r'C:\Users\aviga\Documents\Ofek\Year 3\semester 2\Excelentim\pythonProject\final_prodj\final-projects-avigayilm\outputs'

    # Check if the outputs folder exists, if not, create it
    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)

    while True:
        if not os.path.exists(uploads_folder):
            continue
        # Scan the uploads folder for new files
        new_files = [filename for filename in os.listdir(uploads_folder)]

        for file in new_files:
            output_filename = os.path.splitext(file)[0] + ".json"
            output_path = os.path.join(outputs_folder, output_filename)
            file_path = os.path.join(uploads_folder, file)

            print(f"Processing file: {file}")
            explanation_data = read_powerpoint(file_path)  # Use your read_powerpoint function
            with open(output_path, 'w') as output_file:
                json.dump(explanation_data, output_file, indent=4)  # Write the JSON data to the output file
            print(f"Explanation saved for {file}")
            # Delete the processed file from the to_be_processed folder
            processed_file = os.path.join(uploads_folder, file)
            os.remove(processed_file)
            print("powerpoint read")

            time.sleep(10)  # Sleep for 10 seconds before the next iteration

if __name__ == '__main__':
    main()
