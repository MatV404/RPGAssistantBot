import discord
import discord.ext.test as dpytest
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio

class Misc(Cog):
    @command()
    async def ping(self, ctx):
        await ctx.send("Pong !")

    @command()
    async def echo(self, ctx, text: str):
        await ctx.send(text)


@pytest_asyncio.fixture
async def bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="R!",
                       intents=intents)
    await bot._async_setup_hook()
    await bot.add_cog(Misc())

    dpytest.configure(bot)

    yield bot

    await dpytest.empty_queue()

@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("R!ping")
    assert dpytest.verify().message().content("Pong !")

@pytest.mark.asyncio
async def test_echo(bot):
    await dpytest.message("R!echo HI!")
    assert dpytest.verify().message().contains().content("HI!")