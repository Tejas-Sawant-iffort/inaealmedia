# from flask import Flask, render_template, jsonify
# import json
# import os

# app = Flask(__name__)

# # Load comic data
# with open("static/comics.json", "r") as f:
#     comics = json.load(f)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/get_comic/<int:index>")
# def get_comic(index):
#     if index < 0 or index >= len(comics):
#         return jsonify({"error": "Invalid comic index"}), 404

#     comic = comics[index]

#     # Load timestamps if available
#     timestamps_file = f"static/audio/{comic['audio'].replace('.mp3', '.json')}"
#     timestamps = []
#     if os.path.exists(timestamps_file):
#         with open(timestamps_file) as f:
#             timestamps = json.load(f)

#     return jsonify({
#         "image": f"static/comics/{comic['image']}",
#         "audio": f"static/audio/{comic['audio']}",
#         "timestamps": timestamps
#     })

# if __name__ == "__main__":
#     app.run(debug=True, port=6005)

from flask import Flask, render_template, jsonify
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
    comics = load_comics()  # Reload comics each time to reflect updates
    if index < 0 or index >= len(comics):
        return jsonify({"error": "Invalid comic index"}), 404

    comic = comics[index]

    # Extract the main image
    image_path = f"static/comics/{comic['image']}"

    # Collect all text-audio pairs dynamically (p1, p2, or direct text/audio fields)
    dialogues = []
    if "p1" in comic:
        for item in comic["p1"]:
            dialogues.append({"text": item["text"], "audio": f"static/audio/{item['audio']}"})
    
    if "p2" in comic:
        for item in comic["p2"]:
            dialogues.append({"text": item["text"], "audio": f"static/audio/{item['audio']}"})

    if "text" in comic and "audio" in comic:
        dialogues.append({"text": comic["text"], "audio": f"static/audio/{comic['audio']}"})

    # Load timestamps for each audio file
    for dialogue in dialogues:
        timestamps_file = dialogue["audio"].replace(".mp3", ".json")
        if os.path.exists(timestamps_file):
            with open(timestamps_file) as f:
                dialogue["timestamps"] = json.load(f)
        else:
            dialogue["timestamps"] = []

    return jsonify({"image": image_path, "dialogues": dialogues})

if __name__ == "__main__":
    app.run(debug=True,host=0.0.0.0 ,port=4000)
