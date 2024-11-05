"""ServerManagerBot Core."""

from logging import getLogger
from os import getenv, listdir, path

from discord import CustomActivity, Intents, Status
from discord.app_commands import AppCommandContext, AppInstallationType
from discord.ext.commands import Bot


class ServerManagerBot(Bot):
    """ServerManagerBotの各種初期化.

    v0.1.0で追加
    """

    def __init__(self) -> None:
        """commands.Botを初期化します.

        v0.1.0で追加
        """
        super().__init__(
            command_prefix=".",
            help_command=None,
            allowed_contexts=AppCommandContext(
                guild=True, dm_channel=False, private_channel=False
            ),
            allowed_installs=AppInstallationType(guild=True, user=False),
            intents=self.get_intents(),
            status=Status.idle,
            activity=CustomActivity("Activating..."),
        )
        self.logger = getLogger("discord.client")

    def get_intents(self) -> Intents:
        """intentsを返します.

        v0.1.0で追加
        """
        intents = Intents.default()
        intents.typing = False
        intents.message_content = True
        return intents

    def get_token(self) -> str:
        """tokenをenvから取得し、返します.

        tokenの値がない場合はValueErrorが発生します.

        v0.1.0で追加
        """
        token = getenv("DISCORD_BOT_TOKEN")
        if token is None:
            raise ValueError("tokenが未設定です")
        return token

    async def cog_load(self, dir_path: str = "src/cogs") -> None:
        """Cogを再帰的検索で読み込む.

        v0.1.0で追加
        """
        for name in listdir(dir_path):
            full_path = path.join(dir_path, name)
            if path.isdir(full_path):
                await self.cog_load(full_path)
            elif name.endswith(".py") and not name.startswith("__"):
                relative_path = path.relpath(full_path, "src")
                cog_path = f"src.{relative_path.replace(path.sep, ".")[:-3]}"
                await self.load_extension(cog_path)
                self.logger.info(f"Cog Loading: {cog_path}")

    async def setup_hook(self) -> None:
        """Cogの読み込みなどをする関数.

        v0.1.0で追加
        """
        await self.cog_load()
        # await self.tree.sync()


def run() -> None:
    """モジュール実行用の関数.

    v0.1.0で追加
    """
    bot = ServerManagerBot()
    bot.run(bot.get_token())
