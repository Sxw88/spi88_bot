from telegram.ext import Updater, CallbackContext, InlineQueryHandler, CommandHandler
from telegram import Update
import requests
import time
import re

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

def main():
    updater = Updater('[CENSORED]', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('tellip',tellip))
    dp.add_handler(CommandHandler('joke',joke))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
