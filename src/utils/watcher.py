import time
import os
import sys
import shutil
# Note: When running standalone, you might need to adjust imports or run via module
# For simplicity in this structure, we assume running from root via -m
try:
    from src.processors.compressor import VideoCompressor
except ImportError:
    # Fallback for direct execution if paths aren't set
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from src.processors.compressor import VideoCompressor

class FolderWatcher:
    def __init__(self, watch_folder, output_folder):
        self.watch_folder = watch_folder
        self.output_folder = output_folder
        self.compressor = VideoCompressor()
        os.makedirs(watch_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

    def start(self):
        print(f"👀 Watching: {self.watch_folder}")
        try:
            while True:
                files = [f for f in os.listdir(self.watch_folder) if f.lower().endswith(('.mp4', '.mkv', '.mov'))]
                for f in files:
                    input_path = os.path.join(self.watch_folder, f)
                    time.sleep(1) # Wait for copy
                    print(f"⚡ Processing: {f}")
                    output_path = os.path.join(self.output_folder, f)
                    if self.compressor.compress_audio_maintain_video(input_path, output_path):
                        print(f"✅ Done.")
                        os.remove(input_path)
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopped.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python watcher.py <watch_folder> <output_folder>")
    else:
        FolderWatcher(sys.argv[1], sys.argv[2]).start()