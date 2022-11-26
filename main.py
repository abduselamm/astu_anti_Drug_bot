import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
# States storage
from telebot.storage import StateMemoryStorage

from constant import API_KEY
state_storage = StateMemoryStorage()

bot = telebot.TeleBot(API_KEY, parse_mode=None,
state_storage=state_storage)

class MyStates(StatesGroup):
    name = State() 
    department = State()
    acadamicyear = State()
    phoneno = State()


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    bot.send_message(message.chat.id, 'enter full Name')
    

    

# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)


 
@bot.message_handler(state=MyStates.name)
def ask_department(message):
    bot.send_message(message.chat.id, "What is your Department?")
    bot.set_state(message.from_user.id, MyStates.department, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
def menub():
    markup = InlineKeyboardMarkup()
    markup.width =1
    markup.add(
                InlineKeyboardButton('1st',callback_data='1'),
                InlineKeyboardButton('2nd',callback_data='2'),
                InlineKeyboardButton('3rd',callback_data='3'),
                InlineKeyboardButton('4th',callback_data='4'),
                InlineKeyboardButton('5th',callback_data='5'),
                )
    return markup 
@bot.message_handler(state=MyStates.department)
def ask_acadamicyear(message):
    bot.send_message(message.chat.id, "acadamic year",reply_markup=menub())
    bot.set_state(message.from_user.id, MyStates.acadamicyear, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['department'] = message.text

#incorrect number
@bot.callback_query_handler(func=lambda m : True)
#@bot.message_handler(state=MyStates.acadamicyear)
def ask_phoneno(message):
    bot.send_message(message.from_user.id, "please-Phone number")
    bot.set_state(message.from_user.id, MyStates.phoneno, message.from_user.id)
    with bot.retrieve_data(message.from_user.id, message.from_user.id) as data:
        data['acadamicyear'] = message.data
 
# result
@bot.message_handler(state=MyStates.phoneno)
def ready_for_answer(message):
   
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Congratulations! you are now member of the club. We will contact you soon. Thank you!\n<b>"
               f"Name: {data['name']}\n"
               f"Department: {data['department']}\n"
               f"Acadamic year: {data['acadamicyear']}\n"
               f"Phone number: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
        bot.send_message(736179579,msg,parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)



