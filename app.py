from flask import Flask, request, render_template, send_file, redirect, url_for
import yt_dlp
import os
import tempfile

app = Flask(__name__)

# 임시 파일을 저장할 폴더
DOWNLOAD_FOLDER = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
    if not video_url:
        return "Please enter a URL.", 400
    
    try:
        # 다운로드 옵션 설정
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        # yt-dlp로 영상 다운로드
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        
        # 다운로드 완료 페이지로 리디렉션하면서 파일명 전달
        filename = os.path.basename(file_path)
        return redirect(url_for('download_complete', filename=filename))
    except Exception as e:
        return f"Download failed: {e}", 500

@app.route('/download_complete/<filename>')
def download_complete(filename):
    # 파일명과 다운로드 링크를 표시하는 페이지 렌더링
    return render_template('download_complete.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    # 사용자에게 파일 다운로드 링크 제공
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)