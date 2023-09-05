import boto3
import os
import uuid
import tempfile
from flask import Flask, request, redirect, url_for, render_template
import requests

from extract_times import extract_times
from search_keywords import search_keywords 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = search_keywords(keyword)
        return render_template('results.html', keyword=keyword, results=results)
    else:
        return render_template('search.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(suffix=filename, delete=False) as f:
            file.save(f)
            filepath = f.name

        s3 = boto3.client('s3', region_name='ap-northeast-2')
        s3.upload_file(filepath, 'graduate1', filename)

        transcribe = boto3.client('transcribe', region_name='ap-northeast-2')
        transcribe.start_transcription_job(
            TranscriptionJobName=filename,
            Media={'MediaFileUri': f"s3://graduate1/{filename}"},
            MediaFormat=os.path.splitext(filename)[1][1:],
            LanguageCode='ko-KR'
        )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=filename)
        
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
            
    print(status)


    transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    response = requests.get(transcript_url)

    download_path = os.path.join('D:/nlp_stt/aws_json/', filename.replace(".mp4", ".json"))
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, 'wb') as f:
        f.write(response.content)

    print(f"Downloaded transcription result to {download_path}")
    extract_times()

    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)

    """
    print(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])

    path = status['TranscriptionJob']['Transcript']['TranscriptFileUri'].replace("https://s3.ap-northeast-2.amazonaws.com/", "")
    bucket, key = path.split("/", 1)

    # Download the transcript file to a local directory (e.g., './downloads/')
    download_path = os.path.join('D:/nlp_stt/aws_json/', key)
    
     # Create directory if not exist.
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    s3.download_file(bucket, key, download_path)
    
    print(f"Downloaded transcription result to {download_path}")
    




    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
"""
