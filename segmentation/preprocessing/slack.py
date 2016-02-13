# parse slack messages into structured data.
# example:
#       mentor_paulcutsinger [11:23 AM] 
#       yes @andrew, we have a demo device that you can use during demo day. I'll be around from 6pm on so you can practice hooking up to it. Other folks will need it too so we'll have to share it :smile:
# we want to parse it as:
#       {
#           'speaker': mentor_paulcutsinger,
#           'time':    11:23 AM,
#           'mentions': [@andrew],
#           'emojis': ['smile']
#           'links':  ['']
#       }
import doctest
import re

def find_mentions(text):
    '''
    >>> find_mentions('@andrew: what do you think of our @mentor_alexa')
    ['andrew', 'mentor_alexa']
    '''
    return re.findall(r'@([^\s,.:?-]*)', text)


def find_emojis(text):
    '''
    >>> find_emojis('@andrew: :smile:')
    ['smile']
    '''
    return re.findall(r':([^:\s]*):', text)


def find_urls(text):
    '''
    >>> find_urls('Parrot Rolling Spider mini drone: https://github.com/voodootikigod/node-rolling-spider')
    ['https://github.com/voodootikigod/node-rolling-spider']
    '''
    return re.findall(r"(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})", text)

def sanitize(text, list_of_phrases):
    '''
    >>> sanitize('@andrew: hello@andrew', ['@andrew'])
    ': hello'
    '''
    for phrase in list_of_phrases:
        text = text.replace(phrase, '')
    return text

def parse_body(text):
    data = {
        'emojis': find_emojis(text),
        'mentions': find_mentions(text),
        'urls': find_urls(text),
        'text': text,
    }

    sanitized = sanitize(text, ['@' + item for item in data['mentions']])
    sanitized = sanitize(sanitized, [':' + item + ':' for item in data['emojis']])
    sanitized = sanitize(sanitized, data['urls'])

    data['sanitized'] = sanitized

    return data

doctest.testmod()


