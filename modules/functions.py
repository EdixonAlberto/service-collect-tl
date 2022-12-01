from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantsSearch,
    PeerChannel
)


class Functions():
  def __init__(self, client: TelegramClient, channel: str, limit: int) -> None:
    self.client = client
    self.entity = PeerChannel(channel) if channel.isdigit() else channel
    self.limit = limit

  async def get_users(self) -> list:
    all_participants = []
    all_user_details = []

    try:
      participants = await self.client(GetParticipantsRequest(
          channel=await self.client.get_entity(self.entity),
          filter=ChannelParticipantsSearch(''),
          offset=0,
          limit=self.limit,
          hash=0
      ))
      users = participants.users

      if not users:
        return []

      all_participants.extend(users)
      offset += len(users)

      for participant in all_participants:
        all_user_details.append({
            "id": participant.id,
            "first_name": participant.first_name,
            "last_name": participant.last_name,
            "user": participant.username,
            "phone": participant.phone,
            "is_bot": participant.bot
        })

      return all_user_details
    except:
      print('ERROR:', self.get_users.__name__)
      return []

  async def get_messages(self) -> list:
    all_messages = []
    # total_messages = 0
    # total_count_limit = 0

    try:
      history = await self.client(GetHistoryRequest(
          peer=await self.client.get_entity(self.entity),
          offset_id=0,
          offset_date=None,
          add_offset=0,
          limit=self.limit,
          max_id=0,
          min_id=0,
          hash=0
      ))
      messages = history.messages

      if not messages:
        return []

      for message in messages:
        all_messages.append(message.to_dict())

      # total_messages = len(all_messages)

      # if total_count_limit != 0 and total_messages >= total_count_limit:
      #   return

      return all_messages

    except:
      print('ERROR:', self.get_messages.__name__)
      return []
