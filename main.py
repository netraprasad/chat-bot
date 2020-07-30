#!/usr/bin/env python
import os
import random
from dotenv import load_dotenv

from fbchat import Client, log
from fbchat.models import *
import logging

from messages import messages

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


class FBChatClient(Client):
    def __init__(self,
                 email,
                 password,
                 user_agent=None,
                 max_tries=5,
                 session_cookies=None,
                 logging_level=logging.INFO):
        self.threadsToReply = []
        super().__init__(email,
                         password,
                         user_agent=user_agent,
                         max_tries=max_tries,
                         session_cookies=session_cookies,
                         logging_level=logging_level)

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

        if author_id == self.uid:

            if message.lower() == '-s-':
                print("ADDED!")
                self.threadsToReply.append(thread_id)
                self.unsend(mid)

            if message.lower() == '-x-':
                print("REMOVED!")
                self.threadsToReply.remove(thread_id)
                self.unsend(mid)

            return

        user = None

        if thread_type != ThreadType.USER:

            user = "sathi"

        else:

            user = client.fetchUserInfo(thread_id)[thread_id].first_name

        if message.lower() == '-s-':
            print(f"ADDED! {thread_id}")
            print(self.threadsToReply)
            if thread_id not in self.threadsToReply:
                self.threadsToReply.append(thread_id)
            self.send(Message("hello there."),
                      thread_id=thread_id,
                      thread_type=thread_type)

            return

        if message.lower() == '-x-':

            print(f"REMOVED! {thread_id}")
            self.send(Message("why do u hate robots :( ok bye."),
                      thread_id=thread_id,
                      thread_type=thread_type)
            print(self.threadsToReply)

            self.threadsToReply.remove(thread_id)

            return

        print(self.threadsToReply)

        if thread_id in self.threadsToReply:

            if len(message) == 1:
                self.send(Message("Ali ramrari reply garana k"),
                          thread_id=thread_id)

            self.send(Message(random.choice(messages).format(user)),
                      thread_id=thread_id,
                      thread_type=thread_type)


client = FBChatClient(username, password, logging_level=35)

if not client.isLoggedIn():
    client.login()

client.listen()
