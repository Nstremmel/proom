import discord
import asyncio
import random
from time import sleep
import datetime
import os
import pandas
from discord.utils import get

emojipath = 'proom.csv'
client = discord.Client()




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
		if i.rstrip()==checkedid:
			return "verified"
		else:
			return "no"
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





#fixed !skipword
#can now input words as upercase
#nicer code wtih picking words from words.csv
#spam prevention - 3 seconds








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
async def on_message(message):
	global words,objects,word,guesses,solved,blank,wrong,word1,raffle,daily,bananamode
	if bananamode==True:
		emoji = get(client.get_all_emojis(), name='jad')
		await client.add_reaction(message, emoji)
	if message.channel not in (client.get_server("417404138578772008").channels):
		print(str(message.content)+"\n"+str(message.author))
	else:
		if str(message.author) not in daily:
			staff=False
			for i in open("staff.txt"):
				if str(message.author.id)==i.rstrip():
					staff=True
			if staff==False:
				daily[str(message.author)]=1
		else:
			daily[str(message.author)]+=1
			if str(message.author) not in raffle:
				if daily[str(message.author)]>=5:
					raffle.append(str(message.author))
	#############################################
	#############################################
	if message.content.startswith("!input"):
		print(message.content)
    ###########################################
	elif message.content==("!log"):
		if str(message.author.id)==str(199630284906430465):
			await client.send_message(message.channel, "Goodbye!")
			await client.logout()
	##########################################
	elif message.content.startswith("!send commands"):
		await client.send_message(message.author, "```css\n!colorpicker						  -Gives a link to a random color\n!throw (anything you want)			-Throws your object into the void\n!catch							    -Catches something out of the void\n" \
			"!start unscrambled					-Starts a game where you unscramble letters into a word\n!start hangman						-Starts a game of hangman\n!emoji (sentence)			   	  -Has the bot say your sentence with emoji letters\n" \
			"!countemoji (emoji)			  	 -Displays the number of times someone reacted with that emoji\n!55x2 (amount of points)			  -Gambles an amount of your points (45% chance of doubling your points)\n!points 						      -Displays how many points you have\n" \
			"!spreadsheets						 -Gives a link to a spreadsheet that tracks everyone's points\n```")
		await client.send_message(message.channel, "The commands have been sent to your discord messages.")
	#################################################
	elif message.content.startswith('!colorpicker'):
		color=('')
		for i in range(6):
			color+=random.choice(colors)
		await client.send_message(message.channel, "Your random color is https://www.colorhexa.com/"+color)
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
		#give_points(message.author,10)
		#await client.send_message(message.channel, str(message.author)+" has been given 10 points.")
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
		sent = await client.send_message(message.channel, "```css\n"+str(message.content[6:])+"\n\nRespond below with 👍 for YES, 👎 for NO, or 🤔 for UNSURE/NEUTRAL\n```")
		await client.add_reaction(sent,"👍")
		await client.add_reaction(sent,"👎")
		await client.add_reaction(sent,"🤔")
	#############################################
	elif message.content.startswith("!userinfo"):
		roles=[]
		for i in (message.author.roles):
			roles.append(str(i.id))
		if "417811258642006020" or "438872404157005846" in roles:
			try:
				int(str(message.content[12:13]))
				member=message.server.get_member(message.content[12:30])
			except:
				member=message.server.get_member(message.content[13:31])
			await client.send_message(message.channel, str(member)+" joined the server on "+str(member.joined_at).split(" ")[0])
			await client.send_message(message.channel, str(member)+" created their account on "+str(member.created_at).split(" ")[0])
		else:
			await client.send_message(message.channel, "Sorry charlie, but only admins can use that command.")
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
				#give_points(message.author,10)
				#await client.send_message(message.channel, str(message.author)+" has been given 10 points.")
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
	elif message.content.startswith("!55x2"):
		if int(message.content[6:])<5:
			await client.send_message(message.channel, "The minimum amount you can bet is 5 points.")
		else:
			counter=0
			while True:
				if sheet.cell(counter+2,2).value==str(message.author):
					y=counter+2
					break
				elif sheet.cell(counter+2,2).value=="":
					await client.send_message(message.channel, "<@"+str(message.author.id)+">, you don't have any points.")
					break
				else:
					counter+=1
			if int(sheet.cell(y,3).value)>=int(message.content[6:]):
				roll=random.randint(1,100)
				if roll in range(0,56):
					await client.send_message(message.channel, "```css\n"+str(message.author)+" rolled a "+str(roll)+" and has lost "+str(message.content[6:])+" points.\n```")
					sheet.update_cell(y,3,int(sheet.cell(y,3).value)-int(message.content[6:]))
					sheet.update_cell(y,4, str(now)[:10])
				else:
					await client.send_message(message.channel, "```css\nCongratulations! "+str(message.author)+" rolled a "+str(roll)+" and has won "+str(message.content[6:])+" points.\n```")
					sheet.update_cell(y,3,int(sheet.cell(y,3).value)+int(message.content[6:]))
					sheet.update_cell(y,4, str(now)[:10])
			else:
				await client.send_message(message.channel, "<@"+str(message.author.id)+">, you don't have that many points!")
	#################################################
	elif message.content==("!embed"):
		embed = discord.Embed(title="Party Room Rules:", description="1. Blah\n2. Blah\n3. Blah\n4. Blah", color=0x4E4CB6)
		embed.set_thumbnail(url="http://icons.iconarchive.com/icons/killaaaron/adobe-cc-circles/1024/Adobe-Pr-icon.png")
		await client.send_message(message.channel,embed=embed)
	##############################################
	elif message.content.startswith("!people"):
		if isstaff(str(message.author.id))=="verified":
			await client.send_message(message.author, "```css\nThe following people have entered the daily giveaway: "+(', '.join(raffle))+"\n```")
		else:
			await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
	###################################################
	elif message.content.startswith("!draw"):
		if isstaff(str(message.author.id))=="verified":
			await client.send_message(client.get_channel("421064754266636298"), "The winner of the daily giveaway is <@"+str((message.server.get_member_named(random.choice(raffle))).id)+"> ! Contact <@375706874718191619> to claim your prize!")
		else:
			await client.send_message(message.channel, "You do not have permissions to use that command. Contact <@199630284906430465> if this is a mistake.")
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
	###################################################







	###################################################
	elif message.content==("!points"):
		counter=0
		while True:
			if sheet.cell(counter+2,2).value==str(message.author):
				await client.send_message(message.channel, "<@"+str(message.author.id)+"> has "+str(sheet.cell(counter+2,3).value)+" points.")
				break;
			elif sheet.cell(counter+2,2).value=="":
				sheet.update_cell(counter+2,2, str(message.author))
				sheet.update_cell(counter+2,3, "0")
				sheet.update_cell(2,6, str(int(sheet.cell(2,6).value)+1))
				await client.send_message(message.channel, "<@"+str(message.author.id)+"> has "+str(sheet.cell(counter+2,3).value)+" points.")
				break;
			else:
				counter+=1



	elif  message.content.startswith("!points <@"):
		member=message.server.get_member(message.content[10:28])
		counter=0
		while True:
			if sheet.cell(counter+2,2).value==str(member):
				await client.send_message(message.channel, "<@"+str(message.content[10:28])+"> has "+str(sheet.cell(counter+2,3).value)+" points.")
				break;
			elif sheet.cell(counter+2,2).value=="":
				await client.send_message(message.channel, "That person has not set up their points yet.")
				break;
			else:
				counter+=1
	#############################################
	elif message.content.startswith("!spreadsheet"):
		await client.send_message(message.channel, "https://docs.google.com/spreadsheets/d/1nEuPVTyiSYIV44mrswFFbYb5sjCCzCl1BN_m11MLPrA/edit?usp=sharing")
	##############################################



#client.loop.create_task(my_background_task())

Bot_Token = os.environ['TOKEN']
client.run(str(Bot_Token))

#https://discordapp.com/oauth2/authorize?client_id=426579751583481857&scope=bot&permissions=0


