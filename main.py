from telegram.ext import Updater, CallbackContext, InlineQueryHandler, CommandHandler
from telegram import Update
import subprocess
import requests
import random
import time
import re
import os


enc_file = "[location of encrypted token file]"
key_file = "[location of key to encrypted file]"
decryption_command = 'openssl enc -d -aes-256-cbc -pbkdf2 -in ' + enc_file + ' -pass file:' + key_file
my_token = os.popen(decryption_command).read()
my_token = my_token.rstrip(my_token[-1])


path_to_bot = "[replace with actual path to main.py]"
unauthorized_msg = "Your Telegram Chat ID is unauthorized UnU"

def check_plvl(chatid, plvl=0):
    str_chatid = str(chatid) # convert to string

    # read file containing authorized users
    #Privilege lvl2 lowest privilege level
    if plvl >= 2:
        plvl2 = []
        with open(path_to_bot+'authorized/lvl2.lst') as readfile:
            plvl2 = [line.rstrip() for line in readfile]
        if str_chatid in plvl2:
            return True


    #Privilege lvl1 middle privilege level
    if plvl >= 1:
        plvl1 = []
        with open(path_to_bot+'authorized/lvl1.lst') as readfile:
            plvl1 = [line.rstrip() for line in readfile]
        if str_chatid in plvl1:
            return True

    # Privilege lvl0 highest privilege level
    if plvl >= 0:
        plvl0 = []
        with open(path_to_bot+'authorized/lvl0.lst') as readfile:
            plvl0 = [line.rstrip() for line in readfile]
        if str_chatid in plvl0:
            return True

    return False


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def get_my_ip():
    contents = requests.get('https://ipinfo.io').json()
    ip_add = contents['ip']
    return ip_add

def get_joke():
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
    querystring = {'format':'txt'}
    headers = {
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com",
            'x-rapidapi-key': "[redacted]"
            }
    #contents = requests.get('https://jokeapi-v2.p.rapidapi.com/joke/Any').json()
    contents = requests.request("GET", url, headers=headers, params=querystring)
    return contents.text

def get_truth():
    path_to_file = path_to_bot + "truth.txt"
    truth_list = open(path_to_file, 'r')
    contents = "error: empty string"
    #checking number of lines in 'truth.txt', and then reset the pointer
    num_lines = sum(1 for line in truth_list)
    truth_list.seek(0)

    #use time as seed for random number generator
    random.seed(time.time())
    line_to_read = random.randint(1,num_lines)

    while line_to_read > 0:
        contents = truth_list.readline().strip()
        line_to_read -= 1

    truth_list.close()
    return contents

def get_dare():
    path_to_file = path_to_bot + "dare.txt"
    dare_list = open(path_to_file, 'r')
    contents = "error: empty string"
    #checking number of lines in 'truth.txt', and then reset the pointer
    num_lines = sum(1 for line in dare_list)
    dare_list.seek(0)

    #use time as seed for random number generator
    random.seed(time.time())
    line_to_read = random.randint(1,num_lines)

    while line_to_read > 0:
        contents = dare_list.readline().strip()
        line_to_read -= 1

    dare_list.close()
    return contents

def get_help():
    path_to_file = path_to_bot + "help.txt"
    help_txt = open(path_to_file, 'r')
    contents = help_txt.read()
    help_txt.close()
    return contents

