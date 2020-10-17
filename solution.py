#!/bin/env python3.6
import bitskins
import discord
import pyotp, base64, asyncio
from datetime import timedelta, datetime

TOKEN= "DISCORD TOKEN HERE"

API_KEY= "BITSKINS API KEY HERE"

my_secret= 'BITSKINS SECRET HERE'

client = discord.Client()

def get_embed(item):
	embed=discord.Embed(title=item.name, url= "https://bitskins.com/view_item?app_id=730&item_id={}".format(item.item_id), color=0x8000ff)
	embed.set_author(name="Skin Bot", url="https://www.steadysoles.com/",icon_url="https://pbs.twimg.com/profile_images/1142950465782669313/YvG8n7YA_400x400.png")
	embed.set_thumbnail(url=item.image)
	embed.add_field(name="Price:", value="${}".format(item.price))
	embed.add_field(name="Discount:", value="{}%".format(item.reduction), inline=True)
	if item.available:
		tmp= "Instantly Withdrawable"
	else:
		tmp= str(timedelta(seconds= item.available_in))
	embed.add_field(name="Availability:", value=tmp, inline=True)
	embed.add_field(name="Suggested Price:", value="${}".format(item.suggested_price), inline=True)
	embed.add_field(name="Profit:", value="${}".format(item.margin), inline=True)
	embed.set_footer(text="Made by Aqyl#0001 | {}".format(datetime.now()), icon_url="https://cdn.discordapp.com/avatars/209007491713990656/53c679c5a86fa33c3bb9631626e80589.png")
	return embed

async def status_task(wait_time= 60* 5):
	while True:
		print("Updated on: {}".format(datetime.now()))
		code= pyotp.TOTP(my_secret)
		try:
			items= bitskins.get_items(code.now(), API_KEY)
			for item in items:
				await client.send_message(client.get_channel("CHANNEL ID HERE"), embed=get_embed(item))
		except:
			pass
			traceback.print_exc()
		await asyncio.sleep(wait_time)

@client.event
async def on_ready():

	wait_time= 60 * 10 # 10 mins in this case

	print('CSGO BitSkins Bot')
	print('Made by Aqyl#0001')
	print('Version 1.0.5')
	print('')
	print('Logged in as:')
	print(client.user.name)
	print('------------------------------------------')
	client.loop.create_task(status_task(wait_time))

try:
	client.run(TOKEN)
except:
	print("Couldn't connect to the Discord Server.")
