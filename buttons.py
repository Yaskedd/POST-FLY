from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

def subscribe_button():
    builder = InlineKeyboardBuilder()
    builder.button(text='♻Подписаться',url='t.me/post_publishhh')
    builder.button(text='❓Проверить подписку',callback_data='check_subscribe')
    builder.adjust(1,1)
    return builder.as_markup()

def reply_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text='🔗Привязка бота')
    builder.button(text='📃Новый пост')
    builder.button(text='🛠Тех.поддержка')
    builder.adjust(2,2)
    return builder.as_markup(resize_keyboard=True)

def link_the_bot():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить в канал',url='https://t.me/post_publishh_bot?startchannel&admin=change_info+post_messages+edit_messages+delete_messages+invite_users+pin_messages')
    builder.button(text='➕Добавить в группу',url='http://t.me/post_publishh_bot?startgroup&admin=change_info+delete_messages+invite_users+pin_messages')
    builder.adjust(2)
    return builder.as_markup()

def link_the_more():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить ещё',callback_data='add_more')
    builder.button(text='➕Новый пост',callback_data='new_publish')
    builder.adjust(1,1)
    return builder.as_markup()
    
def post_format():
    builder = InlineKeyboardBuilder()
    builder.button(text='✏Стандартный',callback_data='deafult_post')
    builder.button(text='📸С фото',callback_data='post_with_photo')
    builder.button(text='🎥C видео',callback_data='post_with_video')
    builder.button(text='🔉С аудио',callback_data='post_with_audio')
    builder.adjust(2,2)
    return builder.as_markup()

def edit_post():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить кнопку',callback_data='url_button')
    builder.button(text='🔁Изменить текст',callback_data='edit_text')
    builder.button(text='Продолжить➡',callback_data='continue')
    builder.adjust(2,1)
    return builder.as_markup()

def edit_post_photo():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить кнопку',callback_data='url_button_photo')
    builder.button(text='🔁Изменить текст',callback_data='edit_caption')
    builder.button(text='🔁Изменить фото',callback_data='edit_photo')
    builder.button(text='Продолжить➡',callback_data='continue_photo')
    builder.adjust(2,1)
    return builder.as_markup()

def edit_post_with_audio():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить подпись',callback_data='caption_audio')
    builder.button(text='➕Добавить кнопку', callback_data='url_button_audio')
    builder.button(text='🔁Изменить аудио',callback_data='changed_audio')
    builder.button(text='Продолжить➡',callback_data='continue_audio')
    builder.adjust(2,2)
    return builder.as_markup()

def edit_post_video():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить кнопку',callback_data='url_button_video')
    builder.button(text='🔁Изменить текст',callback_data='edit_caption2')
    builder.button(text='🔁Изменить видео',callback_data='edit_video')
    builder.button(text='Продолжить➡',callback_data='continue_video')
    builder.adjust(2,1)
    return builder.as_markup()

def edit_post_audio():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить кнопку', callback_data='url_button_audio')
    builder.button(text='🔁Изменить подпись',callback_data='change_caption')
    builder.button(text='🔁Изменить аудио',callback_data='changed_audio') 
    builder.button(text='Продолжить➡',callback_data='continue_audio')
    builder.adjust(2,2)
    return builder.as_markup()

def edit_post_with_photo():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить подпись',callback_data='caption_photo')
    builder.button(text='➕Добавить кнопку',callback_data='url_button_photo')
    builder.button(text='🔁Изменить фото',callback_data='edit_photo')
    builder.button(text='Продолжить➡',callback_data='continue_photo')
    builder.adjust(2,1,1)
    return builder.as_markup()

def edit_post_with_video():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Добавить подпись',callback_data='caption_video')
    builder.button(text='➕Добавить кнопку',callback_data='url_button_video')
    builder.button(text='🔁Изменить видео',callback_data='edit_video')
    builder.button(text='Продолжить➡',callback_data='continue_video')
    builder.adjust(2,1,1)
    return builder.as_markup()

def button_colour1():
    builder = InlineKeyboardBuilder()
    builder.button(text='красный',callback_data='red',style='danger')
    builder.button(text='зелёный',callback_data='green',style='success')
    builder.button(text='синий',callback_data='blue',style='primary')
    builder.button(text='без цвета',callback_data='no_colour')
    builder.adjust(1,1,1)
    return builder.as_markup()

def button_colour2():
    builder = InlineKeyboardBuilder()
    builder.button(text='красный',callback_data='red1',style='danger')
    builder.button(text='зелёный',callback_data='green1',style='success')
    builder.button(text='синий',callback_data='blue1',style='primary')
    builder.button(text='без цвета',callback_data='no_colour1')
    builder.adjust(1,1,1)
    return builder.as_markup()

