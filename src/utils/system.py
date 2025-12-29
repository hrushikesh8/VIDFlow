import shutil

class SystemUtils:
    @staticmethod
    def check_ffmpeg_availability() -> bool:
        """Verifies if FFmpeg is installed and accessible."""
        return shutil.which("ffmpeg") is not None