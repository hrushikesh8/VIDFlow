import subprocess
import json
import os
import sys
from typing import List

class TrackProcessor:
    def get_track_info(self, input_path: str, stream_type: str = 'a') -> list:
        """Returns a list of tracks for the given type ('a' or 's')."""
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'stream=index:stream_tags=language,title',
            '-select_streams', stream_type,
            '-of', 'json',
            input_path
        ]
        try:
            output = subprocess.check_output(cmd)
            data = json.loads(output)
            return data.get('streams', [])
        except Exception as e:
            print(f"Error reading tracks: {e}")
            return []

    def keep_multiple_tracks(self, input_path: str, output_path: str, track_indices: List[int], stream_type: str = 'a'):
        """Removes all tracks of 'stream_type' EXCEPT the ones in 'track_indices'."""
        command = ['ffmpeg', '-i', input_path, '-map', '0']
        command.extend(['-map', f'-0:{stream_type}']) # Deselect all
        
        for idx in track_indices:
            command.extend(['-map', f'0:{stream_type}:{idx}']) # Add back selected

        command.extend(['-c', 'copy', '-y', output_path])
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Error: {e.stderr.decode()}")
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    # Args: Script, InputPath, StreamType(a/s), Indices(comma-separated)
    if len(sys.argv) < 4:
        print("❌ Error: Missing arguments.")
        print("Usage: python tracks.py <input_file> <type:a|s> <keep_indexes:0,1>")
        sys.exit(1)

    input_path = sys.argv[1]
    stream_type = sys.argv[2]
    indices_str = sys.argv[3]
    
    # Generate Output Filename
    filename, ext = os.path.splitext(input_path)
    label = "audio" if stream_type == 'a' else "subs"
    output_path = f"{filename}_clean_{label}{ext}"

    try:
        indices = [int(x) for x in indices_str.split(',')]
        processor = TrackProcessor()
        print(f"Processing: {os.path.basename(input_path)}...")
        
        if processor.keep_multiple_tracks(input_path, output_path, indices, stream_type):
            print(f"✅ Success! Saved to: {output_path}")
        else:
            print("❌ Failed.")
    except Exception as e:
        print(f"❌ Error: {e}")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/tracks.py <VideoPath> <Mode> <TrackIDs>
#
# Mode: 'a' for Audio, 's' for Subtitles
# TrackIDs: The index numbers of tracks to KEEP (separated by comma)
#
# Example Command:
# python src/processors/tracks.py "C:\Movies\Avatar.mkv" "a" "0,2"
#
# (This keeps Audio Track 0 and 2, removes the rest)