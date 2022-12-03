from os import getenv
from dotenv import load_dotenv
from modules.client import Client
from modules.json_parser import transform_dict
from fastapi import FastAPI, Query, Request
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


# Authentication
@app.middleware('http')
async def auth(request: Request, call_next):
  if not 'authorization' in request.headers:
    return JSONResponse(
        status_code=401,
        content={'error': "Header 'Authorization' is required"}
    )

  headerToken = request.headers['authorization'].strip('Bearer ')
  token = getenv('ACCESS_TOKEN')

  if (headerToken == token):
    return await call_next(request)
  else:
    return JSONResponse(
        status_code=401,
        content={'error': 'Unauthorized, this token is invalid'}
    )


# Custom Cors
@app.middleware('http')
async def custom_cors(request: Request, call_next):
  print(request.headers)
  if not 'origin' in request.headers:
    return await call_next(request)

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
