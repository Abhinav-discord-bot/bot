import discord
from googlesearch import search
import mysql.connector

mydb = mysql.connector.connect(
  host="us-cdbr-iron-east-01.cleardb.net",
  user="baffdee0ce0ab6",
  passwd="c1cebe337ed78ed",
  database="heroku_f35cac914d4d4d2"
)

mycursor = mydb.cursor()

TOKEN = 'NjkxNjY2ODU3MDEwMjY2MjE0.XnjTmw.zkTEwQm4g97TQudy3CQY2b-cTSU'

client = discord.Client()
query=''

@client.event
async def on_message(message):
		
	if message.content.startswith('hi'):
		await message.channel.send('hey')
	if message.content.startswith('!google '):
		a=message.content[8:]
		sql = """INSERT INTO Recent_Search(search) VALUES('%s')"""%a
		mycursor.execute(sql)
		mydb.commit()
		for j in search(query=message.content[8:], tld="com", num=5, stop=5, pause=2): 
			await message.channel.send(j)
	if message.content.startswith('!recent game'):
		mycursor.execute("SELECT search FROM Recent_Search ORDER BY id DESC LIMIT 2")
		myresult = mycursor.fetchall()
		for x in myresult:
			b=str(x)
			await message.channel.send(b[2:-3])
		
client.run(TOKEN)