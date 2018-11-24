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


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client1 = gspread.authorize(creds)
sheet = client1.open("Party Room Donations").sheet1

# import psycopg2
# DATABASE_URL = os.environ['postgres://rbcuezaukicjrw:a4f881eb70b24835e7244c57842f479d569d7dd0ad51209b823620ff31057e3a@ec2-50-16-196-238.compute-1.amazonaws.com:5432/d2tedbh2aiu1ov']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# conn.Close()


def reset():
	global guesses,solved,blank,wrong,word1
	guesses=6
	solved=[]
	blank=[]
	wrong=[]
	word1="skdfjgslddddfgggsdflkgashdflkjhesrflskjerhfs;eroifaasdfalwkefjhs"

def isstaff(checkedid):
	for i in open("staff.txt"):
		if str(i.split(" ")[0])==str(checkedid):
			return "verified"



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
emojis={}
raffle=[]
daily={}
giveaway=[]
day=int(datetime.datetime.today().day)
bananamode=False




async def my_background_task():
	await client.wait_until_ready()
	while not client.is_closed:
		# client1 = gspread.authorize(creds)
		# sheet = client1.open("Points System").sheet1
		# sheet.update_cell(27,27,"Authenticated")
		# print("authenticated")
		if int(day)!=int(datetime.datetime.today().day):
			print("Do shit")
		day=int(datetime.datetime.today().day)
		await asyncio.sleep(600)




@client.event
async def on_ready():
	print("Bot Logged In!");

@client.event
async def on_reaction_add(reaction, user):
	None

@client.event
async def on_reaction_remove(reaction, user):
	if str(reaction.message.author.id)=="294882584201003009":
		await client.send_message(reaction.message.server.get_channel("511587300136845317"), str(reaction.emoji)+" was removed by <@"+str(user.id)+">.")

