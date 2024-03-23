import time, requests, telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if msg['text'] == '/start':
        bot.sendMessage(chat_id, 'Welcome to SkyLoom!')

    else:
        location = msg['text']

        try:
            temperature = get_weather_data(location)
            temperature_f = (temperature - 273.15) * 9/5 + 32
            temperature_f_txt = f"Temperature: {temperature_f:.2f} °F"

            query_data = str(temperature)+'_c'
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Show in Celcius', callback_data=query_data)],
            ])

            bot.sendMessage(chat_id, temperature_f_txt, reply_markup=keyboard)

        except:
            bot.sendMessage(chat_id, 'Unknown Location!\nPlease use /start to begin.', reply_markup=create_start_button())
        
def create_start_button():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]])

def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    
    message_id = msg['message']['message_id']

    query_data = query_data.split("_")

    temperature = float(query_data[0])

    if query_data[1] == 'c':
        temperature_c = temperature - 273.15
        temperature_c_txt = f"Temperature: {temperature_c:.2f} °C"

        query_data = str(temperature)+'_f'
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Show in Fahrenheit', callback_data=query_data)],
        ])

        bot.editMessageText((chat_id, message_id), temperature_c_txt, reply_markup=keyboard)
    
    else:
        temperature_f = (temperature - 273.15) * 9/5 + 32
        temperature_f_txt = f"Temperature: {temperature_f:.2f} °F"

        query_data = str(temperature)+'_c'
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Show in Celcius', callback_data=query_data)],
        ])
  
        bot.editMessageText((chat_id, message_id), temperature_f_txt, reply_markup=keyboard)

def get_weather_data(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=fb0a12bf21012a1080dc82c63b058a8c"
        response = requests.get(url)
        data = response.json()

        temperature = data['main']['temp']
        return temperature
    except:
        return "Error fetching weather data"

TOKEN = '6774309302:AAG_Occqk52D57rZdPrZB2UhC2Ad_1p41XA'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening...')

while 1:
    time.sleep(10)



