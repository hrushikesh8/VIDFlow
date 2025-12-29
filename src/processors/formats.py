import os
import subprocess
import sys
from pathlib import Path

class FormatMapper:
    def convert_video(self, input_path: str, output_folder: str, target_format: str) -> dict:
        filename = Path(input_path).stem
        output_path = os.path.join(output_folder, f"{filename}.{target_format}")
        
        if target_format == 'mkv':
            cmd_flags = ['-map', '0', '-c', 'copy']
        elif target_format == 'mp4':
            cmd_flags = ['-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text']
        else:
            cmd_flags = ['-c', 'copy']

        command = ['ffmpeg', '-i', input_path, *cmd_flags, '-y', output_path]
        try:
            subprocess.run(command, check=True, capture_output=True)
            return {"status": "success", "output_path": output_path}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python formats.py <input_file> <format>")
    else:
        print(FormatMapper().convert_video(sys.argv[1], os.path.dirname(sys.argv[1]), sys.argv[2]))