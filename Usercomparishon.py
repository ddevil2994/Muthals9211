from telethon.sync import TelegramClient

# Your API ID and Hash from https://my.telegram.org
api_id = 24632603
api_hash = 'cc1f10b085ba37378bb7476428126b9d'
phone_number = '+66994951744'  # Your phone number with the country code

# Group IDs
group_1 = -1002200406757  # ftvpaidchat (base group)
group_2 = -1002161000921  # ftvpremium (comparison group)

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Fetch members from a group
async def get_group_members(group):
    participants = await client.get_participants(group)
    return participants  # Return all participant objects, not just IDs

# Compare members: Find users in ftvpremium not in ftvpaidchat
async def compare_groups():
    await client.start(phone=phone_number)

    # Get members from both groups
    ftvpaidchat_members = await get_group_members(group_1)
    ftvpremium_members = await get_group_members(group_2)

    # Convert the paid chat members to a set of user IDs for comparison
    ftvpaidchat_member_ids = set(participant.id for participant in ftvpaidchat_members)

    # Find members in ftvpremium but not in ftvpaidchat
    premium_not_in_paidchat = [member for member in ftvpremium_members if member.id not in ftvpaidchat_member_ids]

    # Display results with user details
    print(f"Users in 'ftvpremium' but not in 'ftvpaidchat': {len(premium_not_in_paidchat)}")
    
    for member in premium_not_in_paidchat:
        user_details = f"User ID: {member.id}, Username: @{member.username}, Name: {member.first_name} {member.last_name if member.last_name else ''}, Phone: {member.phone if member.phone else 'N/A'}"
        print(user_details)

# Run the script
with client:
    client.loop.run_until_complete(compare_groups())
