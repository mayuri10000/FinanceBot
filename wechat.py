# This file is executable. It can initialize a WeChat based interface
# it will require you to scan a QR code to login to WeChat and enter a name of a friend
# then the bot will automatically chat with that friend.
# NOTE: THIS FUNCTION IS NOT TESTED due to the login limitation of my WeChat account.
# PROBABLY BUGLY!

try:
    from wxpy import *
except:
    print('The WeChat interface is only avaliable when wxpy is installed!')
    exit(-1)

from Bot import Bot as MyBot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

print("Please scan the QR code to log in to WeChat")
wxbot = Bot()

friends = input("Enter the nickname of the friend you want the bot to chat with:")

while len(friends) == 0:
    friends = input("no friend matches. enter again:")

friend = friends[0]

print("Initialing bot...")
bot = MyBot()

@wxbot.register(friend)
def reply_my_friend(msg):
    bot_msg = bot.respond(msg.text)
    if isinstance(bot_msg, list):
        for a in list(bot_msg):
            if isinstance(a, str):
                msg.reply(a)
            elif isinstance(a, Figure):
                plt.savefig('temp.png')
                msg.reply_image('temp.png')
    elif isinstance(bot_msg, str):
        msg.reply(bot_msg)
    elif isinstance(bot_msg, Figure):
        plt.savefig('temp.png')
        msg.reply_image('temp.png')


if __name__ == '__main__':
    embed()
