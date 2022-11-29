import configparser
import json
from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
# from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    # ChannelParticipantsSearch,
    PeerChannel
)


class DateTimeEncoder(json.JSONEncoder):
  # some functions to parse json date
  def default(self, o):
    if isinstance(o, datetime):
      return o.isoformat()

    if isinstance(o, bytes):
      return list(o)

    return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
API_ID = int(config['Telegram']['api_id'])
API_HASH = str(config['Telegram']['api_hash'])
PHONE = config['Telegram']['phone']
USERNAME = config['Telegram']['username']
CODE_LOGIN = config['Telegram']['code_login']
TARGET_CHANNEL = config['Telegram']['target_channel']

# Create the client and connect
client = TelegramClient(USERNAME, API_ID, API_HASH)


async def main(phone):
  # Ensure you're authorized
  await client.start()
  print("Client Created")

  if not await client.is_user_authorized():
    await client.send_code_request(phone)
  try:
    await client.sign_in(phone, CODE_LOGIN)
  except SessionPasswordNeededError:
    await client.sign_in(password=input('Password: '))

  # me = await client.get_me()

  if TARGET_CHANNEL.isdigit():
    entity = PeerChannel(TARGET_CHANNEL)
  else:
    entity = TARGET_CHANNEL

  my_channel = await client.get_entity(entity)

  offset_id = 0
  limit = 10
  all_messages = []
  total_messages = 0
  total_count_limit = 0

  history = await client(GetHistoryRequest(
      peer=my_channel,
      offset_id=offset_id,
      offset_date=None,
      add_offset=0,
      limit=limit,
      max_id=0,
      min_id=0,
      hash=0
  ))

  if not history.messages:
    return

  print(
      "Current Offset ID is:", offset_id,
      "; Total Messages:", total_messages
  )

  messages = history.messages

  for message in messages:
    all_messages.append(message.to_dict())

  offset_id = messages[len(messages) - 1].id
  total_messages = len(all_messages)

  if total_count_limit != 0 and total_messages >= total_count_limit:
    return

  with open('docs/channel_messages.json', 'w') as outfile:
    json.dump(all_messages, outfile, cls=DateTimeEncoder)


with client:
  client.loop.run_until_complete(main(PHONE))

if __name__ == '__MAIN__':
  print('Main runing')
