# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic


from pyrogram import Client

from AloneX import config, logger


class Userbot(Client):
    def __init__(self):
        """
        Initializes the userbot with multiple clients.

        This method sets up clients for the userbot using predefined session strings.
        Each client is assigned a unique name based on the key in the `clients` dictionary.
        """
        self.clients = []
        self.custom_clients = {}
        clients = {"one": "SESSION1", "two": "SESSION2", "three": "SESSION3"}
        for key, string_key in clients.items():
            name = f"AloneXUB{key[-1]}"
            session = getattr(config, string_key)
            if session:
                setattr(
                    self,
                    key,
                    Client(
                        name=name,
                        api_id=config.API_ID,
                        api_hash=config.API_HASH,
                        session_string=session,
                    ),
                )
            else:
                setattr(self, key, None)

    async def boot_client(self, num: int, ub: Client):
        """
        Boot a client and perform initial setup.
        Args:
            num (int): The client number to boot (1, 2, or 3).
            ub (Client): The userbot client instance.
        Raises:
            SystemExit: If the client fails to send a message in the log group.
        """
        clients = {
            1: self.one,
            2: self.two,
            3: self.three,
        }
        client = clients[num]
        if not client:
            return
        await client.start()
        if config.LOGGER_ID:
            try:
                try:
                    await client.get_chat(config.LOGGER_ID)
                except:
                    pass
                await client.send_message(config.LOGGER_ID, "Assistant Started")
            except Exception as ex:
                logger.error(
                    f"Assistant {num} failed to access the log group: {config.LOGGER_ID}\n"
                    f"Reason: {ex}"
                )

        client.id = ub.me.id
        client.name = ub.me.first_name
        client.username = ub.me.username
        client.mention = ub.me.mention
        self.clients.append(client)
        try:
            await ub.join_chat("AloneUpdates")
        except:
            pass
        logger.info(f"Assistant {num} started as @{client.username}")

    async def start_custom_assistant(self, bot_id: int, api_id: int, api_hash: str, session: str):
        if bot_id in self.custom_clients:
            try:
                await self.custom_clients[bot_id].stop()
            except:
                pass

        client = Client(
            name=f"Assistant_{bot_id}",
            api_id=api_id,
            api_hash=api_hash,
            session_string=session,
            in_memory=True,
        )
        await client.start()
        client.id = client.me.id
        client.name = client.me.first_name
        client.username = client.me.username
        client.mention = client.me.mention

        self.custom_clients[bot_id] = client
        return client

    async def boot(self):
        """
        Asynchronously starts the assistants.
        """
        if config.SESSION1:
            await self.boot_client(1, self.one)
        if config.SESSION2:
            await self.boot_client(2, self.two)
        if config.SESSION3:
            await self.boot_client(3, self.three)

    async def exit(self):
        """
        Asynchronously stops the assistants.
        """
        if self.one:
            await self.one.stop()
        if self.two:
            await self.two.stop()
        if self.three:
            await self.three.stop()
        for client in self.custom_clients.values():
            try:
                await client.stop()
            except:
                pass
        logger.info("Assistants stopped.")
