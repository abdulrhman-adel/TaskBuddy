import nextcord
from nextcord import Member, Interaction, File, Embed, ButtonStyle, Colour, SelectOption
from nextcord.ui import View, Button, Select
from nextcord.ext import commands, tasks
from Helpers import config, clickup, ui

# TODO: Add error handling, logging
# TODO: if user is not in database, send message to user to sign in

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

    # TODO: Decrese respond time
    # TODO: Use defer method instead of send_message directly to avoid errors

    @nextcord.slash_command(name="listfolders", description="List available folders",
                            guild_ids=config_data["GUILD_IDS"])
    async def listfolders(self, interaction: Interaction):
        user_id = interaction.user.id
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id)
        teams = clickup.Client(token, user_id).get_teams()
        team_id = clickup.get_team_id(teams)
        spaces = clickup.Client(token, user_id).get_spaces(team_id)
        space_id = clickup.get_space_id(spaces)
        folders = clickup.Client(token, user_id).get_folders(space_id)
        members = clickup.get_members(teams)
        current_page = 0

        async def next_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, folders
            current_page = ui.next_page(current_page, folders)
            embed = ui.create_folders_embed(current_page, folders)
            await interaction.response.edit_message(embeds=[embed], view=view)

        def previous_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, folders
            current_page = ui.previous_page(current_page)
            embed = ui.create_folders_embed(current_page, folders)
            return interaction.response.edit_message(embeds=[embed], view=view)

        embed = ui.create_folders_embed(current_page, folders)
        next_button = Button(style=ButtonStyle.green, label="Next", custom_id="next")
        previous_button = Button(style=ButtonStyle.red, label="Previous", custom_id="previous")
        next_button.callback = next_page_callback
        previous_button.callback = previous_page_callback
        view = View(timeout=180)
        view.add_item(previous_button)
        view.add_item(next_button)
        sent_message = await interaction.followup.send(embeds=[embed], view=view)

    # TODO: Make button disabled when it reaches the end of the list

    @nextcord.slash_command(name="listmembers", description="List available members",
                            guild_ids=config_data["GUILD_IDS"])
    async def listmembers(self, interaction: Interaction):
        user_id = interaction.user.id
        token = clickup.get_token_by_id(user_id)
        teams = clickup.Client(token, user_id).get_teams()
        members = clickup.get_members(teams)
        current_page = 0

        async def next_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, members
            current_page = ui.next_page(current_page, members)
            embed = ui.create_members_embed(current_page, members)
            await interaction.response.edit_message(embeds=[embed], view=view)

        def previous_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, members
            current_page = ui.previous_page(current_page)
            embed = ui.create_members_embed(current_page, members)
            return interaction.response.edit_message(embeds=[embed], view=view)

        embed = ui.create_members_embed(current_page, members)
        next_button = Button(style=ButtonStyle.green, label="Next", custom_id="next")
        previous_button = Button(style=ButtonStyle.red, label="Previous", custom_id="previous")
        next_button.callback = next_page_callback
        previous_button.callback = previous_page_callback
        view = View(timeout=180)
        view.add_item(previous_button)
        view.add_item(next_button)
        sent_message = await interaction.response.send_message(embeds=[embed], view=view)

    @nextcord.slash_command(name="chooseboard", description="Show chosen board",
                            guild_ids=config_data["GUILD_IDS"])
    async def chooseboard(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id)
        teams = clickup.Client(token, user_id).get_teams()
        team_id = clickup.get_team_id(teams)
        spaces = clickup.Client(token, user_id).get_spaces(team_id)
        space_id = clickup.get_space_id(spaces)
        folders = clickup.Client(token, user_id).get_folders(space_id)

        async def folder_dropdown_callback(interaction: Interaction):
            nonlocal sent_message, folders, view, folder_dropdown, channel_id, user_id, team_id, space_id
            folder_id = folder_dropdown.values[0]
            clickup.store_channel_id(user_id, channel_id, space_id, folder_id, team_id)
            folder = clickup.get_folder_by_id(folders, folder_id)
            folder_option = ui.create_folder_option(folder)
            folder_dropdown = Select(placeholder=folder['name'], options=[folder_option], min_values=1, max_values=1)
            folder_dropdown.callback = folder_dropdown_callback
            view = View(timeout=180)
            view.add_item(folder_dropdown)
            await interaction.response.edit_message(content="Folder selected:", view=view)

            # await interaction.response.edit_message(content= "Folder selected: " + folder_id + " " + f"{user_id} d {channel_id} " + team_id + " " + space_id)

        folder_options = ui.create_folders_options(folders)
        folder_dropdown = Select(placeholder="Select a folder", options=folder_options, min_values=1, max_values=1)
        folder_dropdown.callback = folder_dropdown_callback
        view = View(timeout=180)
        view.add_item(folder_dropdown)
        sent_message = await interaction.followup.send("Select a folder", view=view)


    @nextcord.slash_command(name="listoflists", description="List available tasks",
                            guild_ids=config_data["GUILD_IDS"])
    async def listoflists(self, interaction: Interaction):
        user_id = interaction.user.id
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id)
        channel_id = interaction.channel_id
        folder_id = clickup.get_folder_id_by_channel_id(user_id, channel_id)
        # tasks = clickup.Client(token, user_id).get_tasks(folder_id)
        lists = clickup.Client(token, user_id).get_lists(None, folder_id)
        current_page = 0

        async def next_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, lists
            current_page = ui.next_page(current_page, lists)
            embed = ui.create_lists_embed(current_page, lists)
            await interaction.response.edit_message(embeds=[embed], view=view)
        def previous_page_callback(interaction: Interaction):
            nonlocal current_page, sent_message, embed, view, lists
            current_page = ui.previous_page(current_page)
            embed = ui.create_lists_embed(current_page, lists)
            return interaction.response.edit_message(embeds=[embed], view=view)

        embed = ui.create_lists_embed(current_page, lists)
        next_button = Button(style=ButtonStyle.green, label="Next", custom_id="next")
        previous_button = Button(style=ButtonStyle.red, label="Previous", custom_id="previous")
        next_button.callback = next_page_callback
        previous_button.callback = previous_page_callback
        view = View(timeout=180)
        view.add_item(previous_button)
        view.add_item(next_button)
        sent_message = await interaction.followup.send(embeds=[embed], view=view)





def setup(bot):
    bot.add_cog(Clickup(bot))