@client.event
async def on_message(message):
	global word,guesses,solved,blank,wrong,word1,bananamode

	if "ram ranch" in (message.content).lower():
		if str(message.author.id)!="426579751583481857":
			if str(message.channel.id)=="499012338670764042":
				emoji = get(client.get_all_emojis(), name='ramranch')
				sent = await client.send_message(message.channel, "18 naked cowboys in the showers at Ram Ranch! "+str(emoji)+" :shower:")
				await client.add_reaction(sent, emoji)

	# if bananamode==True:
	# 	emoji = get(client.get_all_emojis(), name='jad')
	# 	await client.add_reaction(message, emoji)

	if message.channel not in (client.get_server("498848816976363531").channels):
		print(str(message.content)+"\n"+str(message.author))

	#############################################
	if message.content.startswith("!input"):
		print(message.content)
    ###########################################
	elif message.content==("!log"):
		if str(message.author.id)==str(199630284906430465):
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
		await client.send_message(message.author, embed=embed)
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
		await client.delete_message(message)
		sent = await client.send_message(message.channel, "```css\n"+str(message.content[6:])+"\n\nRespond below with 👍 for YES, 👎 for NO, or 🤔 for UNSURE/NEUTRAL\n```")
		await client.add_reaction(sent,"👍")
		await client.add_reaction(sent,"👎")
		await client.add_reaction(sent,"🤔")
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
	elif message.content.startswith("!people"):
		if isstaff(str(message.author.id))=="verified":
			await client.send_message(message.author, "```css\nThe following people have entered the daily giveaway: "+(', '.join(raffle))+"\n```")
		else:
			await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	###################################################
	# elif message.content.startswith("!draw"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		await client.send_message(client.get_channel("421064754266636298"), "The winner of the daily giveaway is <@"+str((message.server.get_member_named(random.choice(raffle))).id)+"> ! Contact <@375706874718191619> to claim your prize!")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	####################################################
	elif message.content.startswith("!cleargiveaway"):
		if isstaff(str(message.author.id))=="verified":
			daily={}
			raffle=[]
			await client.send_message(message.channel, "The daily giveaway has now been cleared.")
		else:
			await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	####################################################
	elif message.content.startswith("!jad on"):
		bananamode=True
		await client.send_message(message.channel, "Fight Cave Initiated! It's time for <@293268085245214721> to fail again! <:jad:461287872293503027>")
	##################################################
	elif message.content.startswith("!jad off"):
		bananamode=False
		await client.send_message(message.channel, "You have lost to the almighty JAD <:jad:461287872293503027>")
	###################################################
	elif message.content.startswith("!say"):
		await client.edit_profile(avatar=message.author.avatar_url, username=str(message.author.nick))
		print (str(message.author.avatar_url))






	#############################################
	elif message.content.startswith("!donate"):
		try:
			client1 = gspread.authorize(creds)
			sheet = client1.open("Party Room Donations").sheet1
			donation=float(message.content[8:-1])
			if donation<1 or str(message.content)[-1:].lower()=="k":
				await client.send_message(message.channel, "Sorry the minimum donation amount is 1m.")
			else:
				if isinstance(donation, float):
					if (donation).is_integer():
						donation=int(donation)
				donation=str(donation)+"M"

				counter=0
				while True:
					if sheet.cell(counter+2, 1).value=="":
						sheet.update_cell(counter+2, 1, str(message.author))
						sheet.update_cell(counter+2, 2, donation)
						sheet.update_cell(counter+2, 3, str(datetime.datetime.now())[:-7])
						sheet.update_cell(counter+2, 4, "No")
						await client.send_message(message.channel, "<@"+str(message.author.id)+">, You have made a donation request of "+donation+". <@404408034694266881> will message you soon to collect your donation.")
						break
					else:
						counter+=1
		except:
			await client.send_message(message.channel, "An **error** has occured. Make sure you use `!donate (AMOUNT OF 07 GP)` - No parenthesis")
	#############################################
	elif message.content.startswith("!donate"):
		try:
			amount=(message.content).split(" ")[1]
			if (amount[-1:]).lower()=="m":
				donation=int(float(str(amount[:-1]))*1000)
			elif (amount[-1:]).lower()=="k":
				donation=int(str(amount[:-1]))
			else:
				donation=int(float(amount)*1000)

			await client.send_message(message.server.get_channel("478634423718248449"), "<@"+str(message.author.id)+"> Has made a donation request of "+amount+".")
			await client.send_message(message.channel, "<@"+str(message.author.id)+">, You have made a donation request of "+amount+". A rank will message you soon to collect your donation.")
		except:
			await client.send_message(message.channel, "An **error** has occured. Make sure you use `!donate (AMOUNT OF 07 GP)` - No parenthesis")
	#############################
	elif message.content.startswith("!donations <@"):
		try:
			int(str(message.content).split(" ")[1][2:3])
			member=message.server.get_member(str(message.content).split(" ")[1][2:-1])
		except:
			member=message.server.get_member(str(message.content).split(" ")[1][3:-1])

		donations=getvalue(int(member.id), "donations")
		if donations>=10000:
			if len(str(donations))==5:
				donations='{0:.4g}'.format(donations*0.001)+"M"
			elif len(str(donations))==6:
				donations='{0:.5g}'.format(donations*0.001)+"M"
		else:
			donations=str(donations)+"k"

		embed = discord.Embed(color=16771250)
		embed.set_author(name=(str(member))[:-5]+"'s Total Donations", icon_url=str(member.avatar_url))
		embed.add_field(name="Donations", value=donations, inline=True)
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	##########################
	elif (message.content)==("!donations"):
		donations=getvalue(int(message.author.id), "donations")
		if donations>=10000:
			if len(str(donations))==5:
				donations='{0:.4g}'.format(donations*0.001)+"M"
			elif len(str(donations))==6:
				donations='{0:.5g}'.format(donations*0.001)+"M"
		else:
			donations=str(donations)+"k"

		embed = discord.Embed(color=16771250)
		embed.set_author(name=(str(message.author))[:-5]+"'s Total Donations", icon_url=str(message.author.avatar_url))
		embed.add_field(name="Donations", value=donations, inline=True)
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	############################
	elif message.content.startswith("!top donations"):
		c.execute("SELECT * From rsmoney ORDER BY donations DESC LIMIT 10")
		donors=c.fetchall()
		words=""
		for counter, i in enumerate(donors):
			userid=i[0]
			donation=i[4]

			if donation>=10000:
				if len(str(donation))==5:
					donation='{0:.4g}'.format(donation*0.001)+"M"
				elif len(str(donation))==6:
					donation='{0:.5g}'.format(donation*0.001)+"M"
			else:
				donation=str(donation)+"k"

			words+=(str(counter+1)+". "+str(message.server.get_member(str(userid)))+" - "+donation+"\n\n")

		embed = discord.Embed(color=16771250, description=words)
		embed.set_author(name="RSGiveaways Top Donations", icon_url=str(message.author.avatar_url))
		embed.set_footer(text="Donations checked on: "+str(datetime.datetime.now())[:-7])
		await client.send_message(message.channel, embed=embed)
	#########################
	elif message.content.startswith("!dupdate"):
		try:
			if (message.channel.id)=="478634423718248449":
				amount=str(message.content).split(" ")[2]

				if (amount[-1:]).lower()=="m":
					donation=int(float(str(amount[:-1]))*1000)
				elif (amount[-1:]).lower()=="k":
					donation=int(str(amount[:-1]))
				else:
					donation=int(float(amount)*1000)

				try:
					int(str(message.content).split(" ")[1][2:3])
					member=message.server.get_member(str(message.content).split(" ")[1][2:-1])
				except:
					member=message.server.get_member(str(message.content).split(" ")[1][3:-1])

				donations=getvalue(int(member.id), "donations")
				c.execute("UPDATE rsmoney SET donations={} WHERE id={}".format(donations+donation, member.id))
				conn.commit()
				member=message.server.get_member(str(member.id))
				await client.send_message(message.channel, str(member)+"'s donations have been updated.")
			else:
				None
		except:
			await client.send_message(message.channel, "An **error** has occurred. Make sure you use `!dupdate (@user) (amount)`.")

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
	################################################
	elif message.content.startswith("!notify-on"):
		notify=get(message.server.roles, name='Notify')
		if notify not in message.author.roles:
			await client.add_roles(message.author, notify)
			await client.send_message(message.author, "You will now be notified for giveaways. :tada: ")
		else:
			await client.send_message(message.channel, "You already have that role! Use `!notify-off` to remove it.")

	elif message.content.startswith("!notify-off"):
		notify=get(message.server.roles, name='Notify')
		if notify in message.author.roles:
			await client.remove_roles(message.author, notify)
			await client.send_message(message.author, "You will no longer be notified for giveaways.")
			await client.delete_message(message)
		else:
			await client.send_message(message.channel, "You don't currently have this role. Use `!notify-on` to add it.")
	#################################################




	
#client.loop.create_task(my_background_task())

Bot_Token = os.environ['TOKEN']
client.run(str(Bot_Token))

#https://discordapp.com/oauth2/authorize?client_id=426579751583481857&scope=bot&permissions=0


