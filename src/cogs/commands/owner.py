import os
from disnake.ext import commands

from bot import DailyNousance
from util.code import execute_code
from util.errors import format_exception


class OwnerCommands(commands.Cog):
    def __init__(self, bot: DailyNousance):
        self.bot = bot

    @commands.command(name="update", aliases=["reload"])
    @commands.is_owner()
    async def update_bot(self, ctx: commands.Context):
        os.system("git pull")

        for cog in self.bot.cog_list:
            self.bot.reload_extension(f"cogs.{cog}")
        
        await ctx.message.add_reaction("✔️")

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval_code(self, ctx: commands.Context, *, stuff: str):
        stuff = stuff.strip(" `\n")

        if stuff.startswith("py"):
            stuff = stuff[2:]

        try:
            result = await execute_code(stuff, {**globals(), **locals(), "bot": self.bot, "self": self})

            await ctx.reply(f"```\n{str(result).replace('```', '｀｀｀')}```")
        except Exception as e:
            await ctx.reply(f"```py\n{format_exception(e)[:2000-9].replace('```', '｀｀｀')}```")

    @commands.command(name="error")
    @commands.is_owner()
    async def intentional_error(self, ctx: commands.Context):
        raise Exception("This is an intentional error!")


def setup(bot: DailyNousance):
    bot.add_cog(OwnerCommands(bot))
