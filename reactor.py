import os
import json
import random
import requests
from gtts import gTTS
from dotenv import load_dotenv

from fbchat import Client, log, MessageReaction
from fbchat.models import *

load_dotenv(override=True)

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def get_meme():
    url = requests.get('https://meme-api.herokuapp.com/gimme').json()['url']
    print(f"sending {url}")
    return url


def get_random_joke():
    headers = {'Accept': 'text/plain'}
    joke = requests.get('https://icanhazdadjoke.com/', headers=headers).text
    return joke


class FBChatClient(Client):
    def onMessage(self,
                  mid=None,
                  author_id=None,
                  message=None,
                  message_object=None,
                  thread_id=None,
                  thread_type=ThreadType.USER,
                  ts=None,
                  metadata=None,
                  msg=None):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # if author_id == self.uid:
        #     return

        # if thread_type != ThreadType.USER:

        #     return

        # reactions = [
        #     MessageReaction.LOVE, MessageReaction.ANGRY, MessageReaction.SMILE,
        #     MessageReaction.SAD
        # ]

        # self.reactToMessage(mid, random.choice(reactions))

        if message.lower() == '-kanda':
            self.send(Message('sorry i cant :( its illegal.'),
                      thread_id=thread_id,
                      thread_type=thread_type)
        #     kandaGroups = ['2416035088446283', '1767312170046705']
        #     videos = self.fetchThreadImages(
        #         thread_id=random.choice(kandaGroups))
        #     skipping_number = random.randint(0, 50)
        #     for k, i in enumerate(videos):

        #         if k <= skipping_number:
        #             continue

        #         if isinstance(i, VideoAttachment):
        #             self.forwardAttachment(i.uid, thread_id=thread_id)
        #             break

        print(message)

        if message.lower() == '-joke':
            self.send(Message(get_random_joke()),
                      thread_id=thread_id,
                      thread_type=thread_type)

        elif message.lower() == '-meme':
            self.sendRemoteFiles(get_meme(),
                                 thread_id=thread_id,
                                 thread_type=thread_type)

        elif message.lower().startswith('say'):
            voice = " ".join(message.split(" ")[1:])
            tts = gTTS(voice, lang='ne')
            tts.save('voice.mp3')

            self.sendLocalVoiceClips('voice.mp3',
                                     thread_id=thread_id,
                                     thread_type=thread_type)
            os.remove('voice.mp3')

        elif 'help-bot' in message:
            msg = "You can text me using these commands\n-kanda -> will send you kanda\n-meme -> will send you meme\n-joke -> will send you a joke.\nHave fun!"
            self.send(Message(msg),
                      thread_id=thread_id,
                      thread_type=thread_type)


client = FBChatClient(username, password)

if not client.isLoggedIn():
    client.login()

client.listen()
