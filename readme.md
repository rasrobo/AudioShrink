# AudioShrink

A dynamic audio compression workflow for n8n that automatically compresses audio files to stay below a specified file size (default < 200MB).

## Overview

AudioShrink is a powerful audio compression workflow that:

- Automatically calculates the optimal bitrate for your audio files
- Ensures output files stay below your target size (default 200MB)
- Works with various input formats (m4a, wav, mp3, etc.)
- Compresses to MP3 format with dynamically selected bitrate
- Provides detailed compression summary

## Requirements

- n8n workflow engine installed locally
- Python 3.6+
- pydub, mutagen, and other required packages

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rasrobo/AudioShrink.git
   cd AudioShrink
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv ~/AudioShrink_venv
   source ~/AudioShrink_venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg (required by pydub):
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install ffmpeg
   ```
   
   **macOS (with Homebrew):**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Setting up the n8n Workflow

1. Start your local n8n instance
2. Go to Workflows > Import From File
3. Select the `AudioShrink_workflow.json` file from this repository
4. Update the paths in the "Set Input Parameters" node to match your environment

## Running the Python Script Standalone

The Python script can also be used independently of n8n:

```bash
source ~/AudioShrink_venv/bin/activate
python compress_audio.py input_file.m4a [output_file.mp3] [target_size_mb]
```

### Arguments

- `input_file.m4a`: Path to the input audio file
- `output_file.mp3`: (Optional) Path where the compressed file will be saved. If not specified, uses the same name and location as the input file but with .mp3 extension
- `target_size_mb`: (Optional) Target file size in MB (default: 199)

## Example

```bash
# Specify output filename and target size
python compress_audio.py large_podcast.m4a compressed_podcast.mp3 180

# Use default output name (large_podcast.mp3) and default target size (199MB)
python compress_audio.py large_podcast.m4a

# Use default output name but specify target size
python compress_audio.py large_podcast.m4a 180
```

These examples show how to compress `large_podcast.m4a` with different options for output naming and target sizes.

## How It Works

1. The workflow analyzes the input audio file to determine its duration
2. Based on file size and duration, it calculates the optimal bitrate
3. The Python script compresses the audio using the calculated bitrate
4. The workflow provides a detailed compression summary

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Donations

If you find this software useful and would like to support its development, you can buy me a coffee! Your support is greatly appreciated.

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://buymeacoffee.com/robodigitalis)
