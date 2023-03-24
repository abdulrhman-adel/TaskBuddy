from nextcord import Interaction, File, Embed, ButtonStyle, Colour, SelectOption
from nextcord.ui import View, Button, Select
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