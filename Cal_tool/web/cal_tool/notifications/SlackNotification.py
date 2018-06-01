from .Observer import Observer

class SlackNotification(Observer):
    def update(self, observable, arg):
        if 'token' in arg and 'channel' in arg and 'message' in arg and 'message' in arg:
            self.__send_slack_messege(arg['token'], arg['channel'], arg['message'])

    def __send_slack_messege(self, p_token, p_channel, p_messege):
        sc = SlackClient(p_token)

        sc.api_call(
            "chat.postMessage",
            channel=p_channel,
            text=p_messege
        )

from slackclient import SlackClient