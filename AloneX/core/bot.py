# Copyright (c) 2025 TheHamkerAlone 
# Licensed under the MIT License.
# This file is part of AloneXMusic


import pyrogram

from AloneX import config, logger


class Bot(pyrogram.Client):
    def __init__(self, bot_token: str = None):
        kwargs = {
            "name": "AloneX" if not bot_token else f"Clone_{bot_token.split(':')[0]}",
            "api_id": config.API_ID,
            "api_hash": config.API_HASH,
            "bot_token": bot_token or config.BOT_TOKEN,
            "parse_mode": pyrogram.enums.ParseMode.HTML,
            "max_concurrent_transmissions": 7,
        }
        if hasattr(pyrogram.types, "LinkPreviewOptions"):
            kwargs["link_preview_options"] = pyrogram.types.LinkPreviewOptions(is_disabled=True)
        super().__init__(**kwargs)
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention
        return self

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        await self.start()

        if self.logger:
            try:
                try:
                    await self.get_chat(self.logger)
                except:
                    pass
                await self.send_message(self.logger, "Bot Started")
                get = await self.get_chat_member(self.logger, self.id)
                if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
                    logger.error("Please promote the bot as an admin in logger group.")
            except Exception as ex:
                logger.error(
                    f"Bot has failed to access the log group: {self.logger}\n"
                    f"Reason: {ex}\n\n"
                    "Please make sure:\n"
                    "1. The LOGGER_ID is correct.\n"
                    "2. The bot is an admin in the log group.\n"
                    "3. You have sent a message or mentioned the bot in the group."
                )
        logger.info(f"Bot started as @{self.username}")

    def copy_handlers(self, client: pyrogram.Client):
        """
        Copies handlers from another Pyrogram client to this bot.
        """
        for group, handlers in client.dispatcher.groups.items():
            for handler in handlers:
                self.add_handler(handler, group)

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