def get_ifconfig():
    contents = subprocess.run(['ifconfig'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return contents

def get_tech():
    path_to_file = path_to_bot + "tech.txt"
    tech_txt = open(path_to_file, 'r')
    contents = tech_txt.read()
    tech_txt.close()
    return contents

def get_diceroll(dice_sides):
    if dice_sides > 1:
        diceroll = random.randint(1,dice_sides)     # roll a random number for the dice
    else:
        diceroll = "A dice cannot have less than 2 faces!"
    return diceroll



def bop(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 1):
        url = get_image_url()
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def tellip(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 1):
        ip_add = get_my_ip()
        context.bot.send_message(chat_id=update.effective_chat.id, text=ip_add)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def joke(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 1):
        joke_msg = get_joke()
        context.bot.send_message(chat_id=update.effective_chat.id, text=joke_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def truth(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 2):
        truth_msg = get_truth()
        context.bot.send_message(chat_id=update.effective_chat.id, text=truth_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def dare(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 2):
        dare_msg = get_dare()
        context.bot.send_message(chat_id=update.effective_chat.id, text=dare_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def helpp(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 2):
        help_msg = get_help()
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def hi(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 2):
        hi_msg="hi what's up"
        context.bot.send_message(chat_id=update.effective_chat.id, text=hi_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def roll(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 2):
        try:
            dice_roll=get_diceroll(int(context.args[0]))
        except (IndexError, ValueError):
            dice_roll='Usage: "/roll <int>" will roll a virtual dice with <int> sides'
        context.bot.send_message(chat_id=update.effective_chat.id, text=dice_roll)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def ifconfig(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        ifconfig_msg = get_ifconfig()
        context.bot.send_message(chat_id=update.effective_chat.id, text=ifconfig_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def chatid(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def restartnm(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        restartnm_msg = "Attempting to restart Network Manager..."
        context.bot.send_message(chat_id=update.effective_chat.id, text=restartnm_msg)
        #``run the script to restart NetworkManager
        path_to_script = path_to_bot + "restartNM.sh"
        subprocess.run(["sudo", path_to_script])
        #send second message to indicate attempted restart
        #timeout error seems to occur at this part, but does not affect the function
        restartnm_msg = "Recovering from restart attempt: /restartnmlog"
        context.bot.send_message(chat_id=update.effective_chat.id, text=restartnm_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def restartnmlog(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        #read the restartnm.log file
        path_to_file = path_to_bot + "restartnm.log"
        read_log = open(path_to_file, 'r')
        read_log_contents = read_log.read()
        context.bot.send_message(chat_id=update.effective_chat.id, text=read_log_contents)
        read_log.close()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def tech(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        tech_msg = get_tech()
        context.bot.send_message(chat_id=update.effective_chat.id, text=tech_msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def upd_ps_reverse(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        upd_msg = "Updating PowerShell-Reverse-Shell Payload with current IP address..."
        context.bot.send_message(chat_id=update.effective_chat.id, text=upd_msg)
        #run the script to update the files
        path_to_script = path_to_bot + "rvs-ip-update.sh"
        subprocess.run(["sudo", path_to_script])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)

def upd_ovpn(update: Update, context: CallbackContext):
    if check_plvl(update.effective_chat.id, 0):
        upd_msg = "Updating OVPN File with current IP address. Check this path for the updated OVPN file: https://" + str(get_my_ip()) + ":58443/files/secret/default-vpn-user.ovpn"
        context.bot.send_message(chat_id=update.effective_chat.id, text=upd_msg)
        #run the script to update the files
        path_to_script = path_to_bot + "updOVPN.sh"
        subprocess.run(["sudo", path_to_script])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=unauthorized_msg)


def main():
    updater = Updater(my_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('tellip',tellip))
    dp.add_handler(CommandHandler('joke',joke))
    dp.add_handler(CommandHandler('truth',truth))
    dp.add_handler(CommandHandler('dare',dare))
    dp.add_handler(CommandHandler('help',helpp))
    dp.add_handler(CommandHandler('hi',hi))
    dp.add_handler(CommandHandler('roll',roll))
    dp.add_handler(CommandHandler('ifconfig',ifconfig))
    dp.add_handler(CommandHandler('chatid', chatid))
    dp.add_handler(CommandHandler('restartnm',restartnm))
    dp.add_handler(CommandHandler('restartnmlog',restartnmlog))
    dp.add_handler(CommandHandler('tech',tech))
    dp.add_handler(CommandHandler('upd_ps_reverse',upd_ps_reverse))
    dp.add_handler(CommandHandler('upd_ovpn',upd_ovpn))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
