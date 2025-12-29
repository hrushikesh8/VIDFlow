import subprocess
import os
import sys
import math

class VideoEditor:
    def convert_to_shorts_style(self, input_path: str, output_path: str):
        """Converts Landscape to Vertical (9:16) with blur background."""
        filter_cmd = (
            "split[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,boxblur=20:20[bg];"
            "[b]scale=1080:-1[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )
        command = [
            'ffmpeg', '-i', input_path,
            '-vf', filter_cmd,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'copy', '-y', output_path
        ]
        try:
            print("⏳ Processing (this may take time)...")
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False

    def split_by_time(self, input_path: str, segment_time: int):
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.dirname(input_path)
        output_pattern = os.path.join(output_dir, f"{filename}_part%03d.mp4")
        
        command = [
            'ffmpeg', '-i', input_path, '-c', 'copy', '-f', 'segment',
            '-segment_time', str(segment_time), '-reset_timestamps', '1',
            '-y', output_pattern
        ]
        try:
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python editor.py <file> <mode:shorts|split> [seconds]")
        sys.exit(1)

    path = sys.argv[1]
    mode = sys.argv[2]
    editor = VideoEditor()

    if mode == "shorts":
        out = os.path.splitext(path)[0] + "_shorts.mp4"
        if editor.convert_to_shorts_style(path, out):
            print(f"✅ Created: {out}")
            
    elif mode == "split":
        if len(sys.argv) < 4:
            print("❌ Split mode requires seconds argument.")
        else:
            sec = int(sys.argv[3])
            if editor.split_by_time(path, sec):
                print("✅ Split complete.")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Option 1: Create Vertical Short
# python src/processors/editor.py "C:\Videos\Movie.mp4" "shorts"
#
# Option 2: Split Video into 30s chunks
# python src/processors/editor.py "C:\Videos\Movie.mp4" "split" "30"