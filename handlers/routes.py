from aiogram import Router,types,F,html,Bot
from aiogram.filters import Command
from aiogram.types import Message,ChatMemberUpdated
from buttons import reply_menu,link_the_bot,post_format,edit_post,button_colour1,button_today,edit_time01,edit_post_with_photo,edit_post_photo,button_colour2,button_today1,edit_time_photo,edit_post_with_video,edit_post_video,button_colour3,button_today2,edit_time_video,edit_post_with_audio,edit_post_audio,button_today3,button_colour4,edit_time_audio,link_the_more,date_keyboard,data_keyboard1,data_keyboard2,new_post100
from functions import sub_ver,deafult_publish,post_with_photo,post_with_video1,post_with_audio1
from Bot_db import get_chat_id,add_id,init_db,delete_id,name_id,get_user_id
import asyncio
from aiogram.fsm.context import FSMContext
from FSM import deafult_post
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from aiogram.types.input_file import FSInputFile 

router = Router()

async def new_post(message: Message, user_id):
    function = await get_chat_id(user_id=user_id)
    print(f'in db now {function}')
    if not function:
        await message.answer(
            text='🔗Перед использованием бот должен быть привязан к каналу или группе\n\n'
            'Чтобы привязать бота к каналу или группе,выполните несколько необходимых условиий:\n' 
            '<code>1</code>.Выберите место для привязки - телеграм канал или группа,нажав на одну из кнопок ниже\n' 
            '<code>2</code>.Выдайте боту право на публикацию сообщений.\nБез него бот не сможет публиковать посты и сообщения\n\n' \
            'После этого бот автоматически пришлет сообщение о привязке и его функционал станет доступным',
            parse_mode='HTML',
            reply_markup=link_the_bot())
        return
    else:
        await message.answer('📍Выберите место публикации поста',
        reply_markup= await place_publish(user_id=user_id))

async def place_publish(user_id):
    function = await name_id(user_id=user_id)
    builder = InlineKeyboardBuilder()  
    for name,id in function:
        builder.button(text=name, callback_data=f"ch:{id}") # K3 said me,that callback data ограничен 64 bit's поэтому так надежнее
    builder.adjust(1)
    return builder.as_markup()

async def deafult_post1(
    message: Message,
    state : FSMContext
):
    await message.answer('Введите желаемый текст для вашего поста')
    await state.set_state(deafult_post.text)

async def post_wiht_photo(message: Message,state: FSMContext):
    await message.answer('Отлично! Отправь фото для твоего поста')
    await state.set_state(deafult_post.photo)

async def post_with_video(message: Message, state: FSMContext):
    await message.answer('Отлично! Отправь видео для твоего поста')
    await state.set_state(deafult_post.video)

async def post_with_audio(message: Message, state: FSMContext):
    await message.answer('Отлично! Отправь аудио для твоего поста')
    await state.set_state(deafult_post.music)

@router.message(deafult_post.music)
async def parametr_music(message: Message, state: FSMContext):
    try:
        music = message.audio.file_id
        await state.update_data(music=music)
        await message.answer('Окей.Вот,что мы можем сделать ещё:\n\n'
        '• <b>Добавить подпись к твоему посту</b>\n'
        '• <b>Добавить URL кнопку к посту</b>\n'
        '• <b>Изменить аудио</b>\n'
        'Или сразу перейдём к публикации поста?',
        parse_mode="HTML",
        reply_markup=edit_post_with_audio())
    except Exception:
        await message.answer('⚠️Ошибка!\nНеправильный тип сообщения,пожалуйста отправьте аудио')
        return
    
@router.message(deafult_post.video)
async def parametr_video(message: Message, state: FSMContext):
    try:
        video = message.video.file_id
        await state.update_data(video=video)
        await message.answer('Окей.Вот,что мы можем сделать ещё:\n\n'
            '• <b>Добавить подпись к видео</b>\n'
            '• <b>Добавить URL кнопку к посту</b>\n'
            '• <b>Изменить видео</b>\n'
            'Или сразу перейдём к публикации поста?',
            parse_mode='HTML',
            reply_markup=edit_post_with_video())  
    except Exception:
        await message.answer('⚠️Ошибка!\nНеправильный тип сообщения,пожалуйста отправьте видео')
        return

@router.message(deafult_post.photo)
async def parametr_photo(message: Message,state: FSMContext):
    try:
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
        await message.answer('Окей.Вот,что мы можем сделать ещё:\n\n'
            '• <b>Добавить подпись к фото</b>\n'
            '• <b>Добавить URL кнопку к посту</b>\n'
            '• <b>Изменить фото</b>\n'
            'Или сразу перейдём к публикации поста?',
            parse_mode='HTML',
            reply_markup=edit_post_with_photo())
    except Exception:
        await message.answer('⚠️Ошибка!\nНеправильный тип сообщения,пожалуйста отправьте фото')
        return

