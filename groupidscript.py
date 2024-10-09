from telethon import TelegramClient

# Your API ID and API Hash
api_id = 29902706  # Your API ID
api_hash = '95ee402250b2e50354cacf00f6f09878'  # Your API Hash

# Your Phone Number (include country code, e.g., +1234567890)
phone_number = '+6598953994'  # Replace with your phone number

# Create a new Telegram client using your personal account
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()  # Start the client

    print("Your chats:")
    async for dialog in client.iter_dialogs():
        print(f"Title: {dialog.title}, ID: {dialog.id}")

with client:
    client.loop.run_until_complete(main())