def button_colour3():
    builder = InlineKeyboardBuilder()
    builder.button(text='красный',callback_data='red2',style='danger')
    builder.button(text='зелёный',callback_data='green2',style='success')
    builder.button(text='синий',callback_data='blue2',style='primary')
    builder.button(text='без цвета',callback_data='no_colour2')
    builder.adjust(1,1,1,1)
    return builder.as_markup()

def button_colour4():
    builder = InlineKeyboardBuilder()
    builder.button(text='красный',callback_data='red4',style='danger')
    builder.button(text='зелёный',callback_data='green4',style='success')
    builder.button(text='синий',callback_data='blue4',style='primary')
    builder.button(text='без цвета',callback_data='no_colour4')
    builder.adjust(1,1,1,1)
    return builder.as_markup()

def button_today():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить сейчас',callback_data='publish_now')
    builder.button(text='🕒Оправить сегодня',callback_data='today')
    builder.button(text='🗑Удалить пост',callback_data='del')
    builder.adjust(1,1)
    return builder.as_markup()

def button_today1():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить сейчас',callback_data='publish_now1')
    builder.button(text='🕒Оправить сегодня',callback_data='today1')
    builder.button(text='🗑Удалить пост',callback_data='del')
    builder.adjust(1,1)
    return builder.as_markup()

def button_today2():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить сейчас',callback_data='publish_now2')
    builder.button(text='🕒Оправить сегодня',callback_data='today2')
    builder.button(text='🗑Удалить пост',callback_data='del')
    builder.adjust(1,1,1)
    return builder.as_markup()

def button_today3():
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить сейчас',callback_data='publish_now3')
    builder.button(text='🕒Оправить сегодня',callback_data='today3')
    builder.button(text='🗑Удалить пост',callback_data='del')
    builder.adjust(1,1,1)
    return builder.as_markup()    

def edit_time_photo():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔁Изменить',callback_data='edit_time1')
    builder.button(text='Продолжить➡',callback_data='continue_time1')
    builder.adjust(1,1)
    return builder.as_markup()

def edit_time_video():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔁Изменить',callback_data='edit_time2')
    builder.button(text='Продолжить➡',callback_data='continue_time2')
    builder.adjust(1,1)
    return builder.as_markup()

def edit_time_audio():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔁Изменить',callback_data='edit_time3')
    builder.button(text='Продолжить➡',callback_data='continue_time3')
    builder.adjust(1,1)
    return builder.as_markup()
    
def edit_time01():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔁Изменить',callback_data='edit_time')
    builder.button(text='Продолжить➡',callback_data='continue_time')
    builder.adjust(1,1)
    return builder.as_markup()

def date_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='1',callback_data='1')
    builder.button(text='2',callback_data='2')
    builder.button(text='3',callback_data='3')
    builder.button(text='4',callback_data='4')
    builder.button(text='5',callback_data='5')
    builder.button(text='6',callback_data='6')
    builder.button(text='7',callback_data='7')
    builder.button(text='8',callback_data='8')
    builder.button(text='9',callback_data='9')
    builder.button(text='10',callback_data='10')
    builder.button(text='⏩',callback_data='next')
    builder.button(text='Сегодня',callback_data='no_data')
    builder.adjust(3,3,3,2,1)
    return builder.as_markup()

def data_keyboard1():
    builder = InlineKeyboardBuilder()
    builder.button(text='11',callback_data='11')
    builder.button(text='12',callback_data='12')
    builder.button(text='13',callback_data='13')
    builder.button(text='14',callback_data='14')
    builder.button(text='15',callback_data='15')
    builder.button(text='16',callback_data='16')
    builder.button(text='17',callback_data='17')
    builder.button(text='18',callback_data='18')
    builder.button(text='19',callback_data='19')
    builder.button(text='⏪',callback_data='back')
    builder.button(text='20',callback_data='20')
    builder.button(text='⏩',callback_data='next1')
    builder.button(text='Сегодня',callback_data='no_data')    
    builder.adjust(3,3,3,3,1)
    return builder.as_markup()

def data_keyboard2():
    builder = InlineKeyboardBuilder()
    builder.button(text='21',callback_data='21')
    builder.button(text='22',callback_data='22')
    builder.button(text='23',callback_data='23')
    builder.button(text='24',callback_data='24')
    builder.button(text='25',callback_data='25')
    builder.button(text='26',callback_data='26')
    builder.button(text='27',callback_data='27')
    builder.button(text='28',callback_data='28')
    builder.button(text='29',callback_data='29')
    builder.button(text='⏪',callback_data='back1')
    builder.button(text='30',callback_data='30')
    builder.button(text='31',callback_data='31')
    builder.button(text='Сегодня',callback_data='no_data')    
    builder.adjust(3,3,3,3,1)
    return builder.as_markup()

def new_post100():
    builder = InlineKeyboardBuilder()
    builder.button(text='➕Создать ещё',callback_data='post_post')
    builder.adjust(1)
    return builder.as_markup()