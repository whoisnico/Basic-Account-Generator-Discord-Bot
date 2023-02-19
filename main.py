import asyncio
import datetime
from lib2to3.pytree import convert
import time
from timeit import repeat
import disnake,json,os,random
from disnake.ext import commands


credits = """

 /$$    /$$                                    /$$          
| $$   | $$                                   | $$          
| $$   | $$ /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$$ /$$   /$$
|  $$ / $$//$$__  $$| $$__  $$ |____  $$ /$$__  $$| $$  | $$
 \  $$ $$/| $$$$$$$$| $$  \ $$  /$$$$$$$| $$  | $$| $$  | $$
  \  $$$/ | $$_____/| $$  | $$ /$$__  $$| $$  | $$| $$  | $$
   \  $/  |  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$
    \_/    \_______/|__/  |__/ \_______/ \_______/ \____  $$
                                                   /$$  | $$
                                                  |  $$$$$$/
                                                   \______/ 
GitHub - nicotrixxel
Twitter - nicotrixxel
Discord - discord.gg/venady

"""

print(credits)
time.sleep(1) #just fun cooldown lol
print("Bot is starting...")

time.sleep(1) #just fun cooldown lol

with open("config.json") as file:
    config = json.load(file)
    token = config["token"]
    prefix = config["prefix"]
    cmd_channel = config["cmd_channel"]

print("-> Config loaded")


clientIntents = disnake.Intents.default()
clientIntents.message_content = True
clientIntents.members = True
venady = commands.Bot(command_prefix=prefix , intents=clientIntents, help_command=None)

time.sleep(1) #just fun cooldown lol

print("-> Intents loaded")
time.sleep(1) #just fun cooldown lol
print("-> Bot is now online \n") #starting end

#----------------------------------------Bot Events----------------------------------------


@venady.event
async def on_ready():
    await venady.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.playing,
            name=f'*by gg/venady | -help'),
            status=disnake.Status.online)


@venady.event
async def on_command_error(ctx, error): #Global Cooldown for free Generator
    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after)
        await ctx.message.reply(f"Server Global Cooldown! Please try again in {remaining}s")

#----------------------------------------Generator Commands----------------------------------------
@venady.command() #free command
@commands.cooldown(1, 5, commands.BucketType.guild)
async def gen(ctx, stock=None):
        server_name = ctx.guild.name
        if ctx.channel == cmd_channel:
            if stock == None:
                await ctx.message.reply(f"Use `{prefix}gen [account type]`")
                print(f"{ctx.author.name} used (free) -> Error [No Account Type]")
            else:
                stock = stock.lower()+".txt" 
                if stock not in os.listdir(f"Accounts//"): 
                    await ctx.message.reply(f"Account does not exist. `{prefix}stock`")
                    print(f"{ctx.author.account} used (free {stock}) -> Error [No Exist Account Type]".replace(".txt",""))
                else:
                    with open(f"Accounts//"+stock) as file:
                        lines = file.read().splitlines()
                    if len(lines) == 0: 
                        await ctx.send("These accounts are out of stock") 
                        print(f"{ctx.author.name} used (free {stock}) -> Error [No Account Type Stock]".replace(".txt",""))
                    else:
                        with open(f"Accounts//"+stock) as file:
                            account = random.choice(lines)
                        try:
                            em = disnake.Embed(title = " ", description = f"*This is your generated account* \n `{str(account)}` \n *The Order is Username:Password*", color = 0xFFFFFF, timestamp= inter.message.created_at)
                            em.set_footer(text = f"{server_name}")
                            em.set_author(icon_url = "https://media.discordapp.net/attachments/1007664686679986186/1028340335732076634/venady_logo.png?width=676&height=676", name = f"{server_name} Account Generator")

                            delay = [
                                1,
                                6,
                                9,
                                10,
                                5,
                                3
                            ]
                            time.sleep(random.choice(delay))
                            await ctx.author.send(embed=em)
                            print(f"{ctx.author.name} used (gen {stock}) -> Successful | {server_name}".replace(".txt",""))
                        except: 
                            await ctx.message.reply("Failed to send! Turn on ur direct messages")
                            print(f"{ctx.author.name} used (free {stock}) -> Error [Failed Sending / DMS OFF]".replace(".txt",""))
                        else: 
                            await ctx.message.reply("Sent the account to your DMS!")
                            with open(f"Accounts//"+stock,"w") as file:
                                file.write("") #Clear the file
                            with open(f"Accounts//"+stock,"a") as file:
                                for line in lines:
                                    if line != account: 
                                        file.write(line+"\n") 
        else:
            await ctx.message.reply(f"Wrong Channel! Use <#{cmd_channel}>")
            print(f"{ctx.author.name} used (free {stock}) -> Error [Wrong Channel]".replace(".txt",""))



@venady.command() # Stock command
async def stock(inter:disnake.ApplicationCommandInteraction):
    """show you the server stock"""
    id = inter.guild.id
    server_name = inter.guild.name
    stockmenu = disnake.Embed(title="Account Stock",description="**Generator 1** \n", color = 0xFFFFFF, timestamp= datetime.datetime.utcnow()) # Define the embed
    stockmenu.set_footer(text =f"{server_name}")
    stockmenu
    for filename in os.listdir(f"Accounts/"):
        with open(f"Accounts//{filename}") as f: 
            ammount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") 
            stockmenu.description += f"*{name}* - {ammount}\n"
    await inter.send(embed=stockmenu)

#---------------------------------------- Mod Commands----------------------------------------
@venady.command() #help command
async def help(ctx):
    """show you all commands."""
    server_name = ctx.guild.name
    help = disnake.Embed(title="Venady Help",description=f" ", color = 0xffffff, timestamp=datetime.datetime.utcnow())
    help.set_footer(text =f"{server_name}", icon_url="https://media.discordapp.net/attachments/1007664686679986186/1028340335732076634/venady_logo.png?width=676&height=676")


    view = disnake.ui.View()
    item = disnake.ui.Button(style=disnake.ButtonStyle.green, label="Support", url="https://discord.gg/wATBPDjWBP")
    view.add_item(item=item)

    item2 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Invite Me", url="https://discord.com/oauth2/authorize?client_id=1055579817069776906&permissions=8&scope=bot%20applications.commands")
    view.add_item(item=item2)



#--------------------------------------------------------------------------------1 Help Menu
    help.add_field(name="Generators Commands", value=f"""> `{prefix}gen`
    > Use this to generate!


    > `/stock`
    > Show you the account stock!
    """)
#------------------------------------------------------------------------------- 2 Help Menu
    help.add_field(name="Other Commands", value=f"""> `{prefix}help`
    > Show you this Message!
    """)

    await ctx.send(embed=help, view=view)
    print(f"{ctx.author.name} used (help) -> Successfull")


@venady.command() #invite command
async def invite(ctx):

    await ctx.message.reply("Server Invite: https://discord.gg/venady \n Bot invite: https://bit.ly/3WlC3Er \n Sourcecode: https://github.com/nicotrixxel")
    


@venady.command() #test command
async def test(ctx):
   
    await ctx.message.reply("Private Command :P |Bot by discord.gg/venady")
    print(f"{ctx.author.name} used (test) -> Successful")

venady.run(token)
