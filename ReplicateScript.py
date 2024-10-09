import asyncio
from telethon import TelegramClient

# Your API ID and API Hash
api_id = 24632603  # Your API ID
api_hash = 'cc1f10b085ba37378bb7476428126b9d'  # Your API Hash

# Your Bot Token
bot_token = '7404382288:AAEbbG_MK-ShnUjC5LZ2gCJx4Q-BQUK4WdQ'  # Replace with your bot token

# Group IDs
source_group_id = -1002161000921  # Source group ID
target_group_id = -1002162731202  # Target group ID

# Create a new Telegram client using your bot
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Set a delay time (in seconds) to avoid rate limits
delay_time = 5  # Adjust this value if you encounter rate limits

async def forward_media():
    try:
        # Get the source and target groups using their IDs
        source_group = await client.get_entity(source_group_id)
        target_group = await client.get_entity(target_group_id)

        # Get messages from the source group
        async for message in client.iter_messages(source_group):
            # Check if the message has media
            if message.media:
                # Forward the media message to the target group
                await client.send_message(target_group, message)

                # Wait to avoid hitting rate limits
                await asyncio.sleep(delay_time)  # Use the defined delay time

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the forward_media function
with client:
    try:
        client.loop.run_until_complete(forward_media())
    except Exception as e:
        print(f"Failed to run the script: {e}")

# Keep the script running to see output
input("Press Enter to exit...")
