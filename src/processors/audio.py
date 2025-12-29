import subprocess
import json
import os

class AudioProcessor:
    def get_track_info(self, input_path: str) -> list:
        """
        Returns a list of audio tracks found in the video using ffprobe.
        """
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'stream=index:stream_tags=language,title',
            '-select_streams', 'a',
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

    def keep_single_track(self, input_path: str, output_path: str, track_index: int):
        """
        Removes all audio tracks except the specific 'track_index' chosen.
        """
        try:
            # ffmpeg -i video.mp4 -map 0 -map -0:a -map 0:a:INDEX -c copy out.mp4
            command = [
                'ffmpeg', '-i', input_path,
                '-map', '0',               # Select everything
                '-map', '-0:a',            # Deselect all audio
                '-map', f'0:a:{track_index}', # Add back ONLY the chosen audio
                '-c', 'copy',              # No re-encoding (Fast)
                '-y', output_path
            ]
            
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False