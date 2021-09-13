import typing as ty
import vkquick as vq
from title_changer.tortoise_models import Chat
from title_changer.misc import load_settings
import asyncio


SETTINGS = load_settings()

async def sendler(api: vq.API, results: ty.Dict[int, str]):
    text = "Отчет об изменении названий чатов:\n\n"
    for chat_id, status in results.items():
        text += f"vk.com/im?sel=c{chat_id}\n{status}\n\n"
    
    await api.method(
        "messages.send",
        peer_id=SETTINGS.admin_id,
        random_id=0,
        message=text
    )

async def update_name_day(api: vq.API):
    results = {} 

    async for chat in Chat.filter(is_active=True):
        chat_id = chat.id - int(2e9)
        if not chat.can_change(Chat.ChangeType.DAY):
            results[chat_id] = "⚠ Чат пропущен, т.к. имя не установлено"
            continue
        
        try:
            await api.method("messages.editChat", chat_id=chat_id, title=chat.day_name)
            results[chat_id] = f"✅ Имя чата успешно изменена на <<{chat.day_name}>>"
        except Exception as ex:
            results[chat_id] = f"⚠ Ошибка: {ex.__class__.__name__} -> {ex}"
        finally:
            await asyncio.sleep(5)

    await sendler(api, results)

async def update_name_nigth(api: vq.API):
    results = {} 

    async for chat in Chat.filter(is_active=True):
        chat_id = chat.id - int(2e9)
        if not chat.can_change(Chat.ChangeType.NIGTH):
            results[chat_id] = "⚠ Чат пропущен, т.к. имя не установлено"
            continue
        
        try:
            await api.method("messages.editChat", chat_id=chat_id, title=chat.nigth_name)
            results[chat_id] = f"✅ Имя чата успешно изменено на <<{chat.nigth_name}>>"
        except Exception as ex:
            results[chat_id] = f"⚠ Ошибка: {ex.__class__.__name__} -> {ex}"
        finally:
            await asyncio.sleep(5)

    await sendler(api, results)