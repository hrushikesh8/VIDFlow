import subprocess
import os
import sys

class VideoStitcher:
    def concat_videos(self, video_list: list, output_path: str):
        """
        Joins multiple video files into one using the FFmpeg 'concat demuxer'.
        Requirements: All videos must have the same codec/resolution.
        """
        if not video_list:
            return False

        # 1. Create a temporary text file listing all videos
        # Format: file 'path/to/video.mp4'
        list_file_path = "temp_stitch_list.txt"
        with open(list_file_path, "w", encoding='utf-8') as f:
            for vid in video_list:
                # FFmpeg requires paths to be escaped strictly
                safe_path = vid.replace("'", "'\\''") 
                f.write(f"file '{safe_path}'\n")

        # 2. Run FFmpeg concat command
        # -f concat: Use the concat format
        # -safe 0: Allow unsafe file paths (absolute paths)
        # -c copy: No re-encoding (Instant join)
        command = [
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', list_file_path,
            '-c', 'copy', '-y', output_path
        ]

        try:
            print(f"🔗 Stitching {len(video_list)} files...")
            subprocess.run(command, check=True, capture_output=True)
            
            # Cleanup temp file
            os.remove(list_file_path)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            if os.path.exists(list_file_path):
                os.remove(list_file_path)
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    # Usage: python stitcher.py output.mp4 video1.mp4 video2.mp4 video3.mp4 ...
    if len(sys.argv) < 3:
        print("Usage: python stitcher.py <output_file> <input_video_1> <input_video_2> ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_videos = sys.argv[2:]

    stitcher = VideoStitcher()
    if stitcher.concat_videos(input_videos, output_file):
        print(f"✅ Successfully stitched into: {output_file}")
    else:
        print("❌ Failed to stitch videos. Ensure they have matching formats.")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/stitcher.py <Output> <Input1> <Input2> ...
#
# Example Command:
# python src/processors/stitcher.py "FullMovie.mp4" "Part1.mp4" "Part2.mp4"