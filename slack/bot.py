import requests as rq
import json

if __name__ == '__main__':

    channel_name = 'private_chan_name'
    bot_name = 'bot_name'
    text = 'This is posted to #{} and comes from {}'.format(channel_name, bot_name)

    print(text)
    emoji = ':smiley:'

    webhook_url = 'https://hooks.slack.com/services/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'

    data = {}

    data['text'] = text
    data['username'] = bot_name
    data['channel'] = channel_name
    data['icon_emoji'] = emoji

    payload = json.dumps(data)


    r = rq.post(webhook_url, data=payload)

    print(r.text)
