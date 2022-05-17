from http import HTTPStatus
import aiohttp
from disnake.ext import commands, tasks

from bot import DailyNousance
from util.errors import format_exception

class SiteStatus(commands.Cog):
    def __init__(self, bot: DailyNousance):
        self.bot = bot
        self.http_client = bot.http_client
        
        self.check_site_status.start()

    def cog_unload(self):
        self.check_site_status.stop()

    @tasks.loop(seconds=60)
    async def check_site_status(self):
        try:
            self.bot.logger.info("Checking site status...")

            alert_channel = self.bot.get_channel(self.bot.config.DISCORD_DOWNTIME_ALERT_CHANNEL_ID)

            try:
                req = await self.http_client.get("https://dailynous.com", timeout=aiohttp.ClientTimeout(total=5))
            except aiohttp.ServerTimeoutError:
                await alert_channel.send(f":warning::rotating_light: <@735948823368826901>, the website took longer than 5 seconds to respond!")
                return
            except aiohttp.ClientConnectorError:
                await alert_channel.send(f":warning::rotating_light: <@735948823368826901>, the website wouldn't connect at all!")
                return
            except aiohttp.ClientError as e:
                await alert_channel.send(f":warning::rotating_light: <@536986067140608041>, an unknown aiohttp error occurred!")
                self.bot.logger.error(format_exception(e))
                return
            
            status = HTTPStatus(req.status)

            if status != HTTPStatus.OK:
                await alert_channel.send(f":warning::rotating_light: <@735948823368826901>, the response from the website was not OK!\n\nHTTP code: `{status.value} {status.name}` ({status.description})")
        except Exception as e:
            self.bot.logger.error(format_exception(e))
        finally:
            self.bot.logger.info("Done fetching site status.")

    @check_site_status.before_loop
    async def before_check_site_status_loop(self):
        await self.bot.wait_until_ready()

def setup(bot: DailyNousance):
    bot.add_cog(SiteStatus(bot))
