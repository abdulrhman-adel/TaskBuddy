from nextcord import Interaction, File, Embed, ButtonStyle, Colour, SelectOption, TextInputStyle
from nextcord.ui import View, Button, Select, Modal, TextInput
from Helpers import clickup
import time
from datetime import datetime
import json


def next_page(page_num, members):
    if page_num < len(members) // 5:
        page_num += 1
    return page_num


def previous_page(page_num):
    if page_num > 0:
        page_num -= 1
    return page_num


def create_members_embed(page_num, members):
    embed = Embed(title="Members", description="List of members", color=Colour.blue())
    if page_num < len(members) // 5:
        for member in members[page_num * 5:page_num * 5 + 5]:
            embed.add_field(name=member['user']['username'], value=member['user']['email'], inline=False)
        embed.set_footer(text=f"Page {page_num + 1}/{len(members) // 5 + 1}")
        return embed
    else:
        page_num = len(members) // 5
        for member in members[page_num * 5:]:
            embed.add_field(name=member['user']['username'], value=member['user']['email'], inline=False)
        embed.set_footer(text=f"Page {page_num}/{len(members) // 5}")
        return embed


def create_folders_embed(page_num, folders):
    embed = Embed(title="Folders", description="List of folders", color=Colour.blue())
    if page_num < len(folders) // 5:
        for folder in folders[page_num * 5:page_num * 5 + 5]:
            embed.add_field(name=folder['name'], value=folder['task_count'] + "Tasks", inline=False)
        embed.set_footer(text=f"Page {page_num + 1}/{len(folders) // 5 + 1}")
        return embed
    else:
        page_num = len(folders) // 5
        for folder in folders[page_num * 5:]:
            embed.add_field(name=folder['name'], value=folder['id'], inline=False)
        embed.set_footer(text=f"Page {page_num}/{len(folders) // 5}")
        return embed


def create_folders_options(folders):
    folder_dropdown = SelectOption(label="Select a folder", value="0")
    folder_dropdown_list = [folder_dropdown]
    for folder in folders:
        folder_dropdown = SelectOption(label=folder['name'], value=folder['id'])
        folder_dropdown_list.append(folder_dropdown)
    return folder_dropdown_list


def create_folder_option(folder):
    folder_dropdown = SelectOption(label=folder['name'], value=folder['id'])
    return folder_dropdown


def create_lists_embed(page_num, lists):
    embed = Embed(title="Lists", description="List of lists", color=Colour.blue())
    if page_num < len(lists) // 5:
        for list in lists[page_num * 5:page_num * 5 + 5]:
            embed.add_field(name=list['name'], value=list['task_count'] + "Tasks", inline=False)
        embed.set_footer(text=f"Page {page_num + 1}/{len(lists) // 5 + 1}")
        return embed
    else:
        page_num = len(lists) // 5
        for list in lists[page_num * 5:]:
            embed.add_field(name=list['name'], value=list['id'], inline=False)
        embed.set_footer(text=f"Page {page_num}/{len(lists) // 5}")
        return embed


def create_lists_options(lists):
    list_dropdown = SelectOption(label="Select a list", value="0")
    list_dropdown_list = [list_dropdown]
    for list in lists:
        list_dropdown = SelectOption(label=list['name'], value=list['id'])
        list_dropdown_list.append(list_dropdown)
    return list_dropdown_list


def create_tasks_embed(page_num, tasks):
    embed = Embed(title="Tasks", description="List of tasks", color=Colour.blue())

    if page_num < len(tasks) // 5:
        for task in tasks[page_num * 5:page_num * 5 + 5]:
            embed.add_field(name=task['name'], value=task['description'], inline=False)
        embed.set_footer(text=f"Page {page_num + 1}/{len(tasks) // 5 + 1}")
        return embed
    else:
        page_num = len(tasks) // 5
        for task in tasks[page_num * 5:]:
            embed.add_field(name=task['name'], value=task['description'], inline=False)
        embed.set_footer(text=f"Page {page_num}/{len(tasks) // 5}")
        return embed


def create_lists_slash_options(lists):
    list_dropdown = []
    for list in lists:
        list_dropdown.append({"name": list['name'], "value": list['id']})
        list_dropdown = ",".join(repr(e) for e in list_dropdown)
        return list_dropdown
    # return str(list_dropdown).replace("'", "").replace("[", "").replace("]", "").replace(" ", "").replace('"', ''


class CreateTaskModal(Modal):
    def __init__(self, list_id):
        super().__init__(
            title="Create a task",
        )
        self.list_id = list_id
        self.tkTitle = TextInput(label="Task title", placeholder="Enter the title of the task", required=True)
        self.add_item(self.tkTitle)
        self.tkDescription = TextInput(label="Task description", placeholder="Enter the description of the task"
                                       , style=TextInputStyle.paragraph, required=True)
        self.add_item(self.tkDescription)
        self.tkAssignee = TextInput(label="Task assignee", placeholder="Enter the assignee of the task", required=True)
        self.add_item(self.tkAssignee)
        self.tkDueDate = TextInput(label="Task due date", placeholder="Enter the due date of the task", required=True)
        self.add_item(self.tkDueDate)
        self.tkTags = TextInput(label="Task tags", placeholder="Enter the tags of the task", required=True)
        self.add_item(self.tkTags)

    async def callback(self, interaction: Interaction) -> None:
        title = self.tkTitle.value
        description = self.tkDescription.value
        list_id = self.list_id
        task_name = self.tkTitle.value
        task_description = self.tkDescription.value
        task_assignee = self.tkAssignee.value
        task_due_date = self.tkDueDate.value
        task_due_date = task_due_date.replace('-', '/')
        task_due_date = int(time.mktime(datetime.strptime(task_due_date, "%d/%m/%Y").timetuple())) * 1000

        task_tags = self.tkTags.value
        token = clickup.get_token_by_id(interaction.user.id, interaction.channel_id)
        store = clickup.Client(token, interaction.user.id).create_task(list_id, task_name, task_description,
                                                                       task_assignee, task_due_date, task_tags)

        # tk = Embed(title="title", description=description, color=Colour.blue())
        # return await interaction.response.send_message(embed=tk)
