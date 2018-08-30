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
bananamode=False




#async def my_background_task():
#	await client.wait_until_ready()
#	while not client.is_closed:
#		client1 = gspread.authorize(creds)
#		sheet = client1.open("Points System").sheet1
#		sheet.update_cell(27,27,"Authenticated")
#		print("authenticated")
#		await asyncio.sleep(600)




@client.event
async def on_ready():
	print("Bot Logged In!");

@client.event
async def on_reaction_add(reaction, user):
	emoji = str((reaction.emoji))
	if "<:" not in emoji:
		emoji="Other"
	try:
		emojis[emoji]+=1
	except:
		emojis[emoji]=1

@client.event
async def on_reaction_remove(reaction, user):
	if str(reaction.message.author.id)=="294882584201003009":
		await client.send_message(reaction.message.server.get_channel("429385148979609610"), str(reaction.emoji)+" was removed by <@"+str(user.id)+">.")

@client.event
async def on_message(message):
	global words,objects,word,guesses,solved,blank,wrong,word1,bananamode

	if "ram ranch" in (message.content).lower():
		if str(message.author.id)!="426579751583481857":
			if str(message.channel.id)=="420577410099052554":
				emoji = get(client.get_all_emojis(), name='ramranch')
				sent = await client.send_message(message.channel, "18 naked cowboys in the showers at Ram Ranch! "+str(emoji)+" :shower:")
				await client.add_reaction(sent, emoji)

	if bananamode==True:
		emoji = get(client.get_all_emojis(), name='jad')
		await client.add_reaction(message, emoji)

	if message.channel not in (client.get_server("417404138578772008").channels):
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
											"\n `!throw (SOMETHING)` - Throws the given thing into the void\n" +
											"\n `!catch` - Catches something out of the void\n" +
											"\n `!poll (QUESTION)` - Starts a Yes/No poll with the given question\n" +
											"\n `!donate (AMOUNT)` - Tells P Room you want to donate the given amount (07 gp)\n", color=8926385)

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
	elif message.content.startswith("!throw"):
		await client.send_message(message.channel,"You throw "+str(message.content[7:])+" into the deep, dark, empty void.")
		objects.append(str(message.content[7:]))
	#########################################
	elif message.content.startswith("!catch"):
		if len(objects)==0:
			caught="nothing"
		else:
			caught=str(random.choice(objects))
		await client.send_message(message.channel, "You catch a "+caught+" out of the void that someone threw earlier!")
	#########################################
	elif message.content.startswith("!clearthevoid"):
		objects=[]
		await client.send_message(message.channel, "The void is now lonely.")
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
	##########################################
	elif message.content.startswith("!countemoji"):
		try:
			if "<:" not in str(message.content[12:]):
				await client.send_message(message.channel, "\"Other\" has been used "+str(emojis["Other"])+" times. (I can only count custom emojis individually, the natural emojis are counted together as \"Other\")")
			elif "<:" in str(message.content[12:]):
				await client.send_message(message.channel, message.content[12:]+" has been used "+str(emojis[message.content[12:]])+" times.")
		except:
			await client.send_message(message.channel, message.content[12:]+" has never been used before!")
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
	# elif message.content.startswith("!people"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		await client.send_message(message.author, "```css\nThe following people have entered the daily giveaway: "+(', '.join(raffle))+"\n```")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	# ###################################################
	# elif message.content.startswith("!draw"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		await client.send_message(client.get_channel("421064754266636298"), "The winner of the daily giveaway is <@"+str((message.server.get_member_named(random.choice(raffle))).id)+"> ! Contact <@375706874718191619> to claim your prize!")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	# ####################################################
	# elif message.content.startswith("!cleargiveaway"):
	# 	if isstaff(str(message.author.id))=="verified":
	# 		daily={}
	# 		raffle=[]
	# 		await client.send_message(message.channel, "The daily giveaway has now been cleared.")
	# 	else:
	# 		await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
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
		#try:
		client1 = gspread.authorize(creds)
		sheet = client1.open("Party Room Donations").sheet1
		donation=float(message.content[8:-1])
		if donation<1 or str(message.content)[-1:].lower()=="k":
			await client.send_message(message.channel, "Sorry the minimum donation amount is 1m.")
		else:
			donation=donation/1000
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
		#except:
		#	await client.send_message(message.channel, "An **error** has occured. Make sure you use `!donate (AMOUNT OF 07 GP)` - No parenthesis")
	#############################################
	elif message.content.startswith("!spreadsheet"):
		await client.send_message(message.channel, "https://docs.google.com/spreadsheets/d/1nEuPVTyiSYIV44mrswFFbYb5sjCCzCl1BN_m11MLPrA/edit?usp=sharing")
	##############################################



#client.loop.create_task(my_background_task())

Bot_Token = os.environ['TOKEN']
client.run(str(Bot_Token))

#https://discordapp.com/oauth2/authorize?client_id=426579751583481857&scope=bot&permissions=0