@router.message(deafult_post.caption)
async def caption_with_photo(message: Message,state:FSMContext):
    try:
        caption = message.text
        data = await state.get_data()
        photo = data['photo']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(caption=caption)
        await message.answer_photo(photo=photo,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текст?',
            reply_markup=edit_post_photo(),
            parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Подпись должна быть текстом')
        return

@router.message(deafult_post.caption_music)
async def caption_with_audio(message: Message, state: FSMContext, bot: Bot):
    try:
        caption = message.text
        data = await state.get_data()
        audio = data['music']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(caption_music=caption)
        await message.answer_audio(audio=audio,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить аудио или подпись?',
        parse_mode='HTML',
        reply_markup=edit_post_audio())
    except Exception:
        await message.answer('❌Ошибка! Подпись должна быть текстом')
        return 

@router.message(deafult_post.caption_video)
async def caption_with_video(message: Message, state: FSMContext):
    try:
        caption = message.text
        data = await state.get_data()
        video = data['video']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(caption_video=caption)
        await message.answer_video(video=video,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить видео или подпись?',
            reply_markup=edit_post_video(),
            parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Подпись должна быть текстом')
        return

@router.message(deafult_post.text)
async def text_with_def_post(message: Message, state: FSMContext):
    try:
        user_message = message.text
        if len(user_message) >= 4096:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(text=user_message)
        await message.answer(
            f'<b>{user_message}</b>\n\nХотите добавить URL кнопку к вашей публикации или изменить текст?',
            parse_mode='HTML',
            reply_markup=edit_post())
    except Exception:
        await message.answer('⚠️Ошибка!\nНеправильный тип сообщения,пожалуйста отправьте текст')
        return

@router.message(deafult_post.button_title)
async def create_button(message: Message, state: FSMContext):
    try:
        string = message.text
        if len(string) > 18:
            await message.answer('Cлишком большое название!\nРекомендую выбрать короче <b>18</b> символов,иначе кнопка не вместит в себя всё название...',
            parse_mode='HTML')
            return
        await state.update_data(button_title=string)
        await message.answer('Следущее - сделаем кнопку интерактивной.\nОтправь URL ссылку,для твоей кнопки')
        await state.set_state(deafult_post.button_url)
    except Exception:
        await message.answer('❌Ошибка! Название кнопки должно быть текстом')
        return

@router.message(deafult_post.button_url)
async def button_url(message: Message, state: FSMContext):
    try:
        string_url = message.text 
        if 'https://' not in string_url:
            await message.answer('❌Ошибка!\nURL ссылка должна начинаться с "<code>https://</code>"',parse_mode='HTML')   
            return
        await state.update_data(button_url=string_url)
        await message.answer('Украсим нашу кнопку!\n Выбери для неё цвет:',reply_markup=button_colour1())
    except Exception:
        await message.answer('❌Ошибка!\nТип сообщения должен быть URL сылкой')
        return

@router.message(deafult_post.button_title3)
async def button_title_audio(message: Message, state: FSMContext):
    try:
        string = message.text
        if len(string) > 18:
            await message.answer('Cлишком большое название!\nРекомендую выбрать короче <b>18</b> символов,иначе кнопка не вместит в себя всё название...',
            parse_mode='HTML')
            return
        await state.update_data(button_title3=string)
        await message.answer('Следущее - сделаем кнопку интерактивной.\nОтправь URL ссылку,для твоей кнопки')
        await state.set_state(deafult_post.button_url3)
    except Exception:
        await message.answer('❌Ошибка! Название кнопки должно быть текстом')
        return    

@router.message(deafult_post.button_title1)
async def button_title_photo(message: Message,state:FSMContext):
    try:
        string = message.text
        if len(string) > 18:
            await message.answer('Cлишком большое название!\nРекомендую выбрать короче <b>18</b> символов,иначе кнопка не вместит в себя всё название...',
            parse_mode='HTML')
            return
        await state.update_data(button_title1=string)
        await message.answer('Следущее - сделаем кнопку интерактивной.\nОтправь URL ссылку,для твоей кнопки')
        await state.set_state(deafult_post.button_url1)
    except Exception:
        await message.answer('❌Ошибка! Название кнопки должно быть текстом')
        return

@router.message(deafult_post.button_title2)
async def button_title_video(message: Message, state: FSMContext):
    try:
        string = message.text
        if len(string) > 18:
            await message.answer('Cлишком большое название!\nРекомендую выбрать короче <b>18</b> символов,иначе кнопка не вместит в себя всё название...',
            parse_mode='HTML')
            return
        await state.update_data(button_title2=string)
        await message.answer('Следущее - сделаем кнопку интерактивной.\nОтправь URL ссылку,для твоей кнопки')
        await state.set_state(deafult_post.button_url2)
    except Exception:
        await message.answer('❌Ошибка! Название кнопки должно быть текстом')
        return

@router.message(deafult_post.button_url2)
async def button_url_video(message:Message,state:FSMContext):
    try:
        string_url = message.text 
        if 'https://' not in string_url:
            await message.answer('❌Ошибка!\nURL ссылка должна начинаться с "<code>https://</code>"',parse_mode='HTML')   
            return
        await state.update_data(button_url2=string_url)
        await message.answer('Украсим нашу кнопку!\n Выбери для неё цвет:',reply_markup=button_colour3())
    except Exception:
        await message.answer('❌Ошибка!\nТип сообщения должен быть URL сылкой')
        return

@router.message(deafult_post.button_url3)
async def button_url_audio(message: Message, state: FSMContext):
    try:
        string_url = message.text 
        if 'https://' not in string_url:
            await message.answer('❌Ошибка!\nURL ссылка должна начинаться с "<code>https://</code>"',parse_mode='HTML')   
            return
        await state.update_data(button_url3=string_url)
        await message.answer('Украсим нашу кнопку!\n Выбери для неё цвет:',reply_markup=button_colour4())
    except Exception:
        await message.answer('❌Ошибка!\nТип сообщения должен быть URL сылкой')
        return
    
@router.message(deafult_post.button_url1)
async def button_url_photo(message:Message,state:FSMContext):
    try:
        string_url = message.text 
        if 'https://' not in string_url:
            await message.answer('❌Ошибка!\nURL ссылка должна начинаться с "<code>https://</code>"',parse_mode='HTML')   
            return
        await state.update_data(button_url1=string_url)
        await message.answer('Украсим нашу кнопку!\n Выбери для неё цвет:',reply_markup=button_colour2())
    except Exception:
        await message.answer('❌Ошибка!\nТип сообщения должен быть URL сылкой')
        return
    
@router.message(deafult_post.edit_text)
async def edit_text(message:Message, state:FSMContext):
    try:
        user_message= message.text
        if len(user_message) >= 4096:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(edit_text=user_message)
        await message.answer(
                f'<b>{user_message}</b>\n\nХотите добавить URL кнопку к вашей публикации или изменить текст?',
                parse_mode='HTML',
                reply_markup=edit_post())
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте текс')
        return

@router.message(deafult_post.edit_caption)
async def edit_caption(message:Message,state:FSMContext):
    try:
        caption = message.text
        data = await state.get_data()
        if data.get('edit_photo') is None:
            photo = data['photo']
        else: 
            photo = data['edit_photo']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(edit_caption=caption)
        await message.answer_photo(photo=photo,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текс',
        reply_markup=edit_post_photo(),
        parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте текс')
        return

@router.message(deafult_post.edit_caption_music)
async def edit_cap_audio(message: Message, state: FSMContext):
    try:
        caption = message.text
        data = await state.get_data()
        if data.get('edit_music') is None:
            audio = data['music']
        else: 
            audio = data['edit_music']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(edit_caption_music=caption)
        await message.answer_audio(audio=audio,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текс',
        reply_markup=edit_post_audio(),
        parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте текс')
        return    

@router.message(deafult_post.edit_caption_video)
async def edit_caption1(message:Message,state:FSMContext):
    try:
        caption = message.text
        data = await state.get_data()
        if data.get('edit_video') is None:
            video = data['video']
        else: 
            video = data['edit_video']
        if len(caption) > 1024:
            await message.answer('❌Превышен лимит символов!\nПожалуйста попробуйте ещё раз')
            return
        await state.update_data(edit_caption_video=caption)
        await message.answer_video(video=video,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текс',
        reply_markup=edit_post_video(),
        parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте текс')
        return

@router.message(deafult_post.edit_photo)
async def edit_photo(message:Message,state:FSMContext):
    try:
        data = await state.get_data()
        if data.get('caption') is None:
            caption = ''
        elif data.get('edit_caption') is None:
            caption = data['caption']
        else:
            caption = data['edit_caption']
        photo = message.photo[-1].file_id
        await state.update_data(edit_photo=photo)
        await message.answer_photo(photo=photo,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текс?',
            reply_markup=edit_post_photo(),
            parse_mode='HTML')
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте фото')
        return

@router.message(deafult_post.edit_music)
async def edit_audio(message:Message,state:FSMContext):
    try:
        data = await state.get_data()
        if data.get('caption_music') is None:
            caption = ''
        elif data.get('edit_caption_music') is None:
            caption = data['caption_music']
        else:
            caption = data['edit_caption_music']
        audio = message.audio.file_id
        await state.update_data(edit_music=audio)
        await message.answer_audio(audio=audio,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить аудио или текс?',
        parse_mode='HTML',
        reply_markup=edit_post_audio()
        )
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте аудио')
        return

@router.message(deafult_post.edit_video)
async def edit_video(message:Message,state:FSMContext):
    try:
        data = await state.get_data()
        if data.get('caption_video') is None:
            caption = ''
        elif data.get('edit_caption_video') is None:
            caption = data['caption_video']
        else:
            caption = data['edit_caption_video']
        video = message.video.file_id
        await state.update_data(edit_video=video)
        await message.answer_photo(video=video,caption=f'<b>{caption}</b>\n\nХотите добавить URL кнопку к вашей публикации,изменить фото или текс',
            reply_markup=edit_post_video(),
            parse_mode='HTML')    
    except Exception:
        await message.answer('❌Ошибка! Неправильный тип сообщения,пожалуйста отправьте видео')
        return

@router.message(deafult_post.time)   
async def set_timee(message:Message, state:FSMContext):
    try:
        string_time = message.text
        await state.update_data(time=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time01())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.time1)   
async def set_time1(message:Message, state:FSMContext):
    try:
        string_time = message.text
        await state.update_data(time1=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_photo())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.time2)   
async def set_time2(message:Message, state:FSMContext):
    try:
        string_time = message.text
        await state.update_data(time2=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_video())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return  
    
@router.message(deafult_post.time3)
async def set_time3(message: Message, state: FSMContext):
    try:
        string_time = message.text
        await state.update_data(time3=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_audio())
        await state.set_state(deafult_post.wating)    
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.edit_time0)
async def edit_time(message: Message, state: FSMContext):
    try:
        string_time = message.text
        await state.update_data(edit_time0=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
            parse_mode='HTML',
            reply_markup=edit_time01())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.edit_time1)
async def edit_time1(message: Message, state: FSMContext):
    try:
        string_time = message.text
        await state.update_data(edit_time1=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_photo())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.edit_time2)
