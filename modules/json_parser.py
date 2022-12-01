import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
  # some functions to parse json date
  def default(self, o):
    if isinstance(o, datetime):
      return o.isoformat()

    if isinstance(o, bytes):
      return list(o)

    return json.JSONEncoder.default(self, o)


def transform_dict(payload: dict) -> dict:
  path_temp = 'result.json'

  with open(path_temp, 'w') as outfile:
    json.dump(payload, outfile, cls=DateTimeEncoder)

  with open(path_temp) as dataJson:
    dataDict = json.load(dataJson)

  return dataDict
