from abc import abstractmethod
from cement.core.interface import Interface
from cement.core.handler import Handler
import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

class SlackInterface(Interface):
    class Meta:
        interface = 'slack'
    
    @abstractmethod
    def _paginate(client, method: str, **kwargs):
        pass
    
    @abstractmethod
    def verify_access(self):
        pass

    @abstractmethod
    def channels_join(self):
        pass
    
    @abstractmethod
    def channel_get_id_from_ticket(self,ticket):
        pass
    
    @abstractmethod
    def channel_get_id_from_name(self, name):
        pass

    @abstractmethod
    def channel_verify(self):
        pass
    
    @abstractmethod
    def send_message(self, channel, text):
        pass
    
    @abstractmethod
    def send_thread(self):
        pass
    
    @abstractmethod
    def edit_message(self):
        pass
    
class SlackHandler(SlackInterface, Handler):
    pass    

class SlackMessages(SlackHandler):
    class Meta:
        label = 'slack_messages'
        interface = 'slack'
    
    load_dotenv()
    client = WebClient(token=os.getenv("SLACK_TOKEN"))

    def _paginate(self,client: WebClient, method: str, **kwargs):
        aggregated_results = []
        cursor = None
        while True:
            if cursor:
                kwargs["cursor"] = cursor
            response = getattr(client, method)(**kwargs)
            data_key = 'channels'  # adjust this based on the specific API method you're calling
            if data_key in response.data:
                aggregated_results.extend(response.data[data_key])

            # Check for the next cursor
            cursor = response.data.get("response_metadata", {}).get("next_cursor")

            # If there's no next cursor, or it's empty, break out of the loop
            if not cursor:
                break

            # Sleep for a short duration to avoid hitting rate limits (adjust as needed)
            time.sleep(1)

        return aggregated_results  

    def verify_access(self):
        pass
            
    def channels_join(self, channel):
        try:
            response = self.client.conversations_join(channel=channel)
            self.app.log.debug(response)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

    def channel_get_id_from_ticket(self, ticket):
        name = ticket.replace("T", "t").replace(".", "_")
        return self.channel_get_id_from_name(name)

    def channel_get_id_from_name(self, name):
        id = None

        try:
            response = self._paginate(self.client, "conversations_list", exclude_archived=True )
            for channel in response:
                if channel['name'] == name:
                    
                    id = channel['id']
                    break
            
        except SlackApiError as e:
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
        return id

    def channel_verify(self):
        pass
    
    def send_message(self, channel, text):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            self.app.log.debug(response)
            return response['ts']
            
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'


    def send_thread(self, channel, thread_ts, text):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                thread_ts=thread_ts,
                text=text
            )
            self.app.log.info(response)
            
        except SlackApiError as e:
            assert e.response["error"]
        
    
    def edit_message(self):
        pass


# slack_token = config.SLACK_TOKEN
# client = WebClient(token=slack_token)

# try:
#     response = client.chat_postMessage(
#         channel="C05KCJSJV4N",
# 		text="Bot test, please ignore"
#     )
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
