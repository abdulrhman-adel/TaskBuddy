import nextcord
from nextcord import Member, Interaction
from nextcord.ext import commands, tasks
from Helpers import config


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    config_data = config.read_config()

    @nextcord.slash_command(name="ping", description="Pong!", guild_ids=config_data["GUILD_IDS"])
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("Pong!")


def setup(bot):
    bot.add_cog(Greetings(bot))
