#!/usr/bin/env python3
"""
randomreddit.py - return a random reddit url from a subreddit's frontpage
author: andreim <andreim@andreim.net>
"""

import web
import re
import json
from random import choice

def randomreddit(phenny, input):

	subreddit = input.group(2)
	if not subreddit:
		phenny.say(".random <subreddit> - get a random link from the subreddit's frontpage")
		return
		
	if not re.match('^[A-Za-z0-9_-]*$',subreddit):
		phenny.say(input.nick + ": bad subreddit format.")
		return


	url = "http://www.reddit.com/r/" + subreddit + "/.json"
	try:
		resp = web.get(url)
	except:
		try:
			resp = web.get(url)
		except:
			try:
				resp = web.get(url)
			except:
				phenny.reply('Reddit or subreddit unreachable.')
				return
	
	reddit = json.loads(resp)
	post = choice(reddit['data']['children'])

	nsfw = False
	if post['data']['over_18']:
		nsfw = True
	
	if nsfw:
		phenny.reply("!!NSFW!! " + post['data']['url'] + " (" + post['data']['title'] + ") !!NSFW!!")
	else:
		phenny.reply(post['data']['url'] + " (" +  post['data']['title'] + ")")

randomreddit.commands = ['random']
randomreddit.priority = 'medium'
randomreddit.thread = False