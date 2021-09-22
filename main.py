from env_handler import TOKEN

from aternos_server import start

from discord.ext import commands

COMMAND_PREFIX = "mc:"


def main():
    bot = commands.Bot(COMMAND_PREFIX)
    bot.add_command(start)

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
