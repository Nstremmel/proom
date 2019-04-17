import discord
import asyncio
import random
from time import sleep
import datetime
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from discord.utils import get

emojipath = 'proom.csv'
client = discord.Client()


# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# client1 = gspread.authorize(creds)
# sheet = client1.open("Party Room Donations").sheet1

import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c=conn.cursor()

#c.execute("DROP TABLE giveaway")
# c.execute("""CREATE TABLE giveaway (
# 				gnumber int,
# 				people text,
# 				day int
# 				)""")
# c.execute("INSERT INTO giveaway VALUES (%s, %s, %s)", (1, "", int(datetime.datetime.today().day)))
# conn.commit()

# c.execute("DROP TABLE donors")
# c.execute("""CREATE TABLE donors (
# 				id bigint,
# 				donations bigint
# 				)""")
# conn.commit()

# c.execute("DROP TABLE data")
# c.execute("""CREATE TABLE data (
# 				items text,
# 				chest bigint
# 				)""")
# conn.commit()

def reset():
	global guesses,solved,blank,wrong,word1
	guesses=6
	solved=[]
	blank=[]
	wrong=[]
	word1="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs"

def isstaff(checkedid,serverroles,authorroles):
	for i in open("staff.txt"):
		role=get(serverroles, name=str(i.strip()))
		if role in authorroles:
			return "verified"

def getvalue(userid, column):
	try:
		c.execute("SELECT donations FROM donors WHERE id={}".format(userid))
		tester=int(c.fetchone()[0])
	except:
		c.execute("INSERT INTO donors VALUES (%s, %s)", (int(userid), 0))
		return 0

	c.execute("SELECT {} FROM donors WHERE id={}".format(str(column), userid))
	return int(c.fetchone()[0])

def formatok(amount):
	#takes amount as string from message.content
	#returns an integer in K
	if (amount[-1:]).lower()=="m":
		return int(float(str(amount[:-1]))*1000)
	elif (amount[-1:]).lower()=="k":
		return int(str(amount[:-1]))
	elif (amount[-1:]).lower()=="b":
		return int(float(str(amount[:-1]))*1000000)
	else:
		return int(float(amount)*1000)

def formatfromk(amount):
	#takes amount as integer in K
	#returns a string to be printed
	if amount>=1000000:
		if len(str(amount))==7:
			return '{0:.3g}'.format(amount*0.000001)+"B"
		elif len(str(amount))==8:
			return '{0:.4g}'.format(amount*0.000001)+"B"
		else:
			return '{0:.5g}'.format(amount*0.000001)+"B"
	elif amount>=1000:
		if len(str(amount))==4:
			return '{0:.3g}'.format(amount*0.001)+"M"
		elif len(str(amount))==5:
			return '{0:.4g}'.format(amount*0.001)+"M"
		elif len(str(amount))==6:
			return '{0:.5g}'.format(amount*0.001)+"M"
	else:
		return str(amount)+"k"
######################################################################################

#Predefined Variables
colors=["A","B","C","D","E","F","0","1","2","3","4","5","6","7","8","9"]
objects=[]
word="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs"
day=int(datetime.datetime.today().day)
bananamode=False




async def my_background_task():
	global people
	await client.wait_until_ready()
	while not client.is_closed:
		# client1 = gspread.authorize(creds)
		# sheet = client1.open("Points System").sheet1
		# sheet.update_cell(27,27,"Authenticated")
		# print("authenticated")
		c.execute("SELECT day FROM giveaway WHERE gnumber=1")
		day=int(c.fetchone()[0])
		print(day)
		if day!=int(datetime.datetime.today().day):
			c.execute("SELECT people FROM giveaway WHERE gnumber=1")
			people=str(c.fetchone()[0]).split("\n")
			embed = discord.Embed(description=random.choice(people)+" has won today's giveaway! DM <@199630284906430465> to claim your **1m**!", color=16724736)
			embed.set_author(name="Daily Holiday Giveaway", icon_url=str(member.avatar_url))
			embed.set_footer(text="Provided by Scandal, Poet, Victarion, and Partners ;)")
			await client.send_message(client.get_channel("510329148003319818"), embed=embed)

			client1 = gspread.authorize(creds)
			sheet = client1.open("Party Room Donations").sheet1
			for counter, i in enumerate(people):
				sheet.update_cell(1+counter, 11+day, str(i))

			c.execute("UPDATE giveaway SET people='{}' WHERE gnumber=1".format(""))
		c.execute("UPDATE giveaway SET day='{}' WHERE gnumber=1".format(int(datetime.datetime.today().day)))
		conn.commit()
		await asyncio.sleep(3600)