async def edit_time2(message:Message, state: FSMContext):
    try:
        string_time = message.text
        await state.update_data(edit_time2=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_video())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(deafult_post.edit_time3)
async def edit_time_audio1(message: Message, state: FSMContext):
    try:
        string_time = message.text
        await state.update_data(edit_time3=string_time)
        await message.answer(f'Готово!\nЗапланированое время отправки <code>{string_time}</code>\nХотите изменить дату публикации?',
        parse_mode='HTML',
        reply_markup=edit_time_audio())
        await state.set_state(deafult_post.wating)
    except Exception:
        await message.answer('Некорректый ввод! введите время в формате 22:15')
        return
    
@router.message(Command('start'))
async def cmd_start(message: Message):
    await init_db()
    photo = FSInputFile('post_fly.png')
    await message.answer_photo(
        photo=photo,
        caption='Привет!\n' \
        'Я бот,который прокачает твои публикации в телеграм канале или беседе\n\n' 
        '<b>В чем моя особенность:</b>\n\n' 
        '• 🕓Планировка публикаций!\n' 
        'Отправляй посты когда захочешь,без ограничений\n' 
        'а если время необходимо <b>изменить</b>,то я обязательно тебе в этом помогу =)\n' 
        '• 📷Публикации с медиа-контентом!\n' 
        'Создавай посты с видео,фото и музыкой\n' 
        '• 🧱 Публикации с URL <b>кнопками</b>!\n' 
        'Прокачай пост специальной кнопкой с URL сылкой!' 
        'Настраивай её полностью под себя от названия до цвета\n\n' 
        '<b>В чём моё преимущество?</b>\n\n' 
        '🆓Весь функционал бота абсолютно <b>бесплатный!</b>\n' 
        'Никаких ограничений и никакой рекламы\n\n' 
        'Чтобы приступить к работе,выбери интересующий раздел кнопками ниже⬇⬇⬇',
        reply_markup=reply_menu(),
        parse_mode='HTML'
    )

