# Discord Image Uploader

A Python script that uploads all images from a folder to a specified Discord channel.

## Requirements
- Python 3.x
- discord.py (`pip install discord.py`)
- Pillow (`pip install Pillow`)

## Setup
1. Set your bot token as an environment variable: `DISCORD_TOKEN=your_token_here`
2. Update `CHANNEL_ID` with your Discord channel ID
3. Set `IMAGE_FOLDER` to your image directory
4. Run: `python image_uploader.py`

## Features
- Uploads images (.png, .jpg, .jpeg, .gif, .webp)
- Logs image dimensions
- Error handling for failed uploads