@client.event
async def on_ready():
	print("Bot Logged In!");

@client.event
async def on_reaction_add(reaction, user):
	print(str(reaction.message.channel.id))
	print(str(reaction.message.id))
	if str(reaction.message.channel.id)=="559449631604342824" and str(reaction.message.id)=="560301934385430558":
		print(str(reaction.emoji))
		print(reaction.emoji)
		if str(reaction.emoji)=="❗":
			notify=get(reaction.message.server.roles, name='Notify')
			if notify not in user.roles:
				await client.add_roles(user, notify)
		elif str(reaction.emoji)=="🎲":
			games=get(reaction.message.server.roles, name='Games')
			if games not in user.roles:
				await client.add_roles(user, games)
		elif str(reaction.emoji)=="🤑":
			pvm=get(reaction.message.server.roles, name="PvM")
			if pvm not in user.roles:
				await client.add_roles(user, pvm)
		elif str(reaction.emoji)=="⚔":
			pvp=get(reaction.message.server.roles, name="PvP")
			if pvp not in user.roles:
				await client.add_roles(user, pvp)
		elif str(reaction.emoji)=="♿":
			ironman=get(reaction.message.server.roles, name="Ironman Btw")
			if iron not in user.roles:
				await client.add_roles(user, ironman)
	else:
		None

@client.event
async def on_reaction_remove(reaction, user):
	if str(reaction.message.channel.id)=="559449631604342824" and str(reaction.message.id)=="560301934385430558":
		if str(reaction.emoji)=="❗":
			notify=get(reaction.message.server.roles, name='Notify')
			if notify in user.roles:
				await client.remove_roles(user, notify)
		elif str(reaction.emoji)=="🎲":
			games=get(reaction.message.server.roles, name='Games')
			if games in user.roles:
				await client.remove_roles(user, games)
		elif str(reaction.emoji)=="🤑":
			pvm=get(reaction.message.server.roles, name="PvM")
			if pvm in user.roles:
				await client.remove_roles(user, pvm)
		elif str(reaction.emoji)=="⚔":
			pvp=get(reaction.message.server.roles, name="PvP")
			if pvp in user.roles:
				await client.remove_roles(user, pvp)
		elif str(reaction.emoji)=="♿":
			ironman=get(reaction.message.server.roles, name="Ironman Btw")
			if iron in user.roles:
				await client.remove_roles(user, ironman)
	else:
		None

