import discord
from discord.ext import commands
from main import embedCreator, getAlias

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=getAlias("ping"))
    async def ping(self, ctx):
        apiping = int(self.client.latency * 1000)
        embed=embedCreator("API Latency", f"{apiping}ms", discord.Color.blurple())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Admin(client))