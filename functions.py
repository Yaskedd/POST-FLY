from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

chanel_user_name = '@post_publishhh'

async def sub_ver(
        bot: Bot,
        user_id: int
) -> bool:
    member = await bot.get_chat_member(
        chat_id=chanel_user_name,
        user_id=user_id
    )
    return member.status in(
        "creator",
        "administrator",
        "member"
    )

async def deafult_publish(
        bot: Bot,
        chanel_id: int,
        text: str,
        button_title,
        button_url,
        button_colour
):  
    builder = InlineKeyboardBuilder()
    if button_title and button_url:
        builder.button(text=button_title,url=button_url,style=button_colour)
        builder.adjust(1)

    await bot.send_message(
        chat_id=chanel_id,
        text=text,
        reply_markup=builder.as_markup()
    )

async def post_with_photo(
        bot: Bot,
        chanel_id: int,
        photo,
        caption,
        button_title,
        button_url,
        button_colour
):  
    builder = InlineKeyboardBuilder()
    if button_title and button_url:
        builder.button(text=button_title,url=button_url,style=button_colour)
        builder.adjust(1)
    await bot.send_photo(
        chat_id=chanel_id,
        photo=photo,
        caption=caption,
        reply_markup=builder.as_markup()
    )

async def post_with_video1(
        bot: Bot,
        chanel_id : int,
        video,
        caption,
        button_title,
                button_url,
                button_colour
):  
    builder = InlineKeyboardBuilder()
    if button_title and button_url:
        builder.button(text=button_title,url=button_url,style=button_colour)
        builder.adjust(1)
    await bot.send_video(
    chat_id=chanel_id,
    video=video,
    caption=caption,
    reply_markup=builder.as_markup()
            )

async def post_with_audio1(
        bot: Bot,
        chanel_id : int,
        audio,
        caption,
        button_title,
        button_url,
        button_colour
):
    builder = InlineKeyboardBuilder()
    if button_title and button_url:
        builder.button(text=button_title,url=button_url,style=button_colour)
        builder.adjust(1)
    await bot.send_audio(
        chat_id=chanel_id,
        audio=audio,
        caption=caption,
        reply_markup=builder.as_markup()
    )