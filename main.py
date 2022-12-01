from os import getenv
from dotenv import load_dotenv
from modules.client import Client
from modules.json_parser import transform_dict
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

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


@app.middleware('http')
# Authentication
async def auth(request, call_next):
  if not 'authorization' in request.headers:
    return JSONResponse(
        status_code=401,
        content={'error': "Header 'Authorization' is required"}
    )

  headerToken = request.headers['authorization'].split(' ')[1]
  token = getenv('ACCESS_TOKEN')

  if (headerToken == token):
    return await call_next(request)
  else:
    return JSONResponse(
        status_code=401,
        content={'error': 'Unauthorized, this token is invalid'}
    )


@app.middleware('http')
# Custom Cors
async def custom_cors(request, call_next):
  if not 'origin' in request.headers:
    return JSONResponse(
        status_code=401,
        content={'error': "Header 'Origin' is required"}
    )

  origin = request.headers['origin']
  whiteList = getenv('WHITE_LIST').split(',')

  if origin in whiteList:
    return await call_next(request)
  else:
    return JSONResponse(
        status_code=401,
        content={'error': 'Unauthorized, this origin not allowed'}
    )


@app.get('/api/collect_channel/{channel}')
async def collect(channel: str, limit: int = Query(gt=0, lt=11), data: str = Query(regex="^messages$|^users$")):
  await client.run()
  response = await client.execute(channel, data, limit)
  response = transform_dict(response)

  return response
