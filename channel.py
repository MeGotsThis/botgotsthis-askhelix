import random
import urllib.parse
from typing import Dict, List  # noqa: F401

import aiohttp

import bot
from lib.data import ChatCommandArgs
from lib.helper.chat import feature, min_args, permission

outcomes: List[str] = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again ",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
    "no.",
    "START",
    "A",
    "B",
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "SELECT",
    ]


@feature('helixfossil')
@min_args(2)
@permission('moderator')
async def commandAskHelix(args: ChatCommandArgs):
    browserHash: str = base36encode(random.randrange(60466177, 2176782336))
    helixRespose: str = random.choice(outcomes)
    data: Dict[str, str] = {
        'action': 'save',
        'hash': browserHash,
        'ans': helixRespose,
        'q': args.message.query,
        }
    headers: Dict[str, str] = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    postData: str = urllib.parse.urlencode(data)

    session: aiohttp.ClientSession
    response: aiohttp.ClientResponse
    async with aiohttp.ClientSession(raise_for_status=True) as session, \
            session.post('http://askhelixfossil.com/ajax.php',
                         data=postData,
                         headers=headers,
                         timeout=bot.config.httpTimeout) as response:
        await response.read()

    url: str = f'http://askhelixfossil.com/#{browserHash}'
    args.chat.send(f'{args.nick} -> {url}')
    return True


def base36encode(number: int,
                 alphabet: str='0123456789abcdefghijklmnopqrstuvwxyz') -> str:
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36: str = ''
    sign: str = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        i: int
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36
