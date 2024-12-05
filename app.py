from flask import Flask, request, render_template, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_transcript", methods=["POST"])
def get_transcript():
    video_id = request.form.get("video_id")
    language = request.form.get("language")

    try:
        # Fetch transcript in the specified language
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Format transcript as plain text
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)

        # Save transcript to a file
        filename = f"{video_id}_transcript_{language}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcript_text)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Fehler: {e}", 400

    finally:
        # Clean up the file after sending it
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(debug=True)
