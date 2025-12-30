# 🎬 VidFlow Engine

**VidFlow** is a comprehensive video engineering microservice designed to automate and simplify complex media workflows. It serves as a bridge between raw command-line tools and professional editing software, enabling you to remaster legacy footage, create social media shorts, rip audiophile-quality audio, and manage subtitles—all through a single, intuitive interface.

---

## 📂 The Core Processors

Located in `src/processors/`, these modules are the engine's powerhouse. Each operates independently:

* **`editor.py`**
    Handles visual transformations, specifically converting horizontal videos into vertical Shorts (9:16) with dynamic background blurring for platforms like TikTok and Reels.

* **`division.py`**
    Manages structural edits, allowing you to split long videos into 30-second chunks (Status Mode) or cut movies exactly in half at a specific timestamp (Intermission Mode).

* **`remaster.py`**
    A digital restoration engine that denoises, sharpens, color-grades, and upscales old 1970s/80s footage to clear 1080p resolution.

* **`extractor.py`**
    Rips audio tracks from video files in high-fidelity formats, supporting 320kbps MP3, 24-bit WAV, and Lossless FLAC for audiophile-grade output.

* **`tracks.py`**
    Provides surgical control over file streams, allowing you to inspect all audio/subtitle tracks and select exactly which ones to keep or delete (Multi-Select).

* **`formats.py`**
    An intelligent format converter that wraps video streams into new containers (MP4, MKV, AVI, MOV) without unnecessary re-encoding, preserving original quality.

* **`compressor.py`**
    Reduces file size by intelligently optimizing audio bitrates while maintaining the original video stream quality (Lossless Video Pass-through).

* **`stitcher.py`**
    Joins multiple video files together instantly using the "Demuxer Method," which avoids quality loss and long rendering times associated with traditional editing.

* **`merger.py`**
    Automatically scans directories to find and embed matching `.srt` subtitle files into their corresponding video containers.

* **`watermark.py`**
    Burns a logo image or text overlay onto your video at a specific position (e.g., Bottom-Right) for effective branding and copyright protection.

* **`gif_maker.py`**
    Generates crystal-clear, high-definition GIFs using a 2-pass palette generation algorithm to ensure accurate colors and smooth playback.
---

## 🚀 Getting Started

Follow these steps to set up the engine on your local machine.

### 1. Clone the Repository
Start by downloading the codebase to your computer using Git. Open your terminal or command prompt and run:

```bash
git clone https://github.com/hrushikesh8/VIDFlow.git
cd VidFlow-Engine
```

### 2. FFmpeg Setup (Critical)

VidFlow relies on **FFmpeg** for all media processing. If this is not set up correctly, the application will not work.

* **Download:** Visit [ffmpeg.org/download](https://ffmpeg.org/download.html) and download the build release for your operating system.
* **Extract:** Unzip the folder and place it in a permanent location (e.g., `C:\ffmpeg`).
* **Add to PATH (Windows):**
1. Search for "Edit the system environment variables".
2. Click **Environment Variables** -> Select **Path** -> Click **Edit**.
3. Click **New** and paste the path to the `bin` folder inside your FFmpeg directory (e.g., `C:\ffmpeg\bin`).
4. **Important:** Restart your computer for these changes to take effect.



### 3. Install Dependencies

Once inside the project folder, install the required Python libraries:

```bash
pip install -r requirements.txt
```

*(Note: If you encounter issues, ensure you have Python 3.8+ installed).*
---

## 🎮 How to Use

### The Main Dashboard

The easiest way to use VidFlow is through the central dashboard, which guides you through every feature.

1. **Run the script:**
```bash
python main.py
```


2. **Select a Tool:** You will see a menu listing all 13 features. Type the number of the tool you want (e.g., `6` for Auto-Shorts) and press Enter.
3. **Follow the Prompts:** The system will ask for file paths or settings. You can drag and drop your video file into the terminal window to paste the path.

### Standalone Usage

For automation or quick tasks, you can run any processor directly:

**Example: Split a video into 30s chunks**

```bash
python src/processors/division.py "C:\Videos\Status.mp4" "chunk" 30
```

**Example: Extract Audio as MP3**

```bash
python src/processors/extractor.py "C:\Music\Video.mkv" "mp3"
```

---

**Built with 💻 & ☕ by Hrushikesh**