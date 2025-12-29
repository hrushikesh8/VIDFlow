import subprocess
import os

class StreamMerger:
    def merge_video_audio(self, video_path: str, audio_path: str, output_path: str):
        """Replaces or adds audio to a video file."""
        command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-map', '0:v:0', # Take video from file 0
            '-map', '1:a:0', # Take audio from file 1
            '-y', output_path
        ]
        subprocess.run(command, check=True)

    def mux_subtitles(self, video_path: str, sub_path: str, output_path: str):
        """Embeds a subtitle file into the video container (Soft subs)."""
        command = [
            'ffmpeg', '-i', video_path, '-i', sub_path,
            '-map', '0', '-map', '1',
            '-c', 'copy',
            '-y', output_path
        ]
        subprocess.run(command, check=True)