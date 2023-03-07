import discord
import openai


print("""
DiscordChatGPT Copyright (C) 2023  Linares Julien
This program comes with ABSOLUTELY NO WARRANTY; for details look at README.md and LICENSE files.
This is free software, and you are welcome to redistribute it
under certain conditions; for details look at README.md and LICENSE files.""")





openai.api_key = "your_api_key"


client = discord.Client()

# Créez un dictionnaire pour stocker les messages précédents et leur contexte
message_history = {}

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.channel.name != "chatgpt":
    return
  # Utilisez GPT-3 pour générer une réponse en utilisant l'historique des messages comme contexte
  prompt = f"{message.author.mention} a dit : {message.content}\n"
  prompt += "\n tu est un chat bot et la suite est simplement le contexte de la conversation (ta mémoire), utilise seulment les choses pertinente mais pas tout:\n"
  for msg_id, msg_content in message_history.items():
    prompt += f"{msg_content}\n"
  response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024).get("choices")[0].text
  # Ajoutez le nouveau message au dictionnaire de l'historique des messages
  message_history[f'{message.id}'] = f'{message.author.mention} a dit : {message.content}'
  message_history[f'{message.id}res'] = f"j'ai répondu (moi, le chat bot): {response}"

  # Envoyez la réponse à l'utilisateur via le serveur Discord
  # Sépare le message en plusieurs s'il est trop long pour Discord
  for chunk in [response[i:i+2000] for i in range(0, len(response), 2000)]:
        await message.channel.send(chunk)

client.run("your_discord_bot_token")
