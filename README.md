# Nova Discord Bot

Nova is a discord bot it bought to life using a Python library called Nextcord, it helps to CRUD clickup tasks from discord.

![Licence](https://img.shields.io/github/license/abdulrhman-adel/Discord-bot)
![Isuues](https://img.shields.io/github/issues/abdulrhman-adel/Discord-bot)
![Pull Request](https://img.shields.io/github/issues-pr/abdulrhman-adel/Discord-bot)
## Screenshots

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages required to run Nova.

```bash
pip install -r requirments.txt
```

## Usage

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

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[Apache 2](https://choosealicense.com/licenses/apache-2.0/)
