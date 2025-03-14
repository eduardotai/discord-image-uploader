import discord
import os
from discord.ext import commands
import asyncio
from PIL import Image  # For checking image dimensions

# Bot configuration - To be set by the user
TOKEN = os.getenv('DISCORD_TOKEN')  # Set this via environment variable
CHANNEL_ID = None  # Replace with your Discord channel ID
IMAGE_FOLDER = None  # Replace with your image folder path

# Supported image extensions
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event handler triggered when the bot successfully connects to Discord."""
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} guilds')
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    print('------')

    # Validate configuration
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set")
        await bot.close()
        return
    if not CHANNEL_ID:
        print("Error: CHANNEL_ID not set in script")
        await bot.close()
        return
    if not IMAGE_FOLDER or not os.path.isdir(IMAGE_FOLDER):
        print("Error: IMAGE_FOLDER not set or invalid directory")
        await bot.close()
        return

    # Get the target channel
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")
        await bot.close()
        return

    print(f"Connected to channel: {channel.name} in guild: {channel.guild.name}")

    try:
        # Find all valid image files in the folder
        image_files = [f for f in os.listdir(IMAGE_FOLDER) 
                      if f.lower().endswith(VALID_EXTENSIONS)]
        
        if not image_files:
            print("No images found in the specified folder")
            await channel.send("No images found in the specified folder")
            await bot.close()
            return

        print(f"Found {len(image_files)} images to send")

        # Upload each image
        for image_file in image_files:
            file_path = os.path.join(IMAGE_FOLDER, image_file)
            try:
                # Log image dimensions
                with Image.open(file_path) as img:
                    width, height = img.size
                    print(f"{image_file} dimensions: {width}x{height} pixels")
                
                # Send the image to Discord
                with open(file_path, 'rb') as f:
                    picture = discord.File(f)
                    await channel.send(file=picture)
                print(f"Sent {image_file}")
                await asyncio.sleep(1)  # Prevent rate limiting
            except Exception as e:
                print(f"Error processing/sending {image_file}: {str(e)}")
                await channel.send(f"Error sending {image_file}: {str(e)}")

        print("Finished sending all images")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await channel.send(f"An error occurred: {str(e)}")
    
    finally:
        await bot.close()

def main():
    """Main function to run the bot."""
    bot.run(TOKEN)

if __name__ == "__main__":
    main()