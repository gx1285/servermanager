"""Cog file."""

from logging import getLogger

import discord
from discord.app_commands import AppCommandError
from discord.ext.commands import Cog, Context
from discord.ext.commands.errors import CommandError

from src.core import ServerManagerBot


class ErrorHandler(Cog):
    """エラーハンドラー.

    v0.1.0で追加
    """

    def __init__(self, bot: ServerManagerBot):
        """クラス初期化.

        v0.1.0で追加.
        """
        self.bot = bot
        bot.tree.error(coro=self.__dispatch_tree_error_handle)

    async def __dispatch_tree_error_handle(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        self.bot.dispatch("application_command_error", interaction, error)

    @Cog.listener("on_command_error")
    async def on_command_error(
        self, ctx: Context[ServerManagerBot], exc: CommandError
    ) -> None:
        """メッセージコマンドのエラーハンドリング.

        v0.1.0で追加
        """
        logger = getLogger("discord.ext.Bot")
        logger.error("Ignoring exception in command %s", ctx, exc_info=exc)

    @Cog.listener("on_application_command_error")
    async def on_application_command_error(
        self, interaction: discord.Interaction, er: AppCommandError
    ) -> None:
        """インタラクションコマンドのエラーハンドリング."""
        logger = getLogger("discord.app_commands")
        command = interaction.command
        if command is not None:
            if command._has_any_error_handlers():
                return
            name = command.name
            logger.error("Ignoring exception in command %r", name, exc_info=er)
        else:
            logger.error("Ignoring exception in command tree", exc_info=er)


async def setup(bot: ServerManagerBot) -> None:
    """読み込み関数.

    v0.1.0で追加
    """
    await bot.add_cog(ErrorHandler(bot))
