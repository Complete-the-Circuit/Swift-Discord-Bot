import discord
from discord.ext import commands
import asyncio
import youtube_dl

import cv2
import numpy as np
from urllib.request import urlretrieve
from urllib.error import HTTPError
import urllib

from talking_clock import TalkingClock
from time import sleep

bot_token = ""
bot_ID = ""

client = discord.Client()
bot_prefix = "!"
client = commands.Bot(command_prefix = bot_prefix)

@client.event
async def on_ready():
    print("Logged in as\n", client.user.name, "\n", client.user.id, "\n ----------")
    if not discord.opus.is_loaded():
        discord.opus.load_opus()

class Messaging():
    def __init__(self, message):
        self.message = message

    async def haar_detect(self):
        if self.message.content.startswith("!detectFeline"):
            url = self.message.content[14:]
            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            valid_url = True
            print(url)
            print(req)

            try:
                urlretrieve(url, "cat_image.jpg")
            except FileNotFoundError as err:
                print(err)  # something wrong with local path
                await client.send_message(self.message.channel, "There is an error on my end, please wait.")
                valid_url = False
            except HTTPError as err:
                print(err)  # something wrong with url
                await client.send_message(self.message.channel, "URL not accepted, cats cannot be found. ABORT! ABORT!")
                valid_url = False

            if valid_url == True:
                image = cv2.imread("cat_image.jpg")
                grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                face_cascade = cv2.CascadeClassifier("haar_cascades/haarcascade_frontalcatface.xml")
                extended_face_cascade = cv2.CascadeClassifier("haar_cascades/haarcascade_frontalcatface_extended.xml")
                num_cats = 0
                cat_bounding_boxes = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=2, minSize=(50, 50))
                for (i, (x, y, w, h)) in enumerate(cat_bounding_boxes):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
                    print("The cats have been detected")
                    if i == 0:
                        await client.send_message(self.message.channel, "1 cat detected")
                    elif i > 0:
                        await client.send_message(self.message.channel, "%d cats detected" % (i + 1))
                    num_cats = i + 1
                cv2.imwrite("Results/cat_image_result.jpg", image)
                if num_cats > 0:
                    # Show the detected cat faces
                    await client.send_file(self.message.channel, "Results/cat_image_result.jpg")
                else:
                    await client.send_message(self.message.channel, "There are no cats...")

    async def talking_clock(self):
        if self.message.content.startswith("!time"):
            clock = TalkingClock()
            current_hour, current_minutes, twelve_hour_time = clock.string_time()
            cond_hour = current_hour
            current_hour, current_minutes, twelve_hour_time = str(current_hour), str(current_minutes), str(
                twelve_hour_time)
            if cond_hour >= 12:
                await client.send_message(self.message.channel, "The time is: " + twelve_hour_time + ":" + current_minutes, tts=True)
            elif cond_hour <= 12:
                await client.send_message(self.message.channel, "The time is: " + current_hour + ":" + current_minutes, tts=True)

    async def help(self):
        command_list = ["I have several commands that are currently available for use. These are:",
                        "!detectFeline - Detects cats from the provided URL.",
                        "!youtube - Plays a preset youtube video.",
                        "!ytRequest - Plays the provided youtube video URL in the current voice channel the user is in.",
                        "Credits go to the bot author Fyrngarm#5098, and the discord.py API."]
        if self.message.content.startswith("?help"):
            await client.send_message(self.message.channel, "\n".join(command_list))
        elif self.message.content.startswith("?ping"):
            await client.send_message(self.message.channel, "pong")

class AudioPlayback(Messaging):
    def __init__(self):
        super.__init__()

    async def youtube_player(self):
        if self.message.content.startswith("!youtube"):
            channel = self.message.author.voice_channel
            voice = await client.join_voice_channel(channel)
            player = await voice.create_ytdl_player("https://youtu.be/H3HFOlYba-4")
            player.volume = 0.7
            player.start()
            while player.is_playing():
                if player.is_playing() == False:
                    player.stop()
                    disconnect = await voice.disconnect()
                    print("Bot has left the voice channel")
                    break
client.run(bot_token)