@router.message(Command('link_bot'))
async def cmd1(message: Message):
    await link_bot(message=message)

@router.message(Command('new_post'))
async def cmd2(message: Message):
    await new_post(message=message,
                   user_id=message.from_user.id)

@router.message(Command('support'))
async def cmd3(message: Message):
    await support(message=message)

@router.message(F.text == '🔗Привязка бота')
async def link_bot(message: Message):
    await message.answer(
        text='Чтобы привязать бота к каналу или группе,выполните несколько необходимых условиий:\n' \
        '<code>1</code>.Выберите место для привязки - телеграм канал или группа,нажав на одну из кнопок ниже\n' \
        '<code>2</code>.Выдайте боту право на публикацию сообщений.\nБез него бот не сможет публиковать посты и сообщения\n\n' \
        'После этого бот автоматически пришлет сообщение о привязке и его функционал станет доступным',
        parse_mode='HTML',
        reply_markup=link_the_bot()
    )

@router.message(F.text == '📃Новый пост')
async def proces_post(message:Message):
    await new_post(message=message,
                   user_id=message.from_user.id)

@router.message(F.text == '🛠Тех.поддержка')
async def support(message: Message):
    await message.answer('Если у вас возникла проблема,вы можете обратиться в поддержку,задав свой вопрос разработчику.\n\n@Yasked\n\n'
    '❕Убедительная просьба писать только по делу\nОжидайте ответ в течении суток☺')

@router.callback_query(F.data.startswith("ch:"))
async def channel_chosen(callback: types.CallbackQuery, state: FSMContext):
    chanel_id = int(callback.data.split(':')[1])
    data = await state.get_data()

    if data.get('chat_id') is None:
        await state.update_data(chat_id=chanel_id)
    else:
        await state.update_data(chat_id2=chanel_id)
    photo = FSInputFile('post_format.png')
    await callback.message.answer_photo(photo=photo,caption='Теперь выбери формат публикации:\n' 
        '• <b>Стандартный</b>\n' 
        '• <b>С фото</b>\n'
        '• <b>С видео</b>\n' 
        '• <b>С аудио</b>',
        parse_mode='HTML',
        reply_markup=post_format()
        )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

