import discord, json, os
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

############

with open("config.json", "r") as config_loader:
    config = json.load(config_loader)

############

def embedCreator(title, desc, color):
    embed = discord.Embed(
        title=f"{title}",
        description=f"{desc}",
        color=color
    )
    return embed

def IsOwner(userID):
    OwnerId = config["owner_id"]
    if userID == OwnerId:
        return True
    else:
        return False

############


@bot.command()
async def stop(ctx):
    await ctx.send(embed=embedCreator("Stopping", "Shutting Down Bot", 0xFF0000))
    await bot.logout()

############

# Load Cogs

@bot.command()
async def load(ctx, extension):
    if ctx.message.author.id == OwnerId:
        bot.load_extension(f'commands.{extension}')
        await ctx.send(f"loaded {extension}")
    else:
        await ctx.send(embed=NoPermsEmbed("Bot Owner"))


@bot.command()
async def unload(ctx, extension):
    if ctx.message.author.id == OwnerId:
        bot.unload_extension(f'commands.{extension}')
        await ctx.send(f"unloaded {extension}")
    else:
        await ctx.send(embed=NoPermsEmbed("Bot Owner"))


@bot.command(aliases=["relaod"])
async def reload(ctx):
    if ctx.message.author.id == OwnerId:
        try:
            for filename in os.listdir('./commands/'):
                if filename.endswith('.py'):
                    bot.unload_extension(f'commands.{filename[:-3]}')
                    bot.load_extension(f'commands.{filename[:-3]}')
            await ctx.send("Reloaded Cogs")
        except Exception as e:
            error = discord.Embed(
                title="Error Reloading",
                description=f"`{e}`",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=error)


# load cogs on startup
for filename in os.listdir('./commands/'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Unknown Command",
            color=0xbf1300,
            description=f"The command `{ctx.message.content.split(' ')[0]}` is not found! Use `.help` to list all commands!")
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(
            title="Error",
            color=0xff0000,
            description=f"Unexpected Error: `{error}`"
        )
        await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    await ctx.send(embed=embedCreator("test", "oh no", 0x123456))

bot.run(config["token"])