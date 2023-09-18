import discord
import responses
from discord.ext import commands

DELETE = True
CHANNEL_ID = 0
FILENAME = "data.txt"

def get_channel(client, channel_id):
    channel_real = None
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.id == channel_id:
                channel_real = channel
    return channel_real


async def delete_message(channel,msg):
    try: # Error Check
        await msg.delete() # Deleting
    except Exception as e: # Error Check
        print(e)


async def change_nickname(member, nickname):
    try:
        await member.edit(nick=nickname)
    except Exception as e: # Probably admin
        print(e)


async def apply_response(user, member, guild, client, resp, stat):
    if resp == "CREATE":
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel= False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True, view_channel=True, stream=True),
            client.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        print("searching stat2:" + str(stat[2]))
        t_channel = discord.utils.get(guild.text_channels, name=stat[2])
        v_channel = discord.utils.get(guild.voice_channels, name=stat[2])

        if t_channel:
            await t_channel.set_permissions(member, read_messages=True, send_messages=True)
        else:
            await guild.create_text_channel(stat[2], overwrites=overwrites)
        if v_channel:
            await v_channel.set_permissions(member, connect=True, speak=True, view_channel=True, stream=True)
        else:
            await guild.create_voice_channel(stat[2], overwrites=overwrites)
        nick = stat[0] + " " + stat[1]
        await change_nickname(member=member, nickname=nick)
    elif resp == "ADD":
        t_channel = discord.utils.get(guild.text_channels, name=stat[2])
        v_channel = discord.utils.get(guild.voice_channels, name=stat[2])
        
        await t_channel.set_permissions(member, read_messages=True, send_messages=True, view_channel=True)
        await v_channel.set_permissions(member, connect=True, speak=True, view_channel=True, stream=True)
        nick = stat[0] + " " + stat[1]
        await change_nickname(member=member, nickname=nick)




async def get_history_of_channel(channel_id, client, char:str, filename:str, dele:bool):
    channel = get_channel(client, channel_id=channel_id)
    if channel == None:
        return
    
    guild = channel.guild

    messages = []

    async for message in channel.history(limit=200):
        if message.author != client.user:
            user = message.author
            resp, stat = responses.handle_response(message.content, char, filename)
            member = guild.get_member(user.id)
            await apply_response(user, member, guild, client, resp, stat)
        messages.append(message)
    if dele:
        for message in messages:
            await delete_message(channel=channel, msg=message)



def run(argv, token):
    """ FORMAT OF PROGRAM: 
        USE: main.py <channel_id> <filename>
        In Case of Non message deletion: main.py <channel_id> <filename> nodelete
        """
    TOKEN = token
    intents=discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    intents.members = True
    CHAR = ' '

    if TOKEN == "":
        print("TOKEN NEEDED. Go to main.py and assign the bot's token to the token variable")
        return
    if len(argv) >= 3:
        CHANNEL_ID = int(argv[1])
        FILENAME = argv[2]
        if len(argv) > 3:
            print("not deleting")
            DELETE= False
    else:
        print("Incorrect run format:")
        print("Correct: python3 main.py <channel_id> <filename> <optional:nodelete>")
        return

    
    bot = commands.Bot(command_prefix='?', intents=intents)
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now ready')
        await get_history_of_channel(CHANNEL_ID, bot, CHAR, FILENAME, DELETE)


    @bot.event
    async def on_message(message):
        print("New message: " + message.content)
        channelIDsToListen = [ CHANNEL_ID ] # put the channels that you want to listen to here

        #if message.channel.id in channelIDsToListen:

            #if message.content != "" and message.author != bot.user:
                #user = message.author
                #resp, stat = responses.handle_response(message.content, CHAR, FILENAME)
                #member = message.channel.guild.get_member(user.id)
                #await apply_response(user, member, message.channel.guild, bot, resp, stat)
                #await delete_message(channel=message.channel, msg=message)
                #pass

            

    bot.run(TOKEN)
