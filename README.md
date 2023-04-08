# TaskBuddy

TaskBuddy is a Discord bot that helps organize your server's CRUD tasks using the ClickUp API. It also has other small features to enhance your server's functionality.

## Features

- Create, read, update, and delete tasks in your ClickUp workspace directly from Discord
- Organize your server's tasks using the ClickUp task lists and statuses
- View all of your server's tasks in one place with the `/tasks` command
- Get reminders for upcoming due dates for your server's tasks

## Installation

1. Clone this repository to your local machine
2. Install the required dependencies using `pip install -r requirements.txt`
3. Copy and rename the `config.json.example` file and add your Discord bot token and ClickUp API token
4. Run `python main.py` to start the bo## Contributing

## Commands

- `/choosefolder` - Choose a folder you want to use in your channel
- `/create-task` - Creates a new task in ClickUp with the given name and description
- `/createtask` - Creates a new task in ClickUp with the given name and description
- `/tasks` - Lists all the tasks available in your chosen list
- `/lists` - Lists all the lists available in your chosen folder
- `/folders` - Lists all the folders available in your workspace
- `/members` - Lists all the members in your workspace
- `/remove` - Removes the user from the database

## Example

```python
import nextcord
from nextcord import Member, Interaction
from nextcord.ext import commands, tasks

@nextcord.slash_command(name="NAME_OF_COMMAND", description="DESCRIPTION_OF_COMMAND",
                          guild_ids=config_data["GUILD_IDS"])
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("RESPONSE_MESSAGE")
```

## Contributing

If you would like to contribute to this project, please fork this repository and submit a pull request with your changes.

## License

[Apache 2](https://choosealicense.com/licenses/apache-2.0/) This project is licensed under the Apache License 2.0.
