import time
import json
import re

from slackclient import SlackClient  # https://github.com/slackhq/python-slackclient


# token found at https://api.slack.com/web#authentication
def connect_to_slack(access_token):
    if not access_token:
        access_token = str(raw_input("Enter your developer access token: "))
    sc = SlackClient(access_token)
    if sc:
        return sc
    else:
        raise RuntimeError("connection failed! invalid token?")


def map_user_id_to_names(slack_client):
    response = slack_client.api_call('users.list')
    member_data = json.loads(response)
    if member_data['ok']:
        all_members = {}
        members = member_data['members']
        for member in members:
            if 'is_bot' in member and not member['is_bot']:
                member_id = member['id']
                try:
                    full_name = member['profile']['real_name']
                    first_name = member['profile']['first_name']
                    nickname = member['name']
                except KeyError:  # some users have no name information
                    email_name = member['profile']['email'].split('@')[0]  # best we can do, get email address
                    full_name, first_name, nickname = email_name, email_name, email_name
                all_members[member_id] = {'full_name': full_name, 'first_name': first_name,
                                          'nickname': nickname}
    else:
        raise RuntimeError("bad connection to slack api! tried to hit users.list")
    return all_members


def get_messages(user_id_to_name_map, channel_id, channel_name, slack_client, limit):
    messages_data = {'channel_name': channel_name, 'channel_id': channel_id, 'messages': []}
    response = slack_client.api_call('channels.history', count=limit, channel=channel_id)
    channel_data = json.loads(response)
    if channel_data['ok']:
        for message in channel_data['messages']:
            if message['type'] == 'message' and 'subtype' not in message:
                text = message['text'] + '.'
                # replace user ids in text with user names!
                all_user_ids = re.findall(r'<@([^\s\.]*)>', text)
                for user_id in all_user_ids:
                    user = user_id_to_name_map[user_id]['nickname']
                    text = text.replace('<@%s>' % user_id, '@' + user)
                sender = user_id_to_name_map[message['user']]
                timestamp = message['ts']
                emojis = []
                try:
                    emojis = [{'name': name, 'count': count} for reaction in message['reactions']]
                except: KeyError  # no emojis in the message
                message_data = {'text': text, 'emojis': emojis, 'sender': sender, 'timestamp': timestamp}
                messages_data['messages'].append(message_data)
        return messages_data
    else:
        raise RuntimeError('bad connection to slack api! tried to hit channels.history')

