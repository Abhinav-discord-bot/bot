import discord
from googlesearch import search
import mysql.connector

mydb = mysql.connector.connect(					  #Connecting to Mysql server(ClearDb server by heroku) with host,username and password
  host="us-cdbr-iron-east-01.cleardb.net",		  #and storing the connection object in variable mydb
  user="baffdee0ce0ab6",
  passwd="c1cebe337ed78ed",
  database="heroku_f35cac914d4d4d2"
)

mycursor = mydb.cursor() 						 #Creating a object using connection's cursor method

TOKEN = 'NjkxNjY2ODU3MDEwMjY2MjE0.XnzZ9w.UUdW1kaCDd2jm8vX61OSnO86JJU'      #Token of created bot

client = discord.Client()     					 #Creating a client connection that connects to discord 
query=''

@client.event									 #Here it is a decorator which means same as on_message=client.event(on_message),
												 #event method of class client with argument as on_message
async def on_message(message):					 #creating a async function. This occurs when a message is posted in a channel that the bot has access to. 
		
	if message.content.startswith('hi'):		 #Checking if the posted message starts with 'hi' then bot will return 'hey'
		await message.channel.send('hey')
	if message.content.startswith('!google '):	 #Checking if the posted message starts with '!google '
		a=message.content[8:]
		sql = """INSERT INTO Recent_Search(search) VALUES('%s')"""%a       #Taking the message content after 8th word and inserting it into a mysql table Recent _Search
		mycursor.execute(sql)					 #Execurting the sql command and commiting it into the db
		mydb.commit()
		for j in search(query=message.content[8:], tld="com", num=5, stop=5, pause=2):        #Looping the user query result from google.com search and displaying the initial 5 results
			await message.channel.send(j)			
	if message.content.startswith('!recent game'):							#Checking if the posted message starts with '!recent game' then the bot will query in the database table 
		mycursor.execute("SELECT search FROM Recent_Search ORDER BY id DESC LIMIT 2")		#and return the last updated two records with the help of primary key(id) which is 
		myresult = mycursor.fetchall()														#automaticaly gets incremented with 1
		for x in myresult:
			b=str(x)																		#Converting the tuple returned by DB query into string so that we can remove the braces('(')
			await message.channel.send(b[2:-3])
		
client.run(TOKEN)								 #Running our bot by passing bot token