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


def save_json(path: str, result: list) -> None:
  with open(path, 'w') as outfile:
    json.dump(result, outfile, cls=DateTimeEncoder)
    print('APP: Data saved in file json')
