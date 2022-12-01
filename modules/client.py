from __future__ import annotations
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from modules.functions import Functions


class Client():
  def __init__(
      self,
      username: str,
      api_id: str,
      api_hash: str,
      phone: str,
      code_login: str,
      password: str,
      target_channel: str
  ) -> None:
    self.phone = phone
    self.code_login = code_login
    self.password = password
    self.target_channel = target_channel
    # Create the client and connect
    self.client = TelegramClient(username, int(api_id), api_hash)

  async def run(self) -> None:
    await self.client.start()
    print("APP: Client created")

    # Ensure you're authorized
    if not await self.client.is_user_authorized():
      await self.client.send_code_request(self.phone)
    try:
      await self.client.sign_in(self.phone, self.code_login)
    except SessionPasswordNeededError:
      await self.client.sign_in(password=self.password)

  async def execute(self, data: str, limit: int) -> list | None:
    functions = Functions(self.client, self.target_channel, limit)
    method = 'get_{}'.format(data)
    return await getattr(functions, method)()
