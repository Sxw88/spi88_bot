from telegram.ext import Updater, CallbackContext, InlineQueryHandler, CommandHandler
from telegram import Update
import requests
import random
import time
import re

path_to_bot = "/home/spi/spi88_bot/"

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
            'x-rapidapi-key': "[CENSORED]"
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

def bop(update: Update, context: CallbackContext):
    url = get_image_url()
    #chat_id = update.message.chat_id
    #bot.send_photo(chat_id=chat_id, photo=url)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)

def tellip(update: Update, context: CallbackContext):
    ip_add = get_my_ip()
    context.bot.send_message(chat_id=update.effective_chat.id, text=ip_add)

def joke(update: Update, context: CallbackContext):
    joke_msg = get_joke()
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke_msg)

def truth(update: Update, context: CallbackContext):
    truth_msg = get_truth()
    context.bot.send_message(chat_id=update.effective_chat.id, text=truth_msg)

def dare(update: Update, context: CallbackContext):
    dare_msg = get_dare()
    context.bot.send_message(chat_id=update.effective_chat.id, text=dare_msg)

def helpp(update: Update, context: CallbackContext):
    help_msg = get_help()
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)

def hi(update: Update, context: CallbackContext):
    hi_msg="hi what's up"
    context.bot.send_message(chat_id=update.effective_chat.id, text=hi_msg)

def main():
    updater = Updater('[CENSORED]', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('tellip',tellip))
    dp.add_handler(CommandHandler('joke',joke))
    dp.add_handler(CommandHandler('truth',truth))
    dp.add_handler(CommandHandler('dare',dare))
    dp.add_handler(CommandHandler('help',helpp))
    dp.add_handler(CommandHandler('hi',hi))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
