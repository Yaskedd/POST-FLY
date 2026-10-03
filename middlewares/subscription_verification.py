from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Callable, Dict
from functions import sub_ver
from buttons import subscribe_button

class is_subscribe(BaseMiddleware):
    async def __call__(
    self,
    handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
    event: Message,
    data: Dict[str, Any]
    ) -> Any:
        bot = data['bot']
        user_id = event.from_user.id
        function = await sub_ver(
            bot=bot,
            user_id=user_id
        )
        if not function:
            if isinstance(event, Message):
                await event.answer(
                    text='⚠Перед использованием бота необходимо подписаться на канал',
                    reply_markup=subscribe_button()
                )
            return

        return await handler(event, data)