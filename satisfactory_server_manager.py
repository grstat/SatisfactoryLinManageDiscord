import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

#Load from the .env file
load_dotenv()

#Set intents
intents = discord.Intents.default()
intents.message_content = True

#Discord Client
ficsitbot = discord.Client(intents=intents)

@ficsitbot.event
async def on_ready():
  #Just for logging
  print('[FICSIT BOT] We have logged in as {0.user}'.format(ficsitbot))
  #You can issue a hello message here, just copy the channel ID from
  #the channel you wish to use and paste it in the get_channel method
  #otherwise comment out the next 3 lines
  ficsit_hello = "```I have arrived!\nUse: !ficsit to see a list of possible commands```"
  factory_channel = ficsitbot.get_channel(YOUR CHANNEL ID INTEGER)
  await factory_channel.send(ficsit_hello)

@ficsitbot.event
async def on_message(message):
  #Ignore anything the bot says
  if message.author == ficsitbot.user:
    return
  #Unless it starts with ! who cares
  if message.content.startswith('!'):
      #Lower case everything helps eval
      msg = message.content.lower()
      if msg.startswith('!ficsit'):
        #Get what has been passed, this could be better
        #as more than one comamand can be passed but
        #they override each other in this order
        #stat, stop, start, bounce
        stat_count = msg.count('stat')
        stop_count = msg.count('stop')
        start_count = msg.count('start')
        bounce_count = msg.count('bounce')
        bounce_confirm = msg.count('yes')
        #Get info about the author of the message
        author_id = message.author.id
        author_name = message.author.name
        author_roles = message.author.roles
        #Var to test against the server role
        #Just loop through the user's roles and see if
        #They have permission to talk to the bot based on
        #the role string provided
        can_command = 0
        for role in author_roles:
          name_check = role.name.lower()
          if "YOUR ROLE NAME HERE" in name_check:
            can_command = 1
            role_info = "[FICSIT BOT] Found matching {} for user {} ID: {}"
            print(role_info.format(name_check, author_name, author_id))
            break
        #If they don't have permission, let em know and get out
        if can_command == 0:
          inform_str = "```Sorry {} you don't have permission to command me.\nYou must request permission from the server gods for access```"
          await message.channel.send(inform_str.format(author_name))
          return
        #Just logging can be removed
        out_str = "[FICSIT BOT] ID: {} User: {} Stat: {} Stop: {} Start: {} Bounce: {}"
        print(out_str.format(author_id, author_name, stat_count, stop_count, start_count, bounce_count))

        #Stat message
        if stat_count > 0:
          run_stat = os.popen('systemctl status satisfactory | grep Active').read()
          running_count = run_stat.count('running')
          if running_count > 0:
            #Server is running, post useful information about the process
            stat_str = os.popen('systemctl status satisfactory | grep -A 6 satisfactory.service | grep -B 4 Memory').read()
            out_str = "```- Server is Online and Running -\n{}```"
            await message.channel.send(out_str.format(stat_str))
            return
          #Server is offline, post the info
          stat_str = os.popen('systemctl status satisfactory | grep -A 2 satisfactory.service | grep -B 2 Active').read()
          out_str = "```- Server is Offline -\n{}```"
          await message.channel.send(out_str.format(stat_str))
          return

        #Stop message
        if stop_count > 0:
          #Check to make sure the server is running before issuing stop
          run_stat = os.popen('systemctl status satisfactory | grep Active').read()
          running_count = run_stat.count('running')
          if running_count > 0:
            #Server is up so run the stop on it
            stat_str = os.system('systemctl stop satisfactory')
            stop_str = "```Requested server stop, return code was: {}\nZero for success, anything else is failure```"
            await message.channel.send(stop_str.format(stat_str))
            return
          stop_str = "```Server is already in-active\nIgnoring stop command```"
          await message.channel.send(stop_str)
          return

        #Start message
        if start_count > 0:
          #Make sure the server isn't already running before issuing start
          stat_str = os.popen('systemctl status satisfactory | grep Active').read()
          running_count = stat_str.count('running')
          if running_count > 0:
            #Server is running, start is pointless
            await message.channel.send("```Server is already active and running\nIgnoring start command```")
            return
          #Server is not active, issue start
          start_str = "```Requested server start\nReturn code was: {}\nZero for success, anything else is failure```"
          stat_str = os.system('systemctl start satisfactory')
          await message.channel.send(start_str.format(stat_str))
          return

        #Reboot message, must have extra yes in there
        if bounce_count > 0:
          if bounce_confirm > 0:
            #Bounce yes has been issued, reboot the server
            out_msg = "```Reboot command has been sent to the system\nI will die with it! Await my arrival....```"
            await message.channel.send(out_msg)
            reboot_str = os.system('systemctl reboot')
            return
          #Notify user they need to issue yes if they want to bounce the system
          bounce_str = "```If you really think the system needs to be rebooted follow up with !ficsit bounce yes```"
          await message.channel.send(bounce_str)
          return

        #Everything else is ignored and help is shown
        help_str = "```Available commands:\n------------------------\nStat (get server status)\nStop (kill server)\nStart (Start server)\nBounce (Reboot server)```"
        await message.channel.send(help_str.strip())
        return

#Uses the .env file to get the token
#make sure .env exists in the directory and DIS_TOKEN='YOUR APP TOKEN'
ficsitbot.run(os.getenv('DIS_TOKEN'))