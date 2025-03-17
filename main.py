from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Load comic data
COMICS_FILE = "static/comics.json"

def load_comics():
    """Load the latest comic data from JSON file."""
    with open(COMICS_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_comic/<int:index>")
def get_comic(index):
    # Get the selected language from query parameters (default to English if not provided)
    lang = request.args.get("lang", "en")  # Default language is 'en' (English)

    comics = load_comics()  # Reload comics each time to reflect updates
    if index < 0 or index >= len(comics):
        return jsonify({"error": "Invalid comic index"}), 404

    comic = comics[index]

    # Extract the main image based on the selected language
    image_path = f"static/comics/{comic['image'][lang]}"

    # Collect all text-audio pairs dynamically (p1, p2, or direct text/audio fields)
    dialogues = []
    if "p1" in comic:
        for item in comic["p1"]:
            dialogues.append({
                "text": item["text"][lang],
                "audio": f"static/audio/{item['audio'][lang]}"
            })
    
    if "p2" in comic:
        for item in comic["p2"]:
            dialogues.append({
                "text": item["text"][lang],
                "audio": f"static/audio/{item['audio'][lang]}"
            })

    if "text" in comic and "audio" in comic:
        dialogues.append({
            "text": comic["text"][lang],
            "audio": f"static/audio/{comic['audio'][lang]}"
        })

    # Load timestamps for each audio file
    for dialogue in dialogues:
        timestamps_file = dialogue["audio"].replace(".mp3", ".json")
        if os.path.exists(timestamps_file):
            with open(timestamps_file) as f:
                dialogue["timestamps"] = json.load(f)
        else:
            dialogue["timestamps"] = []

    return jsonify({"image": image_path, "dialogues": dialogues})

@app.route("/get_comic_count")
def get_comic_count():
    """Return the total number of comics."""
    comics = load_comics()
    return jsonify({"count": len(comics)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)