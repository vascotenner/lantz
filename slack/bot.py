from requests import post, get
from json import dumps
from time import strftime

def slack_file_upload(directory, filename, slack_channel):
    """
    This function uploads a file to a slack channel from the account that
    corresponds to the token specified the the function body below. Note that
    this file can be acccessed publicly by someone with the url, so do not post
    any information (or data) that might be sensitive.

    You will need to create a web token using the page at:
    https://api.slack.com/web

    Note that this token is yours, and should remain private - please take
    care to not commmit your token to GitHub, since this lets people have
    access to your entire slack account.

    Note that executing this function will send a message to your slackbot
    channel alerting you that the file permissions have been changed.

    Parameters:
        directory (str): location of the file
        filename (str): filename
        slack_channel (str): slack channel to post the file to

    Returns:

        file_url (str): public location of the file
    """
    print('Did you change the token??')
    token = 'xxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxx'
    channel = slack_channel

    upload_url = 'https://slack.com/api/files.upload'

    data = {'token': token, 'channels': slack_channel, 'is_public': 'true',
            'public_url_shared': 'true'}

    f_loc = directory + filename

    file_dict =  {'file': open(f_loc, 'rb')}

    r = post(upload_url,  params=data, files=file_dict)
    json = r.json()

    file_url = json['file']['permalink_public']

    r = post(file_url) #pinging this link is actually what enables the public link

    address = file_url.replace('https://slack-files.com/','')
    keys = address.split('-')

    file_url = 'https://files.slack.com/files-pri/{}-{}/{}?pub_secret={}'.format(keys[0], keys[1], filename, keys[2])
    return file_url

def post_status_message(message, slack_channel, bot_name='status_bot',
                        emoji=':robot_face:', title='', attachment_text='',
                        color='#000000', directory='',  filename='',
                        fallback_message=''):
    """
    Posts a status message to Slack.

    Parameters:

        message (str): message text to post to channel
        slack_channel (str): name of Slack channel to post to

        bot_name (str): name of bot to post as
        emoji (str): emoji to use for bot icon

        title (str): attachment title text
        attachment_text (str): attachment text
        color (hex color): hexadecimal color to display with message

        directory (str): directory where file to post is located
        filename (str): name of file to post
        fallback_message (str): message to display if file does not load

    Returns:
        none
    """
    image_url = ''

    print(directory)

    print(filename)

    if not filename or directory:

        image_url = slack_file_upload(directory=directory, filename=filename,
                          slack_channel=slack_channel)

        message = message + '<{}>'.format(image_url)

    webhook_url = 'https://hooks.slack.com/services/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'

    data = {}

    data['text'] = message
    data['username'] = bot_name
    data['channel'] = slack_channel
    data['icon_emoji'] = emoji

    attachments = {}
    attachments['fallback'] = fallback_message
    attachments['title'] = title
    attachments['text'] = attachment_text
    attachments['color'] = color

    if not image_url:
        attachments['image_url'] = image_url

    att = [attachments]

    data['attachments'] = att

    payload = dumps(data)

    r = post(webhook_url, data=payload)

def send_cryostat_cooldown_complete(temperature, slack_channel, directory, filename):
    """
    Example settings for sending a Janis status message that the cryostat has
    cooled down.
    """
    bot_name = 'janis-bot'
    message = '#janis_status ({})\nThe cyrostat is now cold, current temp: {}K'.format(strftime('%x %X %Z'),3.1)
    emoji = ':snowman:'


    title = 'Cooldown complete'
    attachment_text = 'Cooldown data'
    fallback_text = 'Plot of cryostat cooldown'
    color = '#439FE0'

    post_status_message(message=message, slack_channel=slack_channel,
                        bot_name='janis-bot', emoji=emoji, title=title,
                        attachment_text=attachment_text, color=color,
                        directory=directory, filename=filename,
                        fallback_message=fallback_text)


if __name__ == '__main__':
    """
    Set slack channel here for testing.

    Can also select an image file for upload here to test.
    """

    slack_channel = '#your-channel'
    directory = 'E:\\your\\directory\\name\\here'
    filename = 'image_file.jpg'

    send_cryostat_cooldown_complete(3.1, slack_channel, directory, filename)
