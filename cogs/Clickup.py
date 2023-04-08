import nextcord
from nextcord import Interaction, ButtonStyle
from nextcord.ui import View, Button, Select
from nextcord.ext import commands
from Helpers import config, clickup, ui
import json


# TODO: Add error handling, logging

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

    # TODO: Use defer method instead of send_message directly to avoid errors

    @nextcord.slash_command(name="folders", description="List available folders",
                            guild_ids=config_data["GUILD_IDS"])
    async def folders(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id, channel_id)
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

    @nextcord.slash_command(name="members", description="List available members",
                            guild_ids=config_data["GUILD_IDS"])
    async def members(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        token = clickup.get_token_by_id(user_id, channel_id)
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

    @nextcord.slash_command(name="lists", description="List available Lists",
                            guild_ids=config_data["GUILD_IDS"])
    async def lists(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id, channel_id)
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

    @nextcord.slash_command(name="tasks", description="List available tasks on a folder",
                            guild_ids=config_data["GUILD_IDS"])
    async def tasks(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id, channel_id)
        folder_id = clickup.get_folder_id_by_channel_id(user_id, channel_id)
        lists = clickup.Client(token, user_id).get_lists(None, folder_id)
        current_page = 0

        async def list_dropdown_callbacks(interaction: Interaction):
            nonlocal list_sent_message, lists, view, list_dropdown, channel_id, user_id, folder_id, current_page
            list_id = list_dropdown.values[0]
            tasks = clickup.Client(token, user_id).get_tasks(list_id)
            tasks = json.dumps(tasks)
            tasks = json.loads(tasks)
            tasks = tasks['tasks']

            async def next_page_callback(interaction: Interaction):
                nonlocal current_page, list_sent_message, embed, view, tasks
                current_page = ui.next_page(current_page, tasks)
                embed = ui.create_tasks_embed(current_page, tasks)
                await interaction.response.edit_message(embeds=[embed], view=view)

            def previous_page_callback(interaction: Interaction):
                nonlocal current_page, list_sent_message, embed, view, tasks
                current_page = ui.previous_page(current_page)
                embed = ui.create_tasks_embed(current_page, tasks)
                return interaction.response.edit_message(embeds=[embed], view=view)

            embed = ui.create_tasks_embed(current_page, tasks)
            next_button = Button(style=ButtonStyle.green, label="Next", custom_id="next")
            previous_button = Button(style=ButtonStyle.red, label="Previous", custom_id="previous")
            next_button.callback = next_page_callback
            previous_button.callback = previous_page_callback
            view = View(timeout=180)
            view.add_item(previous_button)
            view.add_item(next_button)
            await interaction.response.edit_message(embeds=[embed], view=view)

        list_options = ui.create_lists_options(lists)
        list_dropdown = Select(placeholder="Select a list", options=list_options, min_values=1, max_values=1)
        list_dropdown.callback = list_dropdown_callbacks
        view = View(timeout=180)
        view.add_item(list_dropdown)
        list_sent_message = await interaction.followup.send("Select a list", view=view)

    @nextcord.slash_command(name="choosefolder", description="Choose folder to work on this channel",
                            guild_ids=config_data["GUILD_IDS"])
    async def choosefolder(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id, channel_id)
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

    @nextcord.slash_command(name="createtask", description="Create a task in a list",
                            guild_ids=config_data["GUILD_IDS"])
    async def createtask(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        await interaction.response.defer()
        token = clickup.get_token_by_id(user_id, channel_id)
        channel_id = interaction.channel_id
        folder_id = clickup.get_folder_id_by_channel_id(user_id, channel_id)
        lists = clickup.Client(token, user_id).get_lists(None, folder_id)

        async def list_dropdown_callback(interaction: Interaction):
            nonlocal list_sent_message, lists, view, list_dropdown, channel_id, user_id, folder_id
            list_id = list_dropdown.values[0]
            await interaction.response.send_modal(ui.CreateTaskModal(list_id))

        list_options = ui.create_lists_options(lists)
        list_dropdown = Select(placeholder="Select a list", options=list_options, min_values=1, max_values=1)
        list_dropdown.callback = list_dropdown_callback
        view = View(timeout=180)
        view.add_item(list_dropdown)
        list_sent_message = await interaction.followup.send("Select a list", view=view)

    @nextcord.slash_command(name="clear", description="Clear all data from this channel",
                            guild_ids=config_data["GUILD_IDS"])
    async def clear(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        channel_id = interaction.channel_id
        clickup.delete_channel_id(user_id, channel_id)
        await interaction.response.send_message("Channel cleared")

    @nextcord.slash_command(name="remove", description="Remove user data",
                            guild_ids=config_data["GUILD_IDS"])
    async def remove(self, interaction: Interaction):
        user_id = interaction.user.id
        channel_id = interaction.channel_id
        check = clickup.check_if_user_exists(user_id, channel_id)
        if check is False:
            await interaction.response.send_message("You are not signed in, please sign in first", ephemeral=True)
            return
        clickup.delete_user_token(user_id, channel_id)
        await interaction.response.send_message("User data removed")


def setup(bot):
    bot.add_cog(Clickup(bot))

# TODO: Clean up code
