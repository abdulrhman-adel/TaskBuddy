import nextcord
from nextcord import Member, Interaction
from nextcord.ext import commands, tasks
from Helpers import config, clickup


class Clickup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    config_data = config.read_config()

    @nextcord.slash_command(name="clickup", description="Clickup Sign In", guild_ids=config_data["GUILD_IDS"])
    async def clickup(self, interaction: Interaction):
        user_id = interaction.user.id
        url = "https://app.clickup.com/api?client_id=" + self.config_data["CLICKUP_CLIENT_ID"] + "&redirect_uri=" + \
              self.config_data["CLICKUP_REDIRECT_URI"] + f"&state={user_id}"
        await interaction.response.send_message(url, ephemeral=True)

    @nextcord.slash_command(name="listfolders", description="List available folders", guild_ids=config_data["GUILD_IDS"])
    async def listfolders(self, interaction: Interaction):
        user_id = interaction.user.id
        token = clickup.get_token_by_id(user_id)
        teams = clickup.Client(token).get_teams()
        spaces = clickup.Client(token).get_spaces(teams[0]['id'])
        folders = clickup.Client(token).get_folders(spaces[0]['id'])
        await interaction.response.send_message(folders, ephemeral=True)


def setup(bot):
    bot.add_cog(Clickup(bot))
