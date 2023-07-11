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
print("Bot is starting...")

time.sleep(1) #just fun cooldown lol

with open("config.json") as file:
    config = json.load(file)
    token = config["token"]
    cooldown = config["cooldown"]
    cmd_channel = config["cmd_channel"]

print("-> Config loaded")

prefix = "-"
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
            name=f'*by @whosnico & gg/venady| /help'),
            status=disnake.Status.online)



#----------------------------------------Generator Commands----------------------------------------
@venady.slash_command()
@commands.cooldown(1, cooldown, commands.BucketType.member)
async def gen(inter, stock):
    user = inter.author
    server_name = inter.guild.name
    if inter.channel.id != cmd_channel:
        await inter.send(f"Wrong Channel! Use <#{cmd_channel}>")
        print(f"{inter.author.name} used (free {stock}) -> Error [Wrong Channel]".replace(".txt",""))
        return
    stock = stock.lower() + ".txt"
    if stock not in os.listdir(f"Accounts//"):
        await inter.send(f"Account does not exist. `{prefix}stock`")
        print(f"{inter.author.name} used (free {stock}) -> Error [No Exist Account Type]".replace(".txt",""))
        return
    with open(f"Accounts//"+stock) as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            await inter.send("These accounts are out of stock")
            print(f"{inter.author.name} used (free {stock}) -> Error [No Account Type Stock]".replace(".txt",""))
            return
    with open(f"Accounts//"+stock) as file:
        account = random.choice(lines)
    em = disnake.Embed(title = " ", description = f"*This is your generated account* \n `{str(account)}` \n *The Order is Username:Password*", color = 0xFFFFFF, timestamp= datetime.datetime.utcnow())
    em.set_footer(text = f"{server_name}")
    em.set_author(icon_url = "https://media.discordapp.net/attachments/1007664686679986186/1028340335732076634/venady_logo.png?width=676&height=676", name = f"{server_name} Account Generator")
    await user.send(embed=em)
    print(f"{inter.author.name} used (gen {stock}) -> Successful | {server_name}".replace(".txt",""))

    await inter.send("Sent the account to your DMS!")
    with open("Accounts//" + stock, "w", encoding='utf-8') as file:
        file.write("")  # Leeren der Datei
    with open("Accounts//" + stock, "a", encoding='utf-8') as file:
        for line in lines:
            if line != account:
                file.write(line + "\n")

                
@gen.error
async def gen_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = disnake.utils.format_dt(
            disnake.utils.utcnow() + datetime.timedelta(seconds=error.retry_after), "R"
        )
        return await inter.response.send_message(
            f"This command is on cooldown, retry {retry_after}",
            ephemeral=True
        )

    raise error


@venady.slash_command() # Stock command
async def stock(inter:disnake.ApplicationCommandInteraction):
    """show you the server stock"""
    id = inter.guild.id
    server_name = inter.guild.name
    stockmenu = disnake.Embed(title="Account Stock",description="**Generator** \n", color = 0xFFFFFF, timestamp= datetime.datetime.utcnow()) # Define the embed
    stockmenu.set_footer(text =f"{server_name}")
    stockmenu
    for filename in os.listdir(f"Accounts/"):
        with open(f"Accounts//{filename}") as f: 
            ammount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") 
            stockmenu.description += f"*{name}* - {ammount}\n"
    await inter.send(embed=stockmenu)

#---------------------------------------- Mod Commands----------------------------------------
@venady.slash_command()
@commands.has_permissions(administrator=True)
async def create_stock(inter:disnake.ApplicationCommandInteraction, stock: disnake.Attachment):
    """Add stock to the generator"""

    if not "text/plain" in stock.content_type:
        await inter.send("Please use a text file!", ephemeral=True)
        return
    

    stock_bytes = await stock.read()
    stock_lines = stock_bytes.decode(stock.content_type.partition("charset=")[2]).splitlines()
    if len(stock_lines) > 5000:
        await inter.send("This combo have to many lines!", ephemeral=True)
        return
    await stock.save(f"Accounts/{stock.filename}")
    await inter.send(f"{stock.filename.partition('.')[0]} added to the generator")
    return

@venady.slash_command()
@commands.has_permissions(administrator=True)
async def delete_stock(inter: disnake.ApplicationCommandInteraction, stock):
    """remove stock from generator"""
    stock = stock.lower()+".txt" 
    path = f"Accounts"
    files = os.listdir(path)
    if not stock in files:
        await inter.send("Stock doesnt exist!", ephemeral=True)
        return
    os.remove(os.path.join(path, stock))
    name = stock.lower().replace(".txt","")
    await inter.send(f"{name} got deleted")
    
        

@venady.slash_command() #help command
async def help(inter):
    """show you all commands."""
    server_name = inter.guild.name
    help = disnake.Embed(title="Venady Help",description=f" ", color = 0xffffff, timestamp=datetime.datetime.utcnow())
    help.set_footer(text =f"{server_name}", icon_url="https://media.discordapp.net/attachments/1007664686679986186/1028340335732076634/venady_logo.png?width=676&height=676")


    view = disnake.ui.View()
    item = disnake.ui.Button(style=disnake.ButtonStyle.green, label="Support", url="https://discord.gg/wATBPDjWBP")
    view.add_item(item=item)

    item2 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Invite Me", url="https://discord.com/oauth2/authorize?client_id=1055579817069776906&permissions=8&scope=bot%20applications.commands")
    view.add_item(item=item2)




#--------------------------------------------------------------------------------1 Help Menu
    help.add_field(name="Generators Commands", value=f"""> `/gen`
    > Use this to generate!


    > `/stock`
    > Show you the account stock!
    """)
#------------------------------------------------------------------------------- 2 Help Menu
    help.add_field(name="Other Commands", value=f"""> `{prefix}help`
    > Show you this Message!
    """)

    await inter.send(embed=help, view=view)
    print(f"{inter.author.name} used (help) -> Successfull")


@venady.slash_command() #invite command
async def invite(inter):

    await inter.message.reply("Server Invite: https://discord.gg/venady \n Bot invite: https://bit.ly/3WlC3Er \n Sourcecode: https://github.com/nicotrixxel")
    


@venady.command() #test command
async def test(ctx):
   
    await ctx.message.reply("Private Command :P |Bot by discord.gg/venady")
    print(f"{ctx.author.name} used (test) -> Successful")

venady.run(token)
