import discord
from discord import app_commands
from discord.ext import commands
import logging
import sys
from utils import format_number, validate_xp_input, parse_xp_input
from level_data import level_xp

# Constants
LOSS_RATE = 0.0506  # 5.06% expected loss
ALLOWED_CHANNEL_ID = 1369342681657901229  # Only listen in this channel

logger = logging.getLogger(__name__)


class XPCalculator(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} ({self.user.id})")
        activity = discord.Activity(type=discord.ActivityType.listening,
                                    name="/xpgoal")
        await self.change_presence(activity=activity)


def setup_and_run_bot(token):
    bot = XPCalculator()

    @bot.tree.command(
        name="xpgoal",
        description=
        "Calculate how much wager and loss is needed to reach your XP goal")
    @app_commands.describe(
        target_xp="Your XP goal (e.g., 4,000,000 or 4.000.000)",
        current_xp="(Optional) Your current XP (e.g., 2,000,000)")
    async def xpgoal(interaction: discord.Interaction,
                     target_xp: str,
                     current_xp: str = None):
        if interaction.channel_id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message(
                "🚫 This command can only be used in the designated channel.",
                ephemeral=True)
            return

        if (validation := validate_xp_input(target_xp)) is not True:
            await interaction.response.send_message(
                f"❌ Target XP error: {validation}", ephemeral=True)
            return

        target_xp_int = parse_xp_input(target_xp)
        current_xp_int = 0

        if current_xp:
            if (validation := validate_xp_input(current_xp)) is not True:
                await interaction.response.send_message(
                    f"❌ Current XP error: {validation}", ephemeral=True)
                return
            current_xp_int = parse_xp_input(current_xp)

        xp_needed = max(0, target_xp_int - current_xp_int)
        wager = xp_needed / 400
        cost = wager * LOSS_RATE

        response = (f"🎯 **XP Goal:** {format_number(target_xp_int)} XP\n"
                    f"📍 **Current XP:** {format_number(current_xp_int)} XP\n"
                    f"📊 **XP Remaining:** {format_number(xp_needed)} XP\n\n"
                    f"💰 **Required Wager:** {format_number(wager)} Coins\n"
                    f"💸 **Estimated Loss:** {format_number(cost)} Coins "
                    f"({LOSS_RATE * 100:.2f}%)\n\n"
                    f"🎲 **Strategy:** Dice – 94% win chance at 1.01x")

        await interaction.response.send_message(response)

    @bot.tree.command(
        name="levelup",
        description=
        "Calculate wager and loss to reach a CSGORoll level using Dice strategy"
    )
    @app_commands.describe(
        target_level="Level you want to reach (1–100)",
        current_xp="Your current XP amount (e.g., 1,234,567)")
    async def levelup(interaction: discord.Interaction, target_level: int,
                      current_xp: str):
        if interaction.channel_id != ALLOWED_CHANNEL_ID:
            await interaction.response.send_message(
                "🚫 This command can only be used in the designated channel.",
                ephemeral=True)
            return

        if target_level < 1 or target_level > 100:
            await interaction.response.send_message(
                "❌ Level must be between 1 and 100.", ephemeral=True)
            return

        if (validation := validate_xp_input(current_xp)) is not True:
            await interaction.response.send_message(
                f"❌ XP input error: {validation}", ephemeral=True)
            return

        current = parse_xp_input(current_xp)
        needed = max(0, level_xp[target_level] - current)
        wager = needed / 400
        loss = wager * LOSS_RATE

        await interaction.response.send_message(
            f"🎯 **Target Level:** {target_level}\n"
            f"📊 **XP Needed:** {format_number(needed)} XP\n\n"
            f"💰 **Required Wager:** {format_number(wager)} Coins\n"
            f"💸 **Estimated Loss:** {format_number(loss)} Coins "
            f"({LOSS_RATE * 100:.2f}%)\n\n"
            f"🎲 **Strategy:** Dice – 94% win chance at 1.01x")

    try:
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        logger.error("Invalid Discord token.")
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
