import praw
from config import *
from time import sleep
from better_profanity import profanity
from badwords import badwords
from datetime import datetime
import discord
import os
# import nest_asyncio
# nest_asyncio.apply()

# import logging

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)

client = discord.Client()

print("Logging in Reddit...")
try:
	reddit = praw.Reddit(username = username,
				password = password,
				client_id = client_id,
				client_secret = client_secret,
				user_agent = user_agent)
	print("Logged in Reddit!")

@client.event
async def on_ready():
  print('We have logged in Discord as {0.user}'.format(client))

def comment(op,body): #Filter Spam
	if op.comment_karma + op.link_karma < 10:
		print(f"{op.name}'s karma is too low. Bypassing submission.")
		error = 'toolong'
		return False
	elif len(body) > 9800:
		body = body[:9800]
	return True

def reply(title, body): 
	if len(body) <= 1:
		replytext = title
	else:
		replytext = body
	profanity.load_censor_words(badwords) #Censor slurs
	return profanity.censor(replytext)

@client.event
async def on_message(message):
	subreddit = reddit.subreddit("copypasta")
	channel = client.get_channel(channelid)
	for submission in subreddit.stream.submissions(skip_existing=True):
		title = submission.title
		body = submission.selftext
		op = submission.author

		try:
			if comment(op,body):
				submission.reply(reply(title,body))
				print(f'Replied to {op.name}')
				time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
				await channel.send(f"{time} --- Replied to {op.name}.")
				sleep(10)
			if not comment(op,body):
				time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
				await channel.send(f"{time} --- Bypassed {op.name}, karma too low.")
		except:
				print('Failed to reply. Please check.')
				time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
				await channel.send(f"{time} --- Error. Failed to reply.")

if __name__ == "__main__":
	client.run(discordtoken)