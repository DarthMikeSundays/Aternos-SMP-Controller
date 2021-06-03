from env_handler import TOKEN

from aternos_server import start

import discord

COMMAND_PREFIX = "mc:"


def main():
    client = discord.Client()
    COMMAND_TO_HANDLER = {
        "start": start_aternos_server,
    }

    @client.event
    async def on_message(message: str):
        if message.author == client.user:
            return

        command = message.content.replace(COMMAND_PREFIX, "")
        handler = COMMAND_TO_HANDLER[command]

        await handler(message)

    client.run(TOKEN)


async def start_aternos_server(message: str):
    await message.channel.send("started opening process...")
    start()
    await message.channel.send("finished opening process...")


if __name__ == '__main__':
    main()
