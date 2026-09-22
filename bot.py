import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
):
    print(f"Erreur lors de l'exécution de /{interaction.command.name if interaction.command else '?'} : {error}")
    message = "❌ Une erreur est survenue lors de l'exécution de cette commande."
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


async def load_extensions():
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), "cogs")):
        if filename.endswith(".py") and not filename.startswith("__"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def setup_hook():
    # Charge les commandes (elles sont déployées séparément avec
    # `python deploy_commands.py`, comme `npm run deploy` dans la version JS).
    await load_extensions()


def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("❌ DISCORD_TOKEN manquant dans le fichier .env")
    bot.run(token)


if __name__ == "__main__":
    main()
