"""Cog file."""

from typing import cast

from discord import ClientUser, CustomActivity, Status
from discord.ext.commands import Cog

from src.core import ServerManagerBot


class ReadyHandle(Cog):
    """起動時の処理.

    v0.1.0で追加
    """

    def __init__(self, bot: ServerManagerBot) -> None:
        """クラス初期化.

        v0.1.0で追加.
        """
        self.bot = bot

    @Cog.listener("on_ready")
    async def on_ready(self) -> None:
        """起動時の処理.

        v0.1.0で追加
        """
        bot = cast(ClientUser, self.bot.user)
        self.bot.logger.info(f"Activated Bot: {bot.name}#{bot.discriminator}")
        await self.bot.change_presence(
            activity=CustomActivity(f"/help | {len(self.bot.guilds)} Server."),
            status=Status.online,
        )


async def setup(bot: ServerManagerBot) -> None:
    """読み込み関数.

    v0.1.0で追加
    """
    await bot.add_cog(ReadyHandle(bot))
