"""
비디오 파일을 업로드 할 수 있음. 
키워드 검색을 요청할 수 있음. 
검색 결과에 따라 비디오 클립을 생성하고 다운로드할 수 있음. 
"""
import boto3
import os
import uuid
import tempfile
from flask import Flask, request, redirect, url_for, render_template, send_file, session
import requests

from extract_times import extract_times
from search_keywords import search_keywords 
from clip_video import create_summary

app = Flask(__name__)
app.secret_key = 'kyungmin'


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = search_keywords(keyword)
        summary_filename = create_summary(keyword)

        return render_template('results.html', keyword=keyword, results=results, summary_filename=summary_filename)
    else:
        return render_template('search.html')
    
@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        keyword = request.form['keyword']
        create_summary(keyword)

        return send_file("summary.mp4", as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(suffix=filename, delete=False) as f:
            file.save(f)
            filepath = f.name

        session['video_filepath'] = filepath

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