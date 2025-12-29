import subprocess
import os
import sys
import math

class VideoDivider:
    def split_by_chunks(self, input_path: str, segment_time: int):
        """
        Splits video into multiple chunks of X seconds (e.g., for WhatsApp Status).
        """
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_pattern = os.path.join(os.path.dirname(input_path), f"{filename}_part%03d.mp4")
        
        command = [
            'ffmpeg', '-i', input_path, 
            '-c', 'copy', 
            '-f', 'segment', 
            '-segment_time', str(segment_time), 
            '-reset_timestamps', '1', 
            '-y', output_pattern
        ]
        
        try:
            print(f"✂️  Dividing into {segment_time}s chunks...")
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False

    def split_at_intermission(self, input_path: str, split_time: float):
        """
        Splits a video into exactly two parts at the specified timestamp.
        """
        base_name, ext = os.path.splitext(os.path.basename(input_path))
        output_dir = os.path.dirname(input_path)
        
        out1 = os.path.join(output_dir, f"{base_name}_First_Half{ext}")
        out2 = os.path.join(output_dir, f"{base_name}_Second_Half{ext}")

        try:
            print(f"✂️  Creating Part 1 (Start -> {split_time}s)...")
            cmd1 = ['ffmpeg', '-i', input_path, '-to', str(split_time), '-c', 'copy', '-y', out1]
            subprocess.run(cmd1, check=True, capture_output=True)

            print(f"✂️  Creating Part 2 ({split_time}s -> End)...")
            cmd2 = ['ffmpeg', '-ss', str(split_time), '-i', input_path, '-c', 'copy', '-y', out2]
            subprocess.run(cmd2, check=True, capture_output=True)
            
            return True, out1, out2
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False, None, None

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Error: Missing arguments.")
        print("Usage: python division.py <file> <mode:chunk|cut> [args]")
        sys.exit(1)

    path = sys.argv[1]
    mode = sys.argv[2]
    divider = VideoDivider()

    if mode == "chunk":
        sec = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        if divider.split_by_chunks(path, sec):
            print("✅ Chunk division complete.")

    elif mode == "cut":
        # Default to 3600s (1 hour) if not specified
        time_point = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
        success, p1, p2 = divider.split_at_intermission(path, time_point)
        if success:
            print(f"✅ Cut Complete:\n   Part 1: {p1}\n   Part 2: {p2}")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Option 1: Split into Chunks (e.g., for WhatsApp Status)
# Syntax: python src/processors/division.py <VideoPath> "chunk" <Seconds>
# Example: python src/processors/division.py "Movie.mp4" "chunk" 30
#
# Option 2: Split Movie at Specific Time (Intermission)
# Syntax: python src/processors/division.py <VideoPath> "cut" <SplitTimeSeconds>
# Example: python src/processors/division.py "Movie.mp4" "cut" 3600
# (Splits the movie into Part 1 and Part 2 exactly at the 1-hour mark)