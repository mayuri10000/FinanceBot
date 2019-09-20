# This file is executable, showing a command-line interface of the bot
# Note: plots will be shown in separate windows.

from Bot import Bot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print("Initializing bot, please wait...")
    try:
        bot = Bot()
    except:
        print("Error occurred while initializing bot! Exiting...")
        exit(-1)

    print("Welcome to the Finance Bot!")
    print("I am not a professional bot, please don't ask me weired questions.")
    print("Please end every company name with 'Inc.', and make sure dates are in format like '2019-01-01'")
    print("If you want to exit, just type 'exit'.")

    while True:
        user_msg = input("USER:  ")
        if user_msg.lower() == 'exit':
            print("BOT:   Bye!")
            exit(0)
        bot_msg = bot.respond(user_msg)
        if isinstance(bot_msg, list):
            for a in list(bot_msg):
                if isinstance(a, str):
                    print("BOT:   {}".format(a))
                elif isinstance(a, Figure):
                    print("BOT:   [The bot sent a graph and it's shown in a separate window.]")
                    plt.show()
                    plt.close()
        elif isinstance(bot_msg, str):
            print("BOT:   {}".format(bot_msg))
        elif isinstance(bot_msg, Figure):
            print("BOT:   [The bot sent a graph and it's shown in a separate window.]")
            plt.show()
            plt.close()


