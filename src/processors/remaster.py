import subprocess
import os
import sys

class VideoRemaster:
    def enhance_old_footage(self, input_path: str, output_path: str):
        """
        Applies a restoration chain to improve old footage:
        1. HQDN3D: High Quality Denoise (removes grain).
        2. Unsharp: Sharpens edges.
        3. EQ: Boosts contrast and saturation (fixes faded colors).
        4. Scale: Upscales to 1080p using Lanczos algorithm.
        """
        
        # Professional Filter Chain Explanation:
        # hqdn3d=1.5:1.5:6:6       -> Denoise (spatial/temporal). Values tuned for film grain.
        # unsharp=5:5:1.0:5:5:0.0  -> Sharpening matrix.
        # eq=saturation=1.2:contrast=1.1 -> Boost color/contrast by 10-20%.
        # scale=1920:-2:flags=lanczos -> Upscale to 1080p width, keep aspect ratio.
        
        filter_chain = (
            "hqdn3d=1.5:1.5:6:6,"
            "unsharp=5:5:1.0:5:5:0.0,"
            "eq=saturation=1.2:contrast=1.1,"
            "scale=1920:-2:flags=lanczos"
        )

        command = [
            'ffmpeg', '-i', input_path,
            '-vf', filter_chain,
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', # High quality encoding
            '-c:a', 'copy', # Keep original audio
            '-y', output_path
        ]

        try:
            print(f"✨ Remastering (Denoise -> Sharpen -> Color -> Upscale)...")
            print("⚠️  This process is CPU intensive. Please wait.")
            subprocess.run(command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")
            return False

# --- STANDALONE EXECUTION LOGIC ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remaster.py <old_movie_path>")
        sys.exit(1)

    path = sys.argv[1]
    out = os.path.splitext(path)[0] + "_remastered_1080p.mp4"
    
    engine = VideoRemaster()
    if engine.enhance_old_footage(path, out):
        print(f"✅ Remaster Complete: {out}")
    else:
        print("❌ Failed.")

# ==========================================
# HOW TO USE THIS CODE (EXAMPLE)
# ==========================================
#
# Syntax: python src/processors/remaster.py <VideoPath>
#
# Example:
# python src/processors/remaster.py "OldWedding_1985.avi"
#
# Result: Converts a grainy 480p file into a clean, sharp 1080p MP4.