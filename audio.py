import whisper
import json
import os
from pathlib import Path

# Directory where your MP3 files are stored
AUDIO_DIR = "static/audio/"

def generate_timestamps(mp3_file):
    """
    Generate word-level timestamps for an MP3 file using Whisper and save them as JSON.
    
    Args:
        mp3_file (str): Path to the MP3 file (e.g., 'static/audio/1_en.mp3')
    """
    try:
        # Load Whisper model (use 'base' for speed, or 'small'/'medium' for better accuracy)
        model = whisper.load_model("base")
        
        # Transcribe the audio with word-level timestamps
        print(f"Processing {mp3_file}...")
        result = model.transcribe(mp3_file, word_timestamps=True)
        
        # Extract timestamps from the first segment's words
        # (Assuming each MP3 corresponds to one dialogue line)
        if not result["segments"]:
            raise ValueError("No segments found in the audio transcription.")
        
        timestamps = [
            {"word": segment["word"], "start": segment["start"], "end": segment["end"]}
            for segment in result["segments"][0]["words"]
        ]
        
        # Define output JSON file name (e.g., '1_en.mp3.json')
        json_file = mp3_file + ".json"
        
        # Save timestamps to JSON file
        with open(json_file, "w") as f:
            json.dump(timestamps, f, indent=4)
        
        print(f"Saved timestamps to {json_file}")
        
    except FileNotFoundError:
        print(f"Error: {mp3_file} not found.")
    except Exception as e:
        print(f"Error processing {mp3_file}: {str(e)}")

def process_all_audio_files():
    """
    Process all MP3 files in the AUDIO_DIR and generate timestamp JSON files.
    """
    # Ensure the audio directory exists
    if not os.path.exists(AUDIO_DIR):
        print(f"Error: Directory {AUDIO_DIR} does not exist.")
        return
    
    # Find all MP3 files in the directory
    mp3_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
    
    if not mp3_files:
        print(f"No MP3 files found in {AUDIO_DIR}.")
        return
    
    # Process each MP3 file
    for mp3_file in mp3_files:
        full_path = os.path.join(AUDIO_DIR, mp3_file)
        generate_timestamps(full_path)

if __name__ == "__main__":
    # Run the script to process all MP3 files
    print("Starting timestamp generation for all MP3 files...")
    process_all_audio_files()
    print("Done!")