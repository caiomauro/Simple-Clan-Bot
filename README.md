# simpleclanbot
About Simple Clan Bot
SimpleClanBot

SimpleClanBot is an easy to setup and use discord bot.
Designed for game servers to engage their community with a built in clan system.
Many customization features coming soon!
Comprehensive and easy to follow installation guide right here!
For help or bug reporting please message me here!
Dev Log:

10/21/23 - Fixed bugs and added new features
Hosting:

Could hosting recommendation: 
Google Cloud - https://cloud.google.com/blog/topics/developers-practitioners/build-and-run-discord-bot-top-google-cloud
Local hosting:
This essentially boils down to running the bot's code on your machine

Setup and Installation:

Setup your servers bot
Create a new application: https://discord.com/developers/docs/getting-started
Assign your bots name (Changeable later)
In General Information upload an icon and give your bot a name and description (Please include "SimpleClanBot by staticDev" in your description)
Go to Bot and assign a username and icon (if it does not carry over)
Scroll down to Privileged Gateway Intents and toggle on the 3 options (Presence, Server Member, Message Content)
Scroll back up in Bot and reset your bot token, copy the new token (store it for later)
Go to OAuth2 -> URL Generator. In Scopes select bot and applications.commands, under Permissions select Administrator
Use the link at the bottom of URL Generator to invite the bot to your server (it will be offline)
Configure the SimpleClanBot.py file
Open the file in a text editor of your choice, if you do not have one here is a good online option: https://www.online-python.com/
On lines 19 & 20 place your discord user id -> owner_id and your servers id -> guild_id (these should remain ints)
Set clawn_owner_role_name to whatever you want the clan owner role to be
Scroll to the bottom of the file and paste your bot's token in bot.run('YOUR TOKEN HERE')
Save the file or export the new edited file for your server.
Upload and Run the bot
Whether local or cloud hosting you should have a Console to work in.
Install the latest version of Python3 on your hosting platform: https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/
Use the package manager pip to install the needed packages. (https://pip.pypa.io/en/stable/)
pip install discord
pip install discord-ext-bot
pip install discord-ui
pip install discord.py
Once the packages are installed upload your edited SimpleClanBot.py file
Use the command python3 SimpleClanBot.py to run the bot
Setup in Discord
Confirm that the bot is now appearing online in your server
Go to your server roles and drag the SimpleClanBot role to the top (Must be done)
In a text channel type the command /clan sync to sync the / commands which prompt users for certain commands inputs 
Enable 'applications.commands' permission to your members who you want to have access to the bot
Wait up to 2 minutes for you to type / and see the new bot in the command UI
Commands:

/clan sync : Syncs the bots command tree to show the clan commands to users when they type / (Only server owner)
/clan ownercolor {hexcode} - Changes color of team owner role (Only Server Owner)
/clan-create {name} : Creates a channel Clan Category, inside all new text channels and roles are placed, assigns role to the clan creator
/clan-invite {user} : PM's user with Accept/Reject buttons, will assign the user the clan role in the server (invited user must be in the server already)
/clan-kick {user} : Automatically removes the users clan role (they can no longer see the text channel)
/clan-leave : Removes the users clan role (they can no longer see the text channel)
/clan-disband {name} : Deletes the clan channel and role from the server (enables clan owner to create a new clan)
/clan-color {hexcode} - Changes the color of your clans role (Only Clan Owner)
 

License

NOT FOR RESALE OR DISTRIBUTION AFTER PURCHASE UNDER ANY CONDITION
