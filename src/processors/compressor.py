import subprocess
import os
import sys

class VideoCompressor:
    def compress_audio_maintain_video(self, input_path: str, output_path: str, bitrate="384k") -> bool:
        command = [
            'ffmpeg', '-i', input_path,
            '-map', '0', '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', bitrate,
            '-c:s', 'copy', '-y', output_path
        ]
        try:
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compressor.py <input_file> [bitrate]")
        sys.exit(1)

    path = sys.argv[1]
    bitrate = sys.argv[2] if len(sys.argv) > 2 else "128k"
    
    out = os.path.splitext(path)[0] + "_compressed.mkv"
    comp = VideoCompressor()
    
    print(f"Compressing audio to {bitrate}...")
    if comp.compress_audio_maintain_video(path, out, bitrate):
        print(f"✅ Finished: {out}")
    else:
        print("❌ Failed.")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/compressor.py <VideoPath> <AudioBitrate>
#
# Example Command:
# python src/processors/compressor.py "C:\Videos\HeavyFile.mkv" "128k"
#
# (This copies the video exactly but shrinks the audio to 128 kbps AAC)