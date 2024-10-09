import asyncio
from telethon import TelegramClient

# Your API ID and API Hash
api_id = 24632603  # Your API ID
api_hash = 'cc1f10b085ba37378bb7476428126b9d'  # Your API Hash

# Phone number (replace with your actual number with country code, e.g., +123456789)
phone_number = '+66994951744'

# Group IDs
source_group_id = -1002161000921  # Source group ID
target_group_id = -1002162731202  # Target group ID

# Create a new Telegram client using your user account
client = TelegramClient('user_session', api_id, api_hash)

# Set a delay time for forwarding (in seconds)
forward_delay = 1  # 1 second delay between each message
batch_size = 1500  # Number of forwards before taking a break
break_time = 15 * 60  # 15 minutes break in seconds (15 * 60)

async def forward_media():
    try:
        # Log in using your phone number if necessary
        await client.start(phone=phone_number)

        # Get the source and target groups using their IDs
        source_group = await client.get_entity(source_group_id)
        target_group = await client.get_entity(target_group_id)

        # Counter to track the number of forwarded messages
        forward_count = 0

        # Get messages from the source group
        async for message in client.iter_messages(source_group):
            if message.media:  # Check if the message has media
                # Forward the media message to the target group
                await client.send_message(target_group, message)
                
                forward_count += 1  # Increment the forward count
                print(f"Message {forward_count} forwarded")

                # Wait for 1 second between each forward
                await asyncio.sleep(forward_delay)

                # If 1500 messages have been forwarded, take a 15-minute break
                if forward_count % batch_size == 0:
                    print(f"Taking a 15-minute break after {forward_count} forwards.")
                    await asyncio.sleep(break_time)
                    print("Resuming forwarding...")

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
