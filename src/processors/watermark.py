import subprocess
import os
import sys

class Watermarker:
    def add_image_watermark(self, video_path: str, image_path: str, output_path: str, position="br"):
        """
        Overlays an image (logo) onto the video.
        position options: 'br' (bottom-right), 'tl' (top-left), 'tr', 'bl', 'center'
        """
        
        # FFmpeg coordinate logic
        coords = {
            "tl": "10:10",                                  # Top-Left
            "tr": "main_w-overlay_w-10:10",                 # Top-Right
            "bl": "10:main_h-overlay_h-10",                 # Bottom-Left
            "br": "main_w-overlay_w-10:main_h-overlay_h-10",# Bottom-Right
            "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
        }
        
        overlay_setting = coords.get(position, coords["br"])

        command = [
            'ffmpeg', '-i', video_path, '-i', image_path,
            '-filter_complex', f"overlay={overlay_setting}",
            '-c:a', 'copy', # Copy audio, re-encode video
            '-y', output_path
        ]

        try:
            print("💧 Burning watermark (this re-encodes the video)...")
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python watermark.py <video_path> <logo_path> <position:tl|tr|bl|br|center>")
        sys.exit(1)

    vid = sys.argv[1]
    img = sys.argv[2]
    pos = sys.argv[3]
    
    out = os.path.splitext(vid)[0] + "_branded.mp4"
    
    wm = Watermarker()
    if wm.add_image_watermark(vid, img, out, pos):
        print(f"✅ Created: {out}")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/watermark.py <Video> <LogoImage> <Position>
#
# Example Command:
# python src/processors/watermark.py "Video.mp4" "Logo.png" "br"
# (Adds logo to Bottom-Right corner)