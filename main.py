import asyncio
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
from modules.client import Client
from modules.save import save_json


async def main():
  # Get environments variables
  load_dotenv()

  client = Client(
      username=getenv('USERNAME'),
      api_id=getenv('API_ID'),
      api_hash=getenv('API_HASH'),
      phone=getenv('PHONE'),
      code_login=getenv('CODE_LOGIN'),
      password=getenv('PASSWORD'),
      target_channel=getenv('TARGET_CHANNEL')
  )

  await client.run()
  result = await client.messages()
  save_json('docs/result.json', result)

asyncio.run(main())
