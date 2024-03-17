from flask import Flask, request, jsonify, send_file
import os
import zipfile

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    file_name = file.filename[2:].split('.')[0]
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file.save(file_name+".zip")
    
    destination_folder = f'received_{file_name}'
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    destination_folder = os.path.abspath(destination_folder)
    
    with zipfile.ZipFile(file_name+".zip", 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    
    return jsonify({'message': 'File uploaded and extracted successfully'}), 200

@app.route('/download', methods=['GET'])
def download():
    zip_file_name = request.args.get('filename', 'example.zip')
    zip_file_path = os.path.join('./', zip_file_name)
    
    if os.path.exists(zip_file_path):
        return send_file(zip_file_path, as_attachment=True)
    else:
        return "Zip file not found", 404

if __name__ == '__main__':
    app.run(debug=True)
