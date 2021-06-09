from env_handler import TOKEN

from aternos_server import start, end

from discord.ext import commands

COMMAND_PREFIX = "mc:"


def main():
    bot = commands.Bot(COMMAND_PREFIX)
    bot.add_command(start)
    bot.add_command(end)

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
