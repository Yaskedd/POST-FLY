from aiogram.fsm.state import State,StatesGroup

class deafult_post(StatesGroup):
    post_format = State()

    text = State()
    button_title = State()
    button_url = State() 
    button_colour = State()
    time = State()

    photo = State()
    caption = State()
    button_title1 = State()
    button_url1 = State()
    button_colour1 = State()
    time1 = State()

    video = State()
    caption_video = State()
    button_title2 = State()
    button_url2 = State()
    button_colour2 = State()
    time2 = State()

    music = State()
    caption_music = State()
    button_title3 = State()
    button_url3 = State()
    button_colour3 = State()
    time3 = State()

    edit_music = State()
    edit_caption_music = State()
    edit_performer = State()
    edit_title_music = State()
    edit_time3 = State()
    edit_photo = State()
    edit_caption = State()
    edit_text = State()
    edit_time0 = State()
    edit_time1 = State()
    edit_video = State()
    edit_caption_video = State()
    edit_time2 = State()


    chat_id = State()
    chat_id2 = State()
    number = State()
    wating = State()
