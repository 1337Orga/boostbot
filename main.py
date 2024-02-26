import discord, os, json, hashlib, fade, datetime
from boosting import *
if os.name == 'nt':
    import ctypes
from datetime import datetime
from colorama import Fore
import discord, asyncio, json, typing, os, random, time
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime
from discord.utils import get
from discord.ext import commands

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command('help')

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            global startTime 
            startTime = time.time()
        from colorama import Fore
        BoostBot = f"""
                                _____________________________________   _______________________
                                ___  __ )_  __ \_  __ \_  ___/__  __/   ___  __ )_  __ \__  __/
                                __  __  |  / / /  / / /____ \__  /      __  __  |  / / /_  /   
                                _  /_/ // /_/ // /_/ /____/ /_  /       _  /_/ // /_/ /_  /    
                                /_____/ \____/ \____/ /____/ /_/        /_____/ \____/ /_/"""
                                    
        fade_text = fade.pinkred(BoostBot)
        print(fade_text + '\n')

bot = client()
tree = app_commands.CommandTree(bot)

config = json.load(open("config.json", encoding="utf-8"))

def clear(): #clears the terminal
    os.system('cls' if os.name =='nt' else 'clear')

if os.name == "nt":
    ctypes.windll.kernel32.SetConsoleTitleW(f"Boost Bot")
else:
    pass

TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
capmonster_key = config.get("capmonster_key")

if capmonster_key != " ":
    from colorama import Fore
    Key = f"{Fore.LIGHTGREEN_EX}Enable{Fore.RESET}"
else :
    from colorama import Fore
    Key = f"{Fore.LIGHTRED_EX}Disabled{Fore.RESET}"
    
@tree.command(name = 'help', description = 'Afficher la liste des commandes.')
async def help(interaction:discord.Interaction):
    embed = discord.Embed(title=f"⚙️ | **BOT COMMANDS**", color=0x2F3136) 
    embed.add_field(name="Find all my commands below :", value=f"""
    \n`/help` - View all commands
`/activity` - Change the activity of the bot
`/ping` - Show the latency of the bot
`/boost` - Allows you to boost servers with tokens
`/stock` -  Shows you your current tokens and boosts stock
`/restock` - Allows to add tokens (https://paste.ee)
`/clearstock` - Will delete everything from your stock""")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'activity', description = 'Afficher la liste des commandes.')
async def activity(interaction:discord.Interaction, activity:str, twitch_url:str = None):
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))
    await bot.change_presence(activity=discord.Streaming(type=discord.ActivityType.streaming, name=activity, url=twitch_url))
    from colorama import Fore
    TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(f" {TimeNow} {Fore.LIGHTYELLOW_EX}[ ~ ] {Fore.WHITE}Activity changed to {Fore.LIGHTBLACK_EX}{activity}")
    embed = discord.Embed(title="🪄 | **ACTIVITY**", description=f"**Activity has been changed to** `{activity}`.\n*Changed by* {interaction.user.mention}", color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    return await interaction.response.send_message(embed=embed)

@tree.command(name = 'ping', description = 'Afficher la liste des commandes.')
async def ping(interaction:discord.Interaction):
    from colorama import Fore
    TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(f" {TimeNow} {Fore.LIGHTYELLOW_EX}[ ~ ] {Fore.WHITE}{interaction.user.name} has check my latency {Fore.LIGHTBLACK_EX}[{Fore.WHITE}{round(bot.latency * 1000)} ms{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    await interaction.response.send_message(embed = discord.Embed(title = " ", description = f"♾️ **{round(bot.latency * 1000)} ms**", color = 0x2c2f33))

@app_commands.choices(
    type=[
        app_commands.Choice(name="3 mois", value=3),
        app_commands.Choice(name="1 mois", value=1)
    ]
)
@tree.command(name='restock', description='Afficher la liste des commandes.')
async def restock(interaction: discord.Interaction, code: str, type: int):  # Change the type to int
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))
    if type != 1 and type != 3 and type != 0:
        return await interaction.response.send_message(embed=discord.Embed(
            title="**Invalid Input**", description="Type can either be 3 (months), 1 (month) or empty",
            color=0xf35454))
    if type == 1:
        file = "input/1m_tokens.txt"
    elif type == 3:
        file = "input/3m_tokens.txt"

    code = code.replace("https://paste.ee/p/", "")
    temp_stock = requests.get(f"https://paste.ee/d/{code}",
                                  headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}).text

    f = open(file, "a", encoding="utf-8")
    f.write(f"{temp_stock}\n")
    f.close()
    lst = temp_stock.split("\n")
    from colorama import Fore
    TimeNow = datetime.now().strftime(
        f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(
        f" {TimeNow} {Fore.LIGHTGREEN_EX}[ + ] {Fore.WHITE}{interaction.user.name} Restock {len(lst)} tokens to `{file}`")
    embed = discord.Embed(title=f"✅ | **TOKENS RESTOCK**",
                          description=f"**Restock {len(lst)} tokens to** `{file}`",
                          color=0x2F3136)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'addowner', description = 'Afficher la liste des commandes.')
async def addowner(interaction:discord.Interaction, member:discord.Member):
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))    
    config["ownerID"].append(member.id)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent = 4)
    
    from colorama import Fore
    TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(f" {TimeNow} {Fore.LIGHTGREEN_EX}[ + ] {Fore.WHITE}{interaction.user.name} added {member} as an owner")
    embed = discord.Embed(title=f"✅ | **ADDED OWNER**",
        description=f"{interaction.user.mention} **added** {member.mention} ({member.id}) **as an owner**",
        color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'addadmin', description = 'Afficher la liste des commandes.')
