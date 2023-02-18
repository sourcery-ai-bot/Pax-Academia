from dataclasses import dataclass

from discord import option, Member
from discord.ext import commands
from discord.commands.context import ApplicationContext
from enum import Enum

from util.EmbedBuilder import EmbedBuilder

TIPS = {
    "Ask Your Question": (
        "You can be helped sooner if you simply ask your question, instead of "
        "asking if you can ask a question or if anyone is available to help you.\n\n"
        "Instead of asking "
        '"Does anyone know X?", "Can someone help me with Y?", or "Are there any experts in Z?" '
        "just ask your question or describe your problem directly."
    ),
    "Format Your Code": (
        "It's much easier to read specially formatted code. "
        "You can format code on discord by using 3 backticks `` ``` `` (**not** quotes `'''`) "
        "followed by the name of the computer language (so for Python code: `` ```python``).\n\n"
        "Lets use Java as an example.\n\n"
        "This message:\n"
        "**\\`\\`\\`java\n"
        'System.out.println("Code formatting is neat!");\n'
        "\\`\\`\\`**\n\n"
        "Will look like this:\n"
        "```java\n"
        'System.out.println("Code formatting is neat!");\n'
        "```\n"
        "Go ahead, try it! You can copy/paste the message above."
    ),
    "Let Us Know What You've Already Tried": (
        "Please show and describe the steps you've already completed so that we may assist you further.\n"
        "This way, we can start helping you right where you left off and can save everyone's time."
    ),
}


class Tips(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="tip", description="Sends various homework-help tips.")
    @option(
        name="tip",
        description="The tip to send.",
        type=str,
        choices=TIPS,
        required=True,
    )
    @option(
        name="ping",
        description="Who should be pinged with the tip?",
        type=Member,
        required=False,
    )
    @option(
        name="anonymous",
        description="Should the tip be sent anonymously?",
        type=str,
        choices=["Yes", "No"],
        required=False,
    )
    async def tip(self, ctx: ApplicationContext, tip: str, ping: Member | None = None, anonymous: str = "No") -> None:
        message_content = None if ping is None else ping.mention
        embed = EmbedBuilder(
            title=f"Tip: {tip.capitalize()}.",
            description=TIPS[tip],
            color=0x32DC64,  # a nice pastel green
        ).build()

        if anonymous.casefold() == "yes":
            await ctx.send(message_content, embed=embed)
            await ctx.respond("Thanks for the tip! It was sent anonymously.", ephemeral=True, delete_after=5)
        else:
            await ctx.respond(message_content, embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Tips(bot))