import subprocess
import os
import sys
from pathlib import Path

class AudioExtractor:
    def extract_audio(self, input_path: str, output_format: str = "mp3"):
        """
        Extracts audio track from video.
        output_format: 'mp3', 'wav', 'aac', or 'original' (copy stream).
        """
        filename = Path(input_path).stem
        output_folder = os.path.dirname(input_path)
        
        # Determine output extension
        ext = output_format if output_format != "original" else "aac"
        output_path = os.path.join(output_folder, f"{filename}.{ext}")

        # Base command: Input file + Disable Video (-vn)
        command = ['ffmpeg', '-i', input_path, '-vn']

        if output_format == "original":
            # Stream Copy (Instant, no quality loss)
            command.extend(['-c:a', 'copy'])
        elif output_format == "mp3":
            # High Quality MP3
            command.extend(['-c:a', 'libmp3lame', '-q:a', '2'])
        elif output_format == "wav":
            # Uncompressed Audio
            command.extend(['-c:a', 'pcm_s16le'])
        else:
            # Generic re-encode for other formats
            command.extend(['-c:a', 'aac'])

        command.extend(['-y', output_path])

        try:
            print(f"🎵 Extracting Audio ({output_format})...")
            subprocess.run(command, check=True, capture_output=True)
            return True, output_path
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False, None

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <video_file> [format:mp3|wav|original]")
        sys.exit(1)

    path = sys.argv[1]
    fmt = sys.argv[2] if len(sys.argv) > 2 else "mp3"
    
    extractor = AudioExtractor()
    success, out = extractor.extract_audio(path, fmt)
    
    if success:
        print(f"✅ Extracted: {out}")

# ==========================================
# HOW TO USE THIS CODE
# ==========================================
#
# Syntax: python src/processors/extractor.py <VideoPath> <Format>
#
# Example 1 (Convert to MP3):
# python src/processors/extractor.py "MusicVideo.mp4" "mp3"
#
# Example 2 (Instant Extraction/Copy):
# python src/processors/extractor.py "MusicVideo.mp4" "original"