@router.callback_query()
async def callback(callback: types.CallbackQuery,state: FSMContext):
    data =callback.data

    if data == 'add_more':
        await link_bot(callback.message)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'new_publish':
        await new_post(message=callback.message,
                       user_id=callback.from_user.id)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)    

    if data == 'check_subscribe':
        function = await sub_ver(
            bot=callback.bot,
            user_id=callback.from_user.id
        )
        if not function:
            await callback.answer(
                text='❌Вы всё ещё не подписаны',
                show_alert=True
            )
            return
        await callback.message.answer('✅Успешно')
        await cmd_start(message=callback.message)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'deafult_post':
        asyncio.create_task(
            deafult_post1(
                message=callback.message,
                state=state
            )
        )
        await state.update_data(post_format='deafult')
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
        
    if data =='post_with_photo':
        await post_wiht_photo(callback.message,state)
        await callback.answer()
        await state.update_data(post_format='photo')
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'post_with_video':
        await post_with_video(
            message=callback.message,
            state=state
        )
        await state.update_data(post_format='video')
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
    
    if data == 'post_with_audio':
        await post_with_audio(
            callback.message,
            state
        )
        await state.update_data(post_format='audio')
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data =='caption_photo':
        await callback.message.answer('Хорошо,отправь мне желаемую подпись к фото')
        await state.set_state(deafult_post.caption)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='caption_audio':
        await callback.message.answer('Хорошо,отправь мне желаемую подпись к аудио')
        await state.set_state(deafult_post.caption_music)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'caption_video':
        await callback.message.answer('Хорошо,отправь мне желаемую подпись к видео')
        await state.set_state(deafult_post.caption_video)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
        
    if data == 'url_button_photo':
        await callback.message.answer('Отлично =)\nВведите название вашей кнопки')
        await state.set_state(deafult_post.button_title1)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'url_button_audio':
        await callback.message.answer('Отлично =)\nВведите название вашей кнопки')
        await state.set_state(deafult_post.button_title3)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
    
    if data == 'url_button_video':
        await callback.message.answer('Отлично =)\nВведите название вашей кнопки')
        await state.set_state(deafult_post.button_title2)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
    if data == 'url_button':
        await callback.message.answer('Отлично =)\nВведите название вашей кнопки')
        await state.set_state(deafult_post.button_title)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'red4':
        await state.update_data(button_colour3='danger')
        data = await state.get_data()
        if data.get('caption_music') is None:
            await state.update_data(caption_music=None)
        await show_post_with_audio(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
            
    if data == 'green4':
        await state.update_data(button_colour3='success')
        data = await state.get_data()
        if data.get('caption_music') is None:
            await state.update_data(caption_music=None)
        await show_post_with_audio(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'blue4':
        await state.update_data(button_colour3='primary')
        data = await state.get_data()
        if data.get('caption_music') is None:
            await state.update_data(caption_music=None)
        await show_post_with_audio(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()       

    if data == 'no_colour4':
        await state.update_data(button_colour3=None)
        data = await state.get_data()
        if data.get('caption_music') is None:
            await state.update_data(caption_music=None)
        await show_post_with_audio(callback.message,state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'red2':
        await state.update_data(button_colour2='danger')
        data = await state.get_data()
        if data.get('caption_video') is None:
            await state.update_data(caption_video=None)
        await show_post_with_video(message=callback.message,state=state)
        await callback.answer()
        
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()
    
    if data == 'green2':
        await state.update_data(button_colour2='success')
        data = await state.get_data()
        if data.get('caption_video') is None:
            await state.update_data(caption_video=None)
        await show_post_with_video(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'blue2':
        await state.update_data(button_colour2='primary')
        data = await state.get_data()
        if data.get('caption_video') is None:
            await state.update_data(caption_video=None)
        await callback.answer()
        await show_post_with_video(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'no_colour2':
        await state.update_data(button_colour2=None)
        data = await state.get_data()
        if data.get('caption_video') is None:
            await state.update_data(caption_video=None)
        await show_post_with_video(callback.message,state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='red1':
        await state.update_data(button_colour1='danger')
        data = await state.get_data()
        if data.get('caption') is None:
            await state.update_data(caption=None)
        await shot_post_with_photo(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='blue1':
        await state.update_data(button_colour1='primary')
        data = await state.get_data()
        if data.get('caption') is None:
            await state.update_data(caption=None)
        await shot_post_with_photo(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='green1':
        await state.update_data(button_colour1='success')
        data = await state.get_data()
        if data.get('caption') is None:
            await state.update_data(caption=None)
        await shot_post_with_photo(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data=='no_colour1':
        await state.update_data(button_colour1=None)
        data = await state.get_data()
        if data.get('caption') is None:
            await state.update_data(caption=None)
        await shot_post_with_photo(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='red':
        await state.update_data(button_colour='danger')
        await show_post(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data=='blue':
        await state.update_data(button_colour='primary')
        await show_post(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data=='green':
        await state.update_data(button_colour='success')
        await show_post(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='no_colour':
        await state.update_data(button_colour=None)
        await show_post(message=callback.message,state=state)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='edit_text':
        await callback.message.answer('Введите новый текст')
        await state.set_state(deafult_post.edit_text)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='edit_caption':
        await callback.message.answer('Введите новую подпись к вашему фото')
        await state.set_state(deafult_post.edit_caption)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'change_caption':
        await callback.message.answer('Введите новую подпись к вашему аудио')
        await state.set_state(deafult_post.edit_caption_music)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None) 
        
    if data == 'edit_caption2':
        await callback.message.answer('Введите новую подпись к вашему видео')
        await state.set_state(deafult_post.edit_caption_video)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None) 

    if data =='edit_photo':
        await callback.message.answer('Хорошо.Отправь мне новое фото для твоей публикации')
        await state.set_state(deafult_post.edit_photo)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'edit_video':
        await callback.message.answer('Хорошо.Отправь мне новое видео для твоей публикации')
        await state.set_state(deafult_post.edit_video)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'changed_audio':
        await callback.message.answer('Хорошо.Отправь мне новое аудио для твоей публикации')
        await state.set_state(deafult_post.edit_music)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data =='today':
        await callback.message.answer('Хорошо,сначала определимся с датой публикации\n'
            'Выберите её,нажав на одну из кнопок ниже⬇',
            reply_markup=date_keyboard())
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='today1':
        await callback.message.answer('Хорошо,сначала определимся с датой публикации\n'
            'Выберите её,нажав на одну из кнопок ниже⬇',
            reply_markup=date_keyboard())
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
    if data == 'today2':
        await callback.message.answer('Хорошо,сначала определимся с датой публикации\n'
            'Выберите её,нажав на одну из кнопок ниже⬇',
            reply_markup=date_keyboard())
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'today3':
        await callback.message.answer('Хорошо,сначала определимся с датой публикации\n'
            'Выберите её,нажав на одну из кнопок ниже⬇',
            reply_markup=date_keyboard())
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)        

    if data == 'continue_time':
        asyncio.create_task(
            time_publish(message=callback.message,state=state)
        )
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'continue_time1':
        asyncio.create_task(
            time_publish1(message=callback.message,state=state)
    )
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
    if data == 'continue_time2':
        asyncio.create_task(
            time_publish2(message=callback.message,state=state)
            )
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'continue_time3':
        asyncio.create_task(
        time_publish3(message=callback.message,state=state)
        )
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)   
    
    if data == 'edit_time':
        await callback.message.answer('Введите новое время отправки поста')
        await state.set_state(deafult_post.edit_time0)
        await callback.answer()

    if data == 'edit_time1':
        await callback.message.answer('Введите новое время отправки поста')
        await state.set_state(deafult_post.edit_time1)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
    if data == 'edit_time2':
        await callback.message.answer('Введите новое время отправки поста')
        await state.set_state(deafult_post.edit_time2)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'edit_time3':
        await callback.message.answer('Введите новое время отправки поста')
        await state.set_state(deafult_post.edit_time3)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data =='continue_photo':
        await callback.message.answer('Финальный шаг - определимся со временем публикации ⬇',
            reply_markup=button_today1())
        data = await state.get_data()
        if data.get('caption') is None:
            await state.update_data(caption='')
        await state.update_data(button_title1=None)
        await state.update_data(button_url1=None)
        await state.update_data(button_colour1=None)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
    if data == 'continue_video':
        await callback.message.answer('Финальный шаг - определимся со временем публикации ⬇',
            reply_markup=button_today2())
        data = await state.get_data()
        if data.get('caption_video') is None:
            await state.update_data(caption_video='')
        await state.update_data(button_title2=None)
        await state.update_data(button_url2=None)
        await state.update_data(button_colour2=None)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'continue_audio':
        await callback.message.answer('Финальный шаг - определимся со временем публикации ⬇',
            reply_markup=button_today3())
        data = await state.get_data()
        if data.get('caption_music') is None:
            await state.update_data(caption_music='')
        await state.update_data(button_title3=None)
        await state.update_data(button_url3=None)
        await state.update_data(button_colour3=None)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)        

    if data == 'continue':
        await callback.message.answer('Финальный шаг - определимся со временем публикации ⬇',
        reply_markup=button_today())
        await state.update_data(button_title=None)
        await state.update_data(button_url=None)
        await state.update_data(button_colour=None)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'publish_now':
        asyncio.create_task(time_publish(
            message=callback.message,
            state=state
        )
        )
        await state.update_data(time=None)
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'publish_now1':
        asyncio.create_task(time_publish1(
        message=callback.message,
        state=state))
        await state.update_data(time1=None)
        await callback.answer() 
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'publish_now2':
        asyncio.create_task(time_publish2(
            message=callback.message,
            state=state))
        await state.update_data(time2=None)
        await callback.answer() 
        await callback.message.edit_reply_markup(reply_markup=None)

    if data == 'publish_now3':
        asyncio.create_task(time_publish3(
            callback.message,
            state
        ))
        await state.update_data(time3=None)
        await callback.answer() 
        await callback.message.edit_reply_markup(reply_markup=None)    

    if data == 'next':
        await callback.message.edit_reply_markup(reply_markup=data_keyboard1())
        await callback.answer()

    if data == 'back':
        await callback.message.edit_reply_markup(reply_markup=date_keyboard())
        await callback.answer()

    if data == 'next1':
        await callback.message.edit_reply_markup(reply_markup=data_keyboard2())
        await callback.answer()

    if data == 'back1':
        await callback.message.edit_reply_markup(reply_markup=data_keyboard1())
        await callback.answer()

    if data in [str(i) for i in range(1, 32)]: # как это работает(range создаёт числа от 1 до 31) если callback.data попадает в этот список - условие срабатывает
        await state.update_data(number = callback.data)
        phormat = await state.get_value('post_format')
        await callback.message.answer('Теперь определимся со временем публикации\nУкажите его в формате "<code>10:27</code>"\nВ противом случае пост опубликуется сразу',parse_mode='HTML')
        if phormat == 'deafult':
            await state.set_state(deafult_post.time)
        elif phormat == 'photo':
            await state.set_state(deafult_post.time1)
        elif phormat == 'video':
            await state.set_state(deafult_post.time2)
        elif phormat == 'audio':
            await state.set_state(deafult_post.time3)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()   

    if data == 'no_data':
        await callback.message.answer('Теперь определимся со временем публикации\nУкажите его в формате "<code>10:27</code>"\nВ противом случае пост опубликуется сразу',parse_mode='HTML')
        phormat = await state.get_value('post_format')
        print(phormat)
        if phormat == 'deafult':
            await state.set_state(deafult_post.time)
        elif phormat == 'photo':
            await state.set_state(deafult_post.time1)
        elif phormat == 'video':
            await state.set_state(deafult_post.time2)
        elif phormat == 'audio':
            await state.set_state(deafult_post.time3)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data == 'post_post':
        await new_post(
            message=callback.message,
            user_id=callback.from_user.id
        )
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer()

    if data =='del':
        await state.set_state(deafult_post.wating)
        phormat = await state.get_value('post_format')
        if phormat == 'deafult':
            await state.update_data(text=None)
            await state.update_data(button_title=None)
            await state.update_data(button_url=None)
            await state.update_data(button_colour=None)
        if phormat == 'photo':
            await state.update_data(photo=None)
            await state.update_data(caption=None)
            await state.update_data(button_title1=None)
            await state.update_data(button_url1=None)
            await state.update_data(button_colour1=None)  
        if phormat == 'video':
            await state.update_data(video=None)
            await state.update_data(caption_video=None)
            await state.update_data(button_title2=None)
            await state.update_data(button_url2=None)
            await state.update_data(button_colour2=None)              
        if phormat == 'audio':
            await state.update_data(music=None)
            await state.update_data(caption_music=None)
            await state.update_data(button_title3=None)
            await state.update_data(button_url3=None)
            await state.update_data(button_colour3=None)                        

        await callback.message.edit_text(text='✅Пост успешно удалён')
        await callback.message.edit_reply_markup(reply_markup=new_post100())
        data = await state.get_data()
        print(f'in data{data}')
        await callback.answer()

@router.my_chat_member()
async def bot_status_changed(
    event : ChatMemberUpdated,
    bot : Bot
):
    if event.chat.type not in ('channel', 'supergroup'):
        return
    
    new_status = event.new_chat_member.status
    print(
    "STATUS:",
    new_status,
    "CHAT:",
    event.chat.title,
    "TYPE:",
    event.chat.type)
    if new_status =='administrator':

        permissions = event.new_chat_member

        can_post = permissions.can_post_messages

        chanel_name = event.chat.title

        chanel_id = event.chat.id
        name = event.chat.title
        user_name = event.from_user.id

        if can_post:
            await add_id(user_id=user_name,
                         id=chanel_id,
                         name_chanel=name)
            await bot.send_message(
                text=f'✅Бот добавлен в канал <b>{chanel_name}</b>!\n'
                'Теперь вы можете начать делать любые публикации на свой вкус!\n' 
                'В случае ошибки обратитесь в тех поддержку,нажав на кнопку вызова в меню\n' 
                'Приятного использования =)',
                parse_mode='HTML',
                chat_id=event.from_user.id,
                reply_markup=link_the_more()
            )
        else:
            await bot.send_message(
                text=f'⚠Бот добавлен в канал <b>{chanel_name}</b>,но у него <b>нет прав</b> на публикацию сообщений!\n'
                'Пожалуйста добавьте бота в канал или группу,кнопками ниже\n' 
                'В случае ошибки обратитесь в тех поддержку,нажав на кнопку вызова в меню',
                reply_markup=link_the_bot(),
                parse_mode='HTML',
                chat_id=event.from_user.id 
            )
    elif new_status == 'kicked':
        print('eeeee!')
        chanel_name = event.chat.title
        chanel_id = event.chat.id
        function = await get_user_id(channel_id=chanel_id)
        await delete_id(
            channel_id=chanel_id,
            name_chanel=chanel_name)
        await bot.send_message(
            text=f'⚠Бот был исключён из канала <b>{chanel_name}</b>!\n'
            'В случае ошибки обратитесь в тех поддержку,нажав на кнопку вызова в меню\n' \
            'Вы можете повторно подключить бота,нажав на кнопку ниже⬇',
            chat_id=function,
            parse_mode='HTML',
            reply_markup=link_the_bot())
    elif new_status == 'left':
        print('eeeee!')
        chanel_name = event.chat.title
        chanel_id = event.chat.id
        function = await get_user_id(channel_id=chanel_id)
        await delete_id(
            channel_id=chanel_id,
            name_chanel=chanel_name)
        await bot.send_message(
            text=f'⚠Бот был исключён из канала <b>{chanel_name}</b>!\n'
            'В случае ошибки обратитесь в тех поддержку,нажав на кнопку вызова в меню\n' \
            'Вы можете повторно подключить бота,нажав на кнопку ниже⬇',
            chat_id=function,
            parse_mode='HTML',
            reply_markup=link_the_bot()
)

@router.message()
async def spam(message: Message):
    await message.answer(
        text='⚠Бот вас не понял!\n' \
        'Открыл меню ниже,выберите интересующий вас раздел⬇',
        reply_markup=reply_menu()
    )

async def show_post(message: Message, state:FSMContext):

    data = await state.get_data()
    if data.get('edit_text') is None:
        text = data['text']
    else:
        text = data['edit_text']
   
    button_title = data['button_title']

    button_url = data['button_url']
   
    button_colour = data['button_colour']

    builder = InlineKeyboardBuilder()

    builder.button(
        text=button_title,
        url=button_url,
        style=button_colour
    )

    builder.adjust(1)

    await message.answer(
        text,
        reply_markup=builder.as_markup()
    )
    await message.answer('Вот,что получилось!\n' 
    'Финальный шаг - определимся со временем публикации ⬇',
    reply_markup=button_today())

async def shot_post_with_photo(message: Message,state: FSMContext):
    data = await state.get_data()
    if data.get('edit_photo') is None:
        photo = data['photo']
    else: 
        photo = data['edit_photo']
    if data.get('edit_caption') is None:
        caption = data['caption']
    else:
        caption = data['edit_caption']

    button_title = data['button_title1']
    
    button_url = data['button_url1']
       
    button_colour = data['button_colour1']
    
    builder = InlineKeyboardBuilder()
    
    builder.button(
            text=button_title,
            url=button_url,
            style=button_colour
    )
    builder.adjust(1)

    await message.answer_photo(photo=photo,caption=caption,reply_markup=builder.as_markup())
    await message.answer('Вот,что получилось!\n' 
    'Финальный шаг - определимся со временем публикации ⬇',
    reply_markup=button_today1())

async def show_post_with_video(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('edit_video') is None:
        video = data['video']
    else: 
        video = data['edit_video']
    if data.get('edit_caption_video') is None:
        caption = data['caption_video']
    else:
        caption = data['edit_caption_video']
    
    button_title = data['button_title2']
        
    button_url = data['button_url2']
           
    button_colour = data['button_colour2']
        
    builder = InlineKeyboardBuilder()
        
    builder.button(
        text=button_title,
        url=button_url,
        style=button_colour
    )
    builder.adjust(1)
        
    await message.answer_video(video=video,caption=caption,reply_markup=builder.as_markup())
    await message.answer('Вот,что получилось!\n' 
    'Финальный шаг - определимся со временем публикации ⬇',
    reply_markup=button_today2())

async def show_post_with_audio(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('edit_music') is None:
        audio = data['music']
    else: 
        audio = data['edit_music']
    if data.get('edit_caption_music') is None:
        caption = data['caption_music']
    else:
        caption = data['edit_caption_music']
    
    button_title = data['button_title3']
        
    button_url = data['button_url3']
           
    button_colour = data['button_colour3']
        
    builder = InlineKeyboardBuilder()
        
    builder.button(
        text=button_title,
        url=button_url,
        style=button_colour
    )
    builder.adjust(1)
        
    await message.answer_audio(audio=audio,caption=caption,reply_markup=builder.as_markup())
    await message.answer('Вот,что получилось!\n' 
    'Финальный шаг - определимся со временем публикации ⬇',
    reply_markup=button_today3())
    
async def time_publish(message: types.Message, state: FSMContext):
    
    data = await state.get_data()

    if data.get('edit_time0') is None:
        time_publish = data['time']
    else:
        time_publish = data['edit_time0']
    
    if data.get('edit_text') is None:
        text = data['text']
    else:
        text = data['edit_text']

    if data.get('chat_id2') is None:
        chat_id = data['chat_id']
    else:
        chat_id = data['chat_id2']

    button_title = data.get('button_title')
    button_url = data.get('button_url')
    button_colour = data.get('button_colour')

    try:
        now = datetime.now()
        number = data.get('number', now.day)
        # День, который выбрал пользователь
        day = int(number)

        # Время, которое ввёл пользователь
        target_time = datetime.strptime(time_publish, "%H:%M").time()

        # Создаём дату с выбранным днём
        target_datetime = datetime(
            year=now.year,
            month=now.month,
            day=day,
            hour=target_time.hour,
            minute=target_time.minute
        )

        # Если эта дата уже прошла — переносим на следующий месяц
        if target_datetime <= now:
            if now.month == 12:
                target_datetime = target_datetime.replace(
                    year=now.year + 1,
                    month=1
                )
            else:
                target_datetime = target_datetime.replace(
                    month=now.month + 1
                )

        # Сколько секунд осталось
        seconds = (target_datetime - now).total_seconds()

        print("Сейчас:", now)
        print("время публикации:", target_datetime)
        print("Ждать секунд:", seconds)

        await asyncio.sleep(seconds)

    except Exception as e:
        print(e)
        await asyncio.sleep(0)

    await deafult_publish(
        bot=message.bot,
        text=text,
        chanel_id=chat_id,
        button_title=button_title,
        button_url=button_url,
        button_colour=button_colour
    )

    await message.answer(
        f"Готово! Пост:\n\n<b>{text}</b>\n\nОпубликован",
        parse_mode="HTML",
        reply_markup=new_post100()
    )

    await state.clear()

async def time_publish1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('chat_id2') is None:
            chat_id = data['chat_id']
    else:
        chat_id = data['chat_id2']

    if data.get('edit_time1') is None:
            time_publish = data['time1']
    else:
        time_publish = data['edit_time0']

    if data.get('edit_photo') is None:
        photo = data['photo']
    else: 
        photo = data['edit_photo']

    if data.get('edit_caption') is None:
        caption = data['caption']
    else:
        caption = data['edit_caption']
    
    button_title = data['button_title1']
        
    button_url = data['button_url1']
           
    button_colour = data['button_colour1']
        
    try:
        now = datetime.now()
        number = data.get('number', now.day)
        # День, который выбрал пользователь
        day = int(number)

        # Время, которое ввёл пользователь
        target_time = datetime.strptime(time_publish, "%H:%M").time()

        # Создаём дату с выбранным днём
        target_datetime = datetime(
            year=now.year,
            month=now.month,
            day=day,
            hour=target_time.hour,
            minute=target_time.minute
        )

        # Если эта дата уже прошла — переносим на следующий месяц
        if target_datetime <= now:
            if now.month == 12:
                target_datetime = target_datetime.replace(
                    year=now.year + 1,
                    month=1
                )
            else:
                target_datetime = target_datetime.replace(
                    month=now.month + 1
                )

        # Сколько секунд осталось
        seconds = (target_datetime - now).total_seconds()

        print("Сейчас:", now)
        print("время публикации:", target_datetime)
        print("Ждать секунд:", seconds)

        await asyncio.sleep(seconds)

    except Exception as e:
        print(e)
        await asyncio.sleep(0)

    await post_with_photo(
        bot=message.bot,
        chanel_id=chat_id,
        photo=photo,
        caption=caption,
        button_title=button_title,
        button_url=button_url,
        button_colour=button_colour
    )
    await message.answer(f"Готово! Пост:\n\n<b>{caption}</b>\n\n Опубликован",
        parse_mode="HTML",
        reply_markup=new_post100())
    await state.clear()

async def time_publish2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('chat_id2') is None:
            chat_id = data['chat_id']
    else:
        chat_id = data['chat_id2']

    if data.get('edit_video') is None:
        video = data['video']
    else: 
        video = data['edit_video']

    if data.get('edit_caption_video') is None:
        caption = data['caption_video']
    else:
        caption = data['edit_caption_video']
    
    button_title = data['button_title2']
        
    button_url = data['button_url2']
           
    button_colour = data['button_colour2']
        

    if data.get('edit_time2') is None:
        time_publish = data['time2']
    else:
        time_publish = data['edit_time2']
    try:
        now = datetime.now()
        number = data.get('number', now.day)
        # День, который выбрал пользователь
        day = int(number)

        # Время, которое ввёл пользователь
        target_time = datetime.strptime(time_publish, "%H:%M").time()

        # Создаём дату с выбранным днём
        target_datetime = datetime(
            year=now.year,
            month=now.month,
            day=day,
            hour=target_time.hour,
            minute=target_time.minute
        )

        # Если эта дата уже прошла — переносим на следующий месяц
        if target_datetime <= now:
            if now.month == 12:
                target_datetime = target_datetime.replace(
                    year=now.year + 1,
                    month=1
                )
            else:
                target_datetime = target_datetime.replace(
                    month=now.month + 1
                )

        # Сколько секунд осталось
        seconds = (target_datetime - now).total_seconds()

        print("Сейчас:", now)
        print("время публикации:", target_datetime)
        print("Ждать секунд:", seconds)

        await asyncio.sleep(seconds)

    except Exception as e:
        print(e)
        await asyncio.sleep(0)

    await post_with_video1(
        bot=message.bot,
        chanel_id=chat_id,
        video=video,
        caption=caption,
        button_title=button_title,
        button_url=button_url,
        button_colour=button_colour
    )
    await message.answer(f"Готово! Пост:\n\n<b>{caption}</b>\n\n Опубликован",
        parse_mode="HTML",reply_markup=new_post100())
    await state.clear()

async def time_publish3(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('chat_id2') is None:
        chat_id = data['chat_id']
    else:
        chat_id = data['chat_id2']


    if data.get('edit_music') is None:
        music = data['music']
    else: 
        music = data['edit_music']

    if data.get('edit_caption_music') is None:
        caption = data['caption_music']
    else:
        caption = data['edit_caption_music']
    
    button_title = data['button_title3']
        
    button_url = data['button_url3']
           
    button_colour = data['button_colour3']
        

    if data.get('edit_time3') is None:
        time_publish = data['time3']
    else:
        time_publish = data['edit_time3']
    try:
        now = datetime.now()
        number = data.get('number', now.day)
        # День, который выбрал пользователь
        day = int(number)

        # Время, которое ввёл пользователь
        target_time = datetime.strptime(time_publish, "%H:%M").time()

        # Создаём дату с выбранным днём
        target_datetime = datetime(
            year=now.year,
            month=now.month,
            day=day,
            hour=target_time.hour,
            minute=target_time.minute
        )

        # Если эта дата уже прошла — переносим на следующий месяц
        if target_datetime <= now:
            if now.month == 12:
                target_datetime = target_datetime.replace(
                    year=now.year + 1,
                    month=1
                )
            else:
                target_datetime = target_datetime.replace(
                    month=now.month + 1
                )

        # Сколько секунд осталось
        seconds = (target_datetime - now).total_seconds()

        print("Сейчас:", now)
        print("время публикации:", target_datetime)
        print("Ждать секунд:", seconds)

        await asyncio.sleep(seconds)

    except Exception:
        await asyncio.sleep(0)

    await post_with_audio1(
        bot=message.bot,
        chanel_id=chat_id,
        audio=music,
        caption=caption,
        button_colour=button_colour,
        button_title=button_title,
        button_url=button_url
    )
    await message.answer(f"Готово! Пост:\n\n<b>{caption}</b>\n\n Опубликован",
        parse_mode="HTML",
        reply_markup=new_post100())
    await state.clear()