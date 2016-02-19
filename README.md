# Instructions

If you haven't installed these yet, run:
pip install tornado
pip install easyjson
pip install flask

The summarizer is linked to the Treehacks Slack by default. 
To change this, go to slack_listener.py and add your API Access Token
to the connect_to_slack function

To initialize the server, run
$ python run_server.py

Server will be listening at port 8889, showing the JSON data of all the groups

# Inspiration

Everyone has those friends who just add you to their group chats, and then you get incessantly flooded with notifications. After muting conversations, you'll miss invitations and key messages, mainly because you didn't see them. Now there's a way to manage your notifications and be sure that you miss out.

It was especially helpful for the TreeHacks Slack group. Especially since we're hacking, we preferred not to be notified much, or spend time just to see where lunch is. It also helped us find out that a guy just dropped off an Echo in the hardware booth, and we promptly intercepted it from another team. :D

We also built this for accessibility. Most people with vision disorders or physical disabilities have a hard time talking to their friends (since most of us use instant messaging, not calls). Our project would allow these people to have the Echo talk to them and basically act as their social assistant.

# What it does

To summarize group messages from GroupMe, you could tell Alexa to summarize whichever group you want. She'll then tell you what topics were discussed, and the main points said in each topic. She'll even tell you about what certain people were feeling. If you don't fully understand the messages, you could ask her for the context, and she'll tell you what was said before and after. The same functions work if you want your Slack messages summarized.

For Slack specifically, we built a Slackbot, which you could enter your commands to select which group to summarize. All the other functions above apply here too!

# Demo

<img src="http://g.recordit.co/bevXGCB2ty.gif" alt="This will display an animated GIF" />

