import logging
from typing import Dict
import disnake
from disnake.ext import commands
import aiohttp

from config import BotConfig, load_config

logging.basicConfig(level=logging.INFO)


class DailyNousance(commands.Bot):
    def __init__(self, config: BotConfig):
        self.config = config

        super().__init__(
            case_insensitive=True,
            help_command=None,
            intents=disnake.Intents.all(),
            command_prefix=commands.when_mentioned_or(config.COMMAND_PREFIX)
        )

        self.logger = logging.getLogger("bot")

        self.http_client: aiohttp.ClientSession = None

        self.cog_list = [
            "commands.owner",
            "core.events",
            "core.site_status",
        ]

    async def start(self, *args, **kwargs) -> None:
        async with aiohttp.ClientSession() as http_client:
            self.http_client = http_client
            
            for cog in self.cog_list:
                self.load_extension(f"cogs.{cog}")

            await super().start(*args, **kwargs)

    def run(self) -> None:
        super().run(self.config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    DailyNousance(load_config()).run()
