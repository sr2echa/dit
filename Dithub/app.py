from flask import Flask, request, jsonify, send_file, render_template
import os
import zipfile, pickle,zlib

app = Flask(__name__, template_folder='./templates')

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


@app.route('/render/<path:filename>', methods=['GET'])
def render(filename):
    '''Returns the history of the database'''

    #check if a folder with "recieved_filename" exists
    if not os.path.exists(f'received_{filename}'):
        return jsonify({'error': 'Database not found'}), 404
    
    history = pickle.load(open(f'received_{filename}' + r"\past.lore", "rb"))
    history = history[::-1]

    logs = []

    for hash in history:
        compressed_data = open(f'received_{filename}'+ r"\{}.rarc".format(hash), 'rb').read()
        pickled_data = zlib.decompress(compressed_data)
        unpickled_data = pickle.loads(pickled_data)
        logs.append([unpickled_data[0], hash])
    
    data = {"dummy": logs}
    return render_template('commit_v.html', data=data, length=len(logs))




if __name__ == '__main__':
    app.run(debug=True)
