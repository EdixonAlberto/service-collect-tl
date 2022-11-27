import configparser
# import json
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import (
    ChannelParticipantsSearch,
    PeerChannel
)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']
user_input_channel = config['Telegram']['user_input_channel']

api_id = int(api_id)
api_hash = str(api_hash)
# user_input_channel = int(user_input_channel) # also to ID

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")

# Ensure you're authorized


async def main():
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
    try:
        await client.sign_in(phone, input('Enter the code: '))
        await run_channels()
    except SessionPasswordNeededError:
        await client.sign_in(password=input('Password: '))


async def run_channels():
    print('init: Channel')
    entity = PeerChannel(user_input_channel)
    my_channel = client.get_entity(entity)
    print('continue: Channel')

    # Config Request
    offset = 0
    limit = 100
    all_participants = []
    hash = 0

    while True:
        participants = client(GetParticipantsRequest(
            my_channel,
            ChannelParticipantsSearch(''),
            offset,
            limit,
            hash
        ))

        if not participants.users:
            break

        all_participants.extend(participants.users)
        offset += len(participants.users)
        print(all_participants)

# _______________________________________
asyncio.run(main())
# if __name__ == '__MAIN__':
#     print('Main runing')