async def addadmin(interaction:discord.Interaction, member:discord.Member):
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))    
    config["adminID"].append(member.id)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent = 4)
        
    from colorama import Fore
    TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(f" {TimeNow} {Fore.LIGHTGREEN_EX}[ + ] {Fore.WHITE}{interaction.user.name} added {member} as an admin")
    embed = discord.Embed(title=f"✅ | **ADDED ADMIN**",
        description=f"{interaction.user.mention} **added** {member.mention} ({member.id}) **as an admin**",
        color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'stock', description = 'Afficher la liste des commandes.')
async def stock(interaction:discord.Interaction):
    three = len(open("input/3m_tokens.txt", "r").readlines())
    one = len(open("input/1m_tokens.txt", "r").readlines())
    embed = discord.Embed(title=f"⚙️ | **INFO STOCK**",
        description=f"""> **1 Month Nitro Tokens :** `{one}`
        > **3 Months Nitro Tokens :** `{three}`\n
        > **1 Month Server Boosts :** `{one*2}`
        > **3 Months Server Boosts :** `{three*2}`""",
        color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    await interaction.response.send_message(embed=embed)

@app_commands.choices(
    type=[
        app_commands.Choice(name="3 mois", value=3),
        app_commands.Choice(name="1 mois", value=1)
    ]
)
@tree.command(name = 'clearstock', description = 'Afficher la liste des commandes.')
async def clearstock(interaction:discord.Interaction, type:int):
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))
    if type == 1:
        file = "input/1m_tokens.txt"
        month = "1 month"
    elif type == 3:
        file = "input/3m_tokens.txt"
        month = "3 month"

    embed = discord.Embed(title=f"✅ | **STOCK CLEARED**",
                          color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/495577196933545985/1127657048570593421/logo-bot.png")
    fileVariable = open(file, 'r+')
    fileVariable.truncate(0)
    fileVariable.close()
    await interaction.response.send_message(embed=embed)
    from colorama import Fore
    TimeNow = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}%H{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%M{Fore.LIGHTBLACK_EX}:{Fore.WHITE}%S{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
    print(f" {TimeNow} {Fore.LIGHTRED_EX}[ - ] {Fore.WHITE}{interaction.user.name} has clear his stock {month}")

@app_commands.choices(
    months=[
        app_commands.Choice(name="3 mois", value=3),
        app_commands.Choice(name="1 mois", value=1)
    ]
)
@tree.command(name='boost', description='Afficher la liste des commandes.')
async def boost(interaction: discord.Interaction, invite: str, amount: int, months: int, nick: str = None):
    if interaction.user.id not in config["ownerID"] and interaction.user.id not in config['adminID']:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Missing Permission**", description = "❌ **You must be an owner or an administrator to use this command ❌", color = 0xf46868))
    
    if months == 1:
        filename = "input/1m_tokens.txt"
    if months == 3:
        filename = "input/3m_tokens.txt"
    
    if checkEmpty(filename):
        return await interaction.response.send_message(embed = discord.Embed(title = "**Stock Error**", description = "❌ **There is currently no stock in the files. Please use `/restock` to add nitro tokens in the stock files** ❌", color = 0xf46868))
    if len(open(filename, "r").readlines()) < amount / 2:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Stock Error**", description = "❌ **There is currently not enough stock in the files. Please use `/restock` to add nitro tokens in the stock files** ❌", color = 0xf46868))
    
    if validateInvite(invite) == False:
        return await interaction.response.send_message(embed = discord.Embed(title = "**Invite Error**", description = "❌ **The invite submitted is invalid. Please sumbit a valid invite link** ❌", color = 0xf46868))
    
    await interaction.response.send_message(embed = discord.Embed(title = "✅ **Boosts Started**", description = f"**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months", color = 0x2c2f33))
    sprint(f"Boosting https://discord.gg/{invite}, {amount} times for {months} months", True)
    start = time.time()
    boosted = thread_boost(invite, amount, months, nick)
    end = time.time()
    time_taken = round(end - start, 2)
    
    if boosted == False:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
        
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
    
    
        embed2 = DiscordEmbed(title = "❌ **Boosts Unsuccessful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0xf35454)
        embed2.set_timestamp()
        webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
        webhook.add_embed(embed2)
        webhook.execute()
        print()
        sprint(f"Failed to Boost https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", False)
        print()
        
        webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
        
        os.remove("success.txt")
        os.remove("failed.txt")
        
        return await interaction.response.send_message(embed = discord.Embed(title = "❌ **Boosts Unsuccessful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0xf35454))
    
    elif boosted:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
        
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
                
        embed3 = DiscordEmbed(title = "✅ **Boosts Successful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0x62f354)
        embed3.set_timestamp()
        webhook = DiscordWebhook(url=config["boost_log_webhook"])
        webhook.add_embed(embed3)
        webhook.execute()
        print()
        sprint(f"Boosted https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", True)
        print()
        
        webhook = DiscordWebhook(url=config["boost_log_webhook"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
        
        os.remove("success.txt")
        os.remove("failed.txt")
        
        return await interaction.response.send_message(embed = discord.Embed(title = "✅ **Boosts Successful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0x62f354))

clear()
bot.run(config['bot_token'])