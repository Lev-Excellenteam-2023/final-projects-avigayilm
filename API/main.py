from flask import *
import os
import uuid
import time
import glob
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']

    # Check if the uploaded file is a PowerPoint file
    allowed_extensions = {'ppt', 'pptx'}
    file_extension = f.filename.rsplit('.', 1)[-1]

    if file_extension.lower() not in allowed_extensions:
        error_message = "This is not a PowerPoint file."
        return render_template("error.html", message=error_message)

    # Specify the path for the upload folder
    upload_folder = r'C:\Users\aviga\Documents\Ofek\Year 3\semester 2\Excelentim\pythonProject\final_prodj\final-projects-avigayilm\uploads'


    # Check if the folder exists, if not, create it
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


    # Generate a unique UID using uuid4
    unique_uid = str(uuid.uuid4())

    # Generate a timestamp
    timestamp = int(time.time())

    filename_without_extension = os.path.splitext(f.filename)[0]

    # Construct the new filename with original filename, timestamp, and UID
    new_filename = f"{filename_without_extension}_{timestamp}_{unique_uid}.{file_extension}"

    print(new_filename)

    # Save the file to the upload folder with the new filename
    f.save(os.path.join(upload_folder, new_filename))

    # Create a JSON response with the UID
    response = {'uid': unique_uid}
    return jsonify(response)
    #return render_template("success.html", message=unique_uid)


def extract_filename_components(filename):
    # Split the filename using underscores and dots
    filename_parts = filename.split('_')
    filename_without_extension = filename_parts[:-1]
    file_extension = filename_parts[-1].split('.')[1]

    # Extract the components
    original_filename = filename_without_extension[0]
    timestamp = int(filename_without_extension[1])
    print(timestamp)
    # Parse the timestamp into a datetime object
    timestamp_datetime = datetime.fromtimestamp(timestamp)

    return original_filename, timestamp_datetime, file_extension


@app.route('/status', methods=['GET'])
def status():
    if request.method == 'GET':
        uid = request.args.get('uid')  # Get the UID from the URL parameter

        # Check if the UID is in the uploads folder
        upload_folder = r'C:\Users\aviga\Documents\Ofek\Year 3\semester 2\Excelentim\pythonProject\FlaskApplication\uploads'
        file_extension = "pptx"  # Replace with the expected file extension

        # Construct the UID pattern with the wildcard
        uid_pattern = f"*_{uid}.{file_extension}"

        # Search for files matching the UID pattern in the uploads folder
        matching_files = glob.glob(os.path.join(upload_folder, uid_pattern))


        if not matching_files:
            # UID not found in uploads folder, return 'not found'
            response_data = {
                'status': 'not found',
                'filename': None,
                'timestamp': None,
                'explanation': None
            }
            return jsonify(response_data), 404

        # Assuming there's only one matching file (or you can handle multiple matches as needed)
        matching_file_path = matching_files[0]

        # Extract the filename from the path
        filename = os.path.basename(matching_file_path)

        # Extract components using the function
        original_filename, timestamp_datetime, file_extension = extract_filename_components(filename)


        # Check if an explanation JSON file exists in the outputs folder with the given UID
        output_folder = r'C:\Users\aviga\Documents\Ofek\Year 3\semester 2\Excelentim\pythonProject\FlaskApplication\outputs'
        # Construct the UID pattern with the wildcard
        uid_pattern = f"*_{uid}.json"


        # Search for files matching the UID pattern in the uploads folder
        matched_files = glob.glob(os.path.join(output_folder, uid_pattern))

        if not matched_files:
            # Explanation not found in outputs folder, return 'pending'
            response_data = {
                'status': 'pending',
                'filename': original_filename,
                'timestamp': timestamp_datetime,
                'explanation': None
            }
            return jsonify(response_data),200

        with open(matching_files[0], 'r') as json_file:
            json_data = json.load(json_file)
            response_data = {
                'status': 'pending',
                'filename': original_filename,
                'timestamp': timestamp_datetime,
                'explanation': None
            }

        return jsonify(response_data),200



if __name__ == '__main__':
    app.run(debug=True)
