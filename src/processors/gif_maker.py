import subprocess
import os
import sys

class GifMaker:
    def create_high_quality_gif(self, input_path: str, output_path: str, start_time: int = 0, duration: int = 5, width: int = 480):
        """
        Converts video to GIF using a 2-pass palette generation for high quality.
        1. Generate color palette from the video segment.
        2. Apply palette to generate the final GIF.
        """
        
        # Filter Explanation:
        # fps=15: Limit frame rate (GIFs don't need 60fps)
        # scale=width:-1: Resize while keeping aspect ratio
        # split[a][b]: Make two copies of the stream
        # [a]palettegen: Analyze colors to make a 256-color palette
        # [b]paletteuse: Use that palette on the second stream
        filter_cmd = f"fps=15,scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"

        command = [
            'ffmpeg', '-ss', str(start_time), '-t', str(duration),
            '-i', input_path,
            '-vf', filter_cmd,
            '-y', output_path
        ]

        try:
            print(f"🎨 Generating High-Quality GIF ({duration}s)...")
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gif_maker.py <video_path> [start_sec] [duration_sec] [width_px]")
        sys.exit(1)

    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    dur = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    width = int(sys.argv[4]) if len(sys.argv) > 4 else 480
    
    maker = GifMaker()
    out = os.path.splitext(path)[0] + ".gif"
    
    if maker.create_high_quality_gif(path, out, start, dur, width):
        print(f"✅ GIF Created: {out}")
    else:
        print("❌ Failed.")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/gif_maker.py <Video> <Start> <Duration> <Width>
#
# Example Command:
# python src/processors/gif_maker.py "FunnyClip.mp4" 10 5 480
#
# (Takes 5 seconds starting at 00:00:10 and makes a 480px wide GIF)