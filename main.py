from os import getenv
from dotenv import load_dotenv

from modules.client import Client
from modules.json_parser import transform_dict
from fastapi import FastAPI, Query

# Get environments variables
load_dotenv()

client = Client(
    username=getenv('USERNAME'),
    api_id=getenv('API_ID'),
    api_hash=getenv('API_HASH'),
    phone=getenv('PHONE'),
    code_login=getenv('CODE_LOGIN'),
    password=getenv('PASSWORD')
)

app = FastAPI()


@app.get('/api/collect_channel/{channel}')
async def collect(channel: str, limit: int = Query(gt=0, lt=11), data: str = Query(regex="^messages$|^users$")):
  await client.run()
  response = await client.execute(channel, data, limit)
  response = transform_dict(response)

  return response
