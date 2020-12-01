import telebot
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection(u'users')

# Use your telegram bot here
bot = telebot.TeleBot("")

# Promo code for the event
code = ["CODE","YOUAREAMAZING"]
redeeming = False
  
# Enables redemption mode
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    users = users_ref.where(u'tele', u'==', message.chat.username).stream()
    user = False
    for user in users:
        user = True

    msg = "Kindly enter your code"
    if user:
        msg = "You have already redeemed for this event!"
    else:
        global redeeming
        redeeming = True
    bot.send_message(message.chat.id,msg)


# Redemption mode
@bot.message_handler(func = lambda m : redeeming)
def redemption(message):
    global redeeming
    if message.text == '/cancel':
        bot.send_message(message.chat.id,"Redemption cancelled")
        redeeming = False
    elif message.text in code:
        # Enter all promo codes here
        bot.send_message(message.chat.id,"You have successfully redeemed your promo code!")

        file = open('promo.txt')
        for promotion in file:
            promotion = promotion.split(",")
            bot.send_photo(message.chat.id,open(promotion[0],'rb'),promotion[1])
            
        redeeming = False
        user = {
            u'lastname': message.chat.last_name,
            u'name': message.chat.first_name,
            u'tele': message.chat.username
        }
        users_ref.document().set(user)
    else:
        bot.send_message(message.chat.id,"You have entered an invalid code, please try again or type /cancel")

# Asks the user to /redeem upon entering any message, /start or /help
@bot.message_handler(func = lambda m : not redeeming)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! Please type /redeem to redeem your code")

bot.polling()