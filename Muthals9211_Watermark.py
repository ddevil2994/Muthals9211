import asyncio
from telethon import TelegramClient, events
from PIL import Image, ImageDraw, ImageFont
import os

# Telegram API credentials (replace with your own)
api_id = '29902706'
api_hash = '95ee402250b2e50354cacf00f6f09878'
bot_token = '7881083084:AAEz7Q5EKFcW9K3XrySZQBZrPb6M8eD4vDA'

# Create Telegram client
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Target group ID where the watermarked images will be sent
target_group_id = -1002343181050  # Your target group ID

# Function to add watermark to the image
def add_watermark(input_image, watermark_text):
    # Open the original image
    image = Image.open(input_image).convert("RGBA")
    
    # Create a new blank image with transparent background
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    
    # Choose font and size
    font_size = 36
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Load a TrueType font
    except IOError:
        font = ImageFont.load_default()  # Load default font if specific font fails
    
    # Calculate text size using an alternative method
    text_size = draw.textbbox((0, 0), watermark_text, font=font)
    textwidth = text_size[2] - text_size[0]
    textheight = text_size[3] - text_size[1]
    
    width, height = image.size
    
    # Position the watermark at the bottom-left corner
    x = 10  # 10 pixels from the left
    y = height - textheight - 10  # 10 pixels from the bottom
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
    
    # Create a new image with the watermark
    watermarked_image = Image.alpha_composite(image, txt)
    watermarked_image = watermarked_image.convert("RGB")  # Convert back to RGB mode
    output_path = f"watermarked_{os.path.basename(input_image)}"
    watermarked_image.save(output_path)
    
    return output_path

# Handle incoming media
@client.on(events.NewMessage())
async def handle_media(event):
    # Log the chat ID where the message was received
    print(f"Received message in chat ID: {event.chat_id}")
    
    # Check if the message contains media
    if event.message.media and event.message.file.mime_type.startswith('image/'):
        # Download the image
        file_path = await client.download_media(event.message, file='temp_image')
        
        # Add watermark to the image
        watermarked_image_path = add_watermark(file_path, "Muthals9211")
        
        # Send the watermarked image to the target group
        await client.send_file(target_group_id, watermarked_image_path)
        
        # Clean up the temporary image files
        os.remove(file_path)
        os.remove(watermarked_image_path)

# Run the client
client.start()
client.run_until_disconnected()
