from flask import Flask, render_template, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/stream/<file_id>')
def stream_audio(file_id):
    drive_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    session = requests.Session()
    req = session.get(drive_url, stream=True)
    
    for k, v in req.cookies.items():
        if k.startswith('download_warning'):
            drive_url += f'&confirm={v}'
            req = session.get(drive_url, stream=True)
            break

    def generate():
        for chunk in req.iter_content(chunk_size=1024 * 8):
            if chunk:
                yield chunk

    return Response(generate(), content_type=req.headers.get('Content-Type', 'image/jpeg'))

if __name__ == '__main__':
    # host='0.0.0.0' allows connections from phones on the same Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)