@client.event
async def on_message(message):
	global word,guesses,solved,blank,wrong,word1,people

	if "ram ranch" in (message.content).lower():
		if str(message.author.id)!="426579751583481857":
			if str(message.channel.id)=="499012338670764042" or str(message.channel.id)=="511966876306374666":
				emoji = get(client.get_all_emojis(), name='ramranch')
				sent = await client.send_message(message.channel, "18 naked cowboys in the showers at Ram Ranch! "+str(emoji)+" :shower:")
				await client.add_reaction(sent, emoji)

	if ":goofygang:" in str(message.content):
		gang=get(message.server.roles, name='Goofy Gang')
		if gang not in message.author.roles:
			await client.delete_message(message)

	if "<@&511968689474633728>" in str(message.content):
		if str(message.channel.id)=="499012338670764042" or str(message.channel.id)=="511966876306374666":
			emoji = get(client.get_all_emojis(), name='goofygang')
			sent = await client.send_message(message.channel, str(emoji)+"**Goofy Goobers Gucci Gang!**"+str(emoji))
			await client.add_reaction(sent, emoji)

	if message.channel not in (client.get_server("498848816976363531").channels):
		print(str(message.content)+"\n"+str(message.author))

	#############################################
	if message.content.startswith("!input"):
		print(message.content)
    ###########################################
	elif message.content==("!log"):
		if str(message.author.id)=="199630284906430465":
			await client.send_message(message.channel, "Goodbye!")
			await client.logout()
	##########################################
	elif message.content.startswith("!help") or message.content.startswith("!commands"):
		embed = discord.Embed(description=  "\n  `!colorpicker` - Shows a random color\n" +
											"\n `!start unscramble` - Starts a game where you unscramble a word\n" +
											"\n `!start hangman` - Starts a game of hangman\n" +
											"\n `!random` - Starts a game where you guess a number between 1 and 10\n" +
											"\n `!poll (QUESTION)` - Starts a Yes/No poll with the given question\n" +
											"\n `!donate (AMOUNT)` - Notifys owners you want to donate the given amount (07 gp)\n", color=8926385)

		embed.set_author(name="Party Room Bot Commands", icon_url="https://cdn.discordapp.com/attachments/456981569903525898/462314032934813698/proom.png")
		await client.send_message(message.channel, embed=embed)
		await client.send_message(message.channel, "The commands have been sent to your private messages.")
	#################################################
	elif message.content.startswith('!colorpicker') or message.content.startswith('!colourpicker'):
		color=('')
		for i in range(6):
			color+=random.choice(colors)
		if message.content.startswith("!colorpicker"):
			await client.send_message(message.channel, "Your random color is https://www.colorhexa.com/"+color)
		elif message.content.startswith("!colourpicker"):
			await client.send_message(message.channel, "Your random colour is https://www.colorhexa.com/"+color)
	#########################################
	elif message.content.startswith('!random'):
		await client.send_message(message.channel, 'Guess a number from __**1**__ to __**10**__')

		def guess_check(m):
			return m.content.isdigit()

		guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
		answer = random.randint(1, 10)
		if guess is None:
			fmt = '**Sorry**, you took too long :cry:. It was __**{}**__.'
			await client.send_message(message.channel, fmt.format(answer))
			return
		if int(guess.content) == answer:
			await client.send_message(message.channel, 'You are **correct**! It was indeed __**{}**__!'.format(answer))
		else:
			await client.send_message(message.channel, '**Sorry**, it was actually __**{}**__.'.format(answer))
	#############################################
	elif message.content.startswith("!start unscramble"):
		await client.send_message(message.channel, "The first person to type the unscrambled version of this word wins!")
		word=str(open("words.csv").readlines()[random.randint(0,100)].splitlines()[0])
		characters=[]
		characters+=word
		scrambled=("")
		for i in range(len(characters)):
			letter=random.randint(0, (len(characters)-1))
			scrambled+=str(characters[letter])
			characters.remove(str(characters[letter]))
		await client.send_message(message.channel, "The word is:   "+str(scrambled))
	#########################################
	elif (str(message.content)).lower()==str(word):
		word="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs"
		await client.send_message(message.channel, str(message.author)+" has succesfully unscrambled the word!")
	########################################
	elif message.content.startswith("!skipword"):
		if word!="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs":
			await client.send_message(message.channel, "Too difficult for you? The word was "+str(word)+".")
			word="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs"
		else:
			await client.send_message(message.channel, "There is no word right now. Use \"!start unscramble\" to play.")
	#########################################
	elif message.content.startswith("!emoji"):
		await client.delete_message(message)
		finalmessage=("")
		characters=[]
		characters+=(str(message.content).lower())[7:]
		for i in characters:
			if i==" ":
				finalmessage+=":white_small_square: "
			elif i in "abcdefghijklmnopqrstuvwxyz":
				finalmessage+=":regional_indicator_"+i+": "
			elif i=="!":
				finalmessage+=":grey_exclamation: "
			else:
				None
		await client.send_message(message.channel, finalmessage)
	############################################
	elif message.content.startswith("!poll"):
		message.content=(message.content).title()
		embed = discord.Embed(description="Respond below with 👍 for YES or 👎 for NO", color=16724721)
		embed.set_author(name=str(message.content[6:]), icon_url=str(message.server.icon_url))
		embed.set_footer(text="Polled on: "+str(datetime.datetime.now())[:-7])
		sent = await client.send_message(message.channel, embed=embed)
		await client.add_reaction(sent,"👍")
		await client.add_reaction(sent,"👎")
	#############################################
	elif message.content.startswith("!userinfo"):
		try:
			int(str(message.content[12:13]))
			member=message.server.get_member(message.content[12:30])
		except:
			member=message.server.get_member(message.content[13:31])
		roles=[]
		for i in member.roles:
			if str(i)=="@everyone":
				roles.append("everyone")
			else:
				roles.append(i.name)
		embed = discord.Embed(description=" Name: "+str(member)+"\n"+
											"\nRoles: "+', '.join(roles)+"\n"+
											"\nJoined server on: "+str(member.joined_at).split(" ")[0]+"\n"+
											"\nCreated account on: "+str(member.created_at).split(" ")[0]+"\n"+
											"\nPlaying: "+str(member.game)+"\n", color=8270499)
		embed.set_author(name="Information of "+str(member)[:-5], icon_url=str(member.avatar_url))
		embed.set_footer(text="Spying on people's information isn't very nice...")
		await client.send_message(message.channel, embed=embed)
	##############################################
	elif message.content.startswith("!start hangman"):
		reset()
		word1=str(open("words.csv").readlines()[random.randint(0,100)].splitlines()[0])
		solved+=word1
		for i in range(len(solved)):
			blank+="_"
			blank+=" "
		await client.send_message(message.channel, "```css\nUse !guess (letter or word here)   to guess a letter, or the whole word\nThe first person to guess the word correctly wins!\n\n"+(''.join(blank))+"\n```")
	###################################################
	elif message.content.startswith("!guess"):
		if not blank:
			await client.send_message(message.channel, "There is not a game of hangman going on right now. Use \"!start hangman\" to start a game.")
		else:
			guess=(message.content[7:]).lower()
			if guess == word1.lower():
				reset()
				await client.send_message(message.channel, "<@"+str(message.author.id)+"> has solved the puzzle!")
			elif guess not in solved:
				wrong.append(message.content[7:])
				guesses-=1
				if guesses<1:
					await client.send_message(message.channel, "GAME OVER! You guessed wrong letters/words 6 times. The word was \""+str(word1)+"\".")
					reset()
				else:
					await client.send_message(message.channel, "```css\nUse !guess (letter or word here) to guess a letter, or the whole word\nThe first person to guess the word correctly wins!\n\n"+(''.join(blank))+"\n\nIncorrect guesses left: "+str(guesses)+"\nPrevious incorrect guesses: "+", ".join(wrong)+"\n```")
			else:
				for counter, i in enumerate(solved):
					if i.lower() == guess:
						blank[counter+counter]=guess
				await client.send_message(message.channel, "```css\nUse !guess (letter or word here) to guess a letter, or the whole word\nThe first person to guess the word correctly wins!\n\n"+(''.join(blank))+"\n\nIncorrect guesses left: "+str(guesses)+"\nPrevious incorrect guesses: "+", ".join(wrong)+"\n```")			
	#################################################
	# elif message.content.startswith("!people"):
	# 	if str(message.channel.id)=="499012338670764042":
	# 		c.execute("SELECT people FROM giveaway WHERE gnumber=1")
	# 		people=str(c.fetchone()[0])
	# 		embed = discord.Embed(description="The following people have entered the daily giveaway: "+people, color=8270499)
	# 		embed.set_author(name="Daily Giveaway Participants", icon_url=str(message.server.icon_url))
	# 		embed.set_footer(text="GL Mate")
	# 		await client.send_message(message.channel, embed=embed)
	# 	else:
	# 		await client.send_message(message.channel, "This command can only be used in <#499012338670764042>.")
	# ###################################################
	# elif message.content.startswith("!giveaway"):
	# 	if str(message.channel.id)=="499012338670764042":
	# 		c.execute("SELECT people FROM giveaway WHERE gnumber=1")
	# 		people=str(c.fetchone()[0])
	# 		if "<@"+str(message.author.id)+">" not in people:
	# 			c.execute("UPDATE giveaway SET people='{}' WHERE gnumber=1".format((people+"\n<@"+str(message.author.id)+">")))
	# 			conn.commit()
	# 			await client.send_message(message.channel, "You have been entered in today's **1m** giveaway! Use `!people` to see who else is entered.")
	# 		else:
	# 			await client.send_message(message.channel, "You have already entered the daily giveaway for today!")
	# 	else:
	# 		await client.send_message(message.channel, "This command can only be used in <#499012338670764042>.")
	# ##################################################
	# elif message.content.startswith("!draw"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		c.execute("SELECT people FROM giveaway WHERE gnumber=1")
	# 		people=str(c.fetchone()[0]).split("\n")
	# 		c.execute("SELECT day FROM giveaway WHERE gnumber=1")
	# 		day=int(c.fetchone()[0])

	# 		client1 = gspread.authorize(creds)
	# 		sheet = client1.open("Party Room Donations").sheet1
	# 		for counter, i in enumerate(people):
	# 			sheet.update_cell(1+counter, 11+day, str(i))

	# 		await client.send_message(message.server.get_channel("510329148003319818"), "The winner of the daily giveaway is "+str(random.choice(people))+"! Contact <@199630284906430465> to claim your **1m** 07!")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	# ####################################################
	# elif message.content.startswith("!cleargiveaway"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		c.execute("UPDATE giveaway SET people='{}' WHERE gnumber=1".format(""))
	# 		conn.commit()
	# 		await client.send_message(message.channel, "The daily giveaway has now been cleared.")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	###################################################
	elif message.content.startswith("!say"):
		await client.edit_profile(avatar=str(message.author.avatar_url), username=str(message.author.nick))
		await client.send_message(message.channel, str(message.content)[5:])
		await client.edit_profile(avatar="https://cdn.discordapp.com/attachments/429102082461532160/566075329286897678/proom.png", username="Party Room Bot")






	#############################################
	# elif message.content.startswith("!donate"):
	# 	try:
	# 		client1 = gspread.authorize(creds)
	# 		sheet = client1.open("Party Room Donations").sheet1
	# 		donation=float(message.content[8:-1])
	# 		if donation<1 or str(message.content)[-1:].lower()=="k":
	# 			await client.send_message(message.channel, "Sorry the minimum donation amount is 1m.")
	# 		else:
	# 			if isinstance(donation, float):
	# 				if (donation).is_integer():
	# 					donation=int(donation)
	# 			donation=str(donation)+"M"

	# 			counter=0
	# 			while True:
	# 				if sheet.cell(counter+2, 1).value=="":
	# 					sheet.update_cell(counter+2, 1, str(message.author))
	# 					sheet.update_cell(counter+2, 2, donation)
	# 					sheet.update_cell(counter+2, 3, str(datetime.datetime.now())[:-7])
	# 					sheet.update_cell(counter+2, 4, "No")
	# 					await client.send_message(message.channel, "<@"+str(message.author.id)+">, You have made a donation request of "+donation+". <@404408034694266881> will message you soon to collect your donation.")
	# 					break
	# 				else:
	# 					counter+=1
	# 	except:
	# 		await client.send_message(message.channel, "An **error** has occured. Make sure you use `!donate (AMOUNT OF 07 GP)` - No parenthesis")
	#############################################
	elif message.content.startswith("!donate"):
		try:
			amount=formatok((message.content).split(" ")[1])
			if amount<1000:
				await client.send_message(message.channel, "There is a minimum donation amount of **1M**.")
			else:
				amount=formatfromk(amount)
				await client.send_message(message.server.get_channel("514771727818031104"), "<@"+str(message.author.id)+"> Has made a donation request of "+amount+".")
				await client.send_message(message.channel, "<@"+str(message.author.id)+">, You have made a donation request of "+amount+". A rank will message you soon to collect your donation.")
		except:
			await client.send_message(message.channel, "An **error** has occured. Make sure you use `!donate (AMOUNT OF 07 GP)` - No parenthesis")
	##############################
	elif message.content.startswith("!donations <@"):
		try:
			int(str(message.content).split(" ")[1][2:3])
			member=message.server.get_member(str(message.content).split(" ")[1][2:-1])
		except:
			member=message.server.get_member(str(message.content).split(" ")[1][3:-1])

		donations=formatfromk(getvalue(int(member.id), "donations"))

		embed = discord.Embed(color=16771250)
		embed.set_author(name=(str(member))[:-5]+"'s Total Donations", icon_url=str(member.avatar_url))
		embed.add_field(name="Donations", value=donations, inline=True)
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	###########################
	elif (message.content)==("!donations"):
		donations=formatfromk(getvalue(int(message.author.id), "donations"))
		embed = discord.Embed(color=16771250)
		embed.set_author(name=(str(message.author))[:-5]+"'s Total Donations", icon_url=str(message.author.avatar_url))
		embed.add_field(name="Donations", value=donations, inline=True)
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	#############################
	elif message.content.startswith("!top"):
		if message.content==("!top donations"):
			c.execute("SELECT * From donors ORDER BY donations DESC LIMIT 10")
			donors=c.fetchall()
		words=""
		for counter, i in enumerate(donors):
			userid=i[0]
			donation=formatfromk(i[1])
			words+=(str(counter+1)+". <@"+str(userid)+"> - "+donation+"\n\n")

		embed = discord.Embed(color=16724721, description=words)
		embed.set_author(name="Party Room Top Donations", icon_url=str(message.server.icon_url))
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	#########################
	elif message.content.startswith("!dupdate"):
		#ry:
		if isstaff(message.author.id, message.server.roles, message.author.roles)=="verified":
			try:
				int(str(message.content).split(" ")[1][2:3])
				member=message.server.get_member(str(message.content).split(" ")[1][2:-1])
			except:
				member=message.server.get_member(str(message.content).split(" ")[1][3:-1])

			donation=formatok(str(message.content).split(" ")[2])
			donations=getvalue(int(member.id), "donations")

			if donation+donations>=5000:
				five=get(message.server.roles, name='💰Donator - 5m')
				if five not in message.author.roles:
					await client.add_roles(message.author, five)
			elif donation+donations>=10000:
				ten=get(message.server.roles, name='💰Donator - 10m')
				if ten not in message.author.roles:
					await client.add_roles(message.author, ten)
			elif donation+donations>=25000:
				tf=get(message.server.roles, name='💰Donator - 25m')
				if tf not in message.author.roles:
					await client.add_roles(message.author, tf)
			elif donation+donations>=50000:
				fifty=get(message.server.roles, name='💰Donator - 50m')
				if fifty not in message.author.roles:
					await client.add_roles(message.author, fifty)
			elif donation+donations>=100000:
				hundred=get(message.server.roles, name='💰Donator - 100m')
				if hundred not in message.author.roles:
					await client.add_roles(message.author, hundred)

			c.execute("UPDATE donors SET donations={} WHERE id={}".format(donations+donation, member.id))
			conn.commit()
			await client.send_message(message.channel, "<@"+str(member.id)+">'s donations have been updated.")
		else:
			await client.send_message(message.channel, "Staff only command!")
		#except:
		#	await client.send_message(message.channel, "An **error** has occurred. Make sure you use `!dupdate (@user) (amount)`.")

	##############################################
	# elif message.content.startswith("!rules"):
	# 	await client.delete_message(message)
	# 	embed = discord.Embed(description="__Discord and CC__"+
	# 										"\n**1.** `No racism/sexism or any of the other \"isms\"`"+
	# 										"\n**2.** `No Advertising other Websites or Discord Servers`"+
	# 										"\n**3.** `No spam/flooding or capslock all day`"+
	# 										"\n**4.** `No excessive trolling, tagging, or otherwise bothering people needlessly!`"+
	# 										"\n**5.** `No trolling other communities or advertising in other CCs/Discords!`"+
	# 										"\n**6.** `No begging! Be thankful for the generosity of our hosts` :heart: "+
	# 										"\n**7.** `No advertising RWT`"+
	# 										"\n**8.** `No Pornographic Images or Videos`"+
	# 										"\n**9.** `If you find ranks doing anything they shouldn't be, please report it to a founder`"+
	# 										"\n\n__Giveaway Specific__"+
	# 										"\n**1.** `Only 07 gp/item can be given away, no accounts, irl transfers or services`"+
	# 										"\n**2.** `NO ALTS entering giveaways!`"+
	# 										"\n\n__**Our Mission**__"+
	# 										"\n\n- To provide a safe, welcoming and drama-free space to share your achievements and to create unforgettable moments with people you'll want to call family."+
	# 										"\n\n- To enrich *your* 07 experience! The Party Room is an 07 giveaway server :heart: ", color=12389380)
	# 	embed.set_author(name="Party Room Rules", icon_url=str(message.server.icon_url))
	# 	embed.set_footer(text="Follow the rules so you don't get banned :)")
	# 	await client.send_message(message.channel, embed=embed)
	######################################################
	elif message.content.startswith("!starttrivia"):
		channel=client.get_channel((str(message.content).split(",")[0])[15:-1])
		question=str(message.content).split(",")[1]
		answer=str(message.content).split(",")[2]
		await client.send_message(channel, question)
		await client.send_message(channel, "Keep in mind the answer must be all lowercase!")
		guess = await client.wait_for_message(timeout=30, channel=channel, content=(answer).lower())
		if guess==None:
			await client.send_message(channel, "Reeee, you took too long with no correct answer. Trivia ended.")
		await client.send_message(channel, "<@"+str(guess.author.id)+"> has gotten the trivia correct!")
	####################################################
	elif message.content.startswith("!purge"):
		purged=int((message.content).split(" ")[1])
		mod=get(message.server.roles, name='Moderator')
		if mod in message.author.roles:
			await client.purge_from(message.channel, limit=purged)
			await client.send_message(message.channel, "Deleted **"+str(purged)+"** messages!")
		else:
			await client.send_message(message.channel, "You must have the Moderator role in order to use this command.")
	####################################################
	elif message.content==("!reactions"):
		embed = discord.Embed(description="`React to this message with the given reaction to gain that role`\n"+
											"\n**Notify:** ❗\n"+
											"\n**Games:** 🎲\n"+
											"\n**PvM:** 🤑\n"+
											"\n**PvP:** ⚔\n"+
											"\n**IronMan:** ♿\n", color=16724721)
		embed.set_author(name="Self Assigned Roles", icon_url=str(message.server.icon_url))
		embed.set_footer(text="DM an Admin or Founder with ideas for new roles")
		await client.send_message(message.channel, embed=embed)
	#####################################################
	elif message.content.startswith("!add"):
		if isstaff(message.author.id, message.server.roles, message.author.roles)=="verified":
			event=str(message.content)[5:]+"\n\n|"
			c.execute("SELECT items from data")
			todolist=str(c.fetchone()[0])
			c.execute("UPDATE data SET items='{}'".format(todolist+event))
			conn.commit()
			embed = discord.Embed(description="Item succesfully added to the to-do list! Use `!to-do` to check the list.", color=16724721)
			embed.set_author(name="To-Do List", icon_url=str(message.server.icon_url))
			await client.send_message(message.channel, embed=embed)
		else:
			await client.send_message(message.channel, "Only staff can add items to the to-do list.")
	###################################
	elif message.content=="!to-do":
		c.execute("SELECT items from data")
		todolist=str(c.fetchone()[0])
		printed=""
		for counter, i in enumerate(todolist.split("|")):
			if i=="":
				pass
			else:
				printed+="**"+(str(counter+1)+".** "+i)
		embed = discord.Embed(description=printed, color=16724721)
		embed.set_author(name="Party Room To-Do List", icon_url=str(message.server.icon_url))
		await client.send_message(message.channel, embed=embed)
	####################################
	elif message.content.startswith("!checkoff"):
		if isstaff(message.author.id, message.server.roles, message.author.roles)=="verified":
			number=int((message.content).split(" ")[1])
			c.execute("SELECT items from data")
			todolist=str(c.fetchone()[0])
		else:
			await client.send_message(message.channel, "Only staff can remove items from the to-do list.")
	#####################################
	elif message.content==("!chest"):
		c.execute("SELECT chest from data")
		chest=formatfromk(int(c.fetchone()[0]))
		embed = discord.Embed(description="The Party Room Community Chest currently holds: __**"+chest+"**__", color=16724721)
		embed.set_author(name="Party Room Community Chest", icon_url=str(message.server.icon_url))
		embed.set_thumbnail(url="http://img2.wikia.nocookie.net/__cb20111125181201/runescape/images/a/a8/Mahogany_prize_chest_POH.png")
		await client.send_message(message.channel, embed=embed)
	####################################
	elif message.content.startswith("!chestupdate"):
		if isstaff(message.author.id, message.server.roles, message.author.roles)=="verified":
			amount=formatok((message.content).split(" ")[1])
			c.execute("SELECT chest from data")
			chest=int(c.fetchone()[0])
			c.execute("UPDATE data SET chest={}".format(chest+amount))
			conn.commit()
			embed = discord.Embed(description="Chest has been updated! Use `!chest` to check the chest contents.", color=16724721)
			embed.set_author(name="Community Chest Update", icon_url=str(message.server.icon_url))
			await client.send_message(message.channel, embed=embed)
		else:
			await client.send_message(message.channel, "Only staff can update the community chest.")
	#####################################
	elif message.content.startswith("!giveroles"):
		notify=get(reaction.message.server.roles, name='Notify')
		if notify not in user.roles:
			await client.add_roles(user, notify)

#client.loop.create_task(my_background_task())

Bot_Token = os.environ['TOKEN']
client.run(str(Bot_Token))

#heroku pg:psql postgresql-parallel-32153 --app discord-host
#https://discordapp.com/oauth2/authorize?client_id=426579751583481857&scope=bot&permissions=0