import vkquick as vq

from title_changer.tortoise_models import Chat
from title_changer.misc import load_settings, b2s, value_or_default


SETTINGS = load_settings()

app = vq.Package()


def get_chat_text(chat: Chat) -> str:
    return (
        f"Изменение названия глобально: {b2s(chat.is_active)}\n"
        f"Изменение названия днем ({SETTINGS.day_change_time}): {b2s(chat.can_change(chat.ChangeType.DAY))}\n"
        f"Изменение названия ночью ({SETTINGS.nigth_change_time}): {b2s(chat.can_change(chat.ChangeType.NIGTH))}\n\n"

        F"Название чата на день ({SETTINGS.day_change_time}): {value_or_default(chat.day_name)}\n"
        F"Название чата на ночь ({SETTINGS.nigth_change_time}): {value_or_default(chat.nigth_name)}"
    )


@app.command('инфо', filter=vq.filters.ChatOnly())
async def show_chat_handler(ctx: vq.NewMessage):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)
    return get_chat_text(chat)

@app.command('чат активность', filter=vq.filters.ChatOnly())
async def toggle_chat_handler(ctx: vq.NewMessage, is_active: bool):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)

    chat.is_active = is_active
    await chat.save()
    return get_chat_text(chat)

@app.command('чат имя день', filter=vq.filters.ChatOnly())
async def set_chat_name(ctx: vq.NewMessage, *, text: str):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)
    chat.day_name = text
    await chat.save()
    return get_chat_text(chat)


@app.command('чат имя ночь', filter=vq.filters.ChatOnly())
async def set_chat_name(ctx: vq.NewMessage, *, text: str):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)
    chat.nigth_name = text
    await chat.save()
    return get_chat_text(chat)


@app.command('-чат имя день', filter=vq.filters.ChatOnly())
async def set_chat_name(ctx: vq.NewMessage):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)
    chat.day_name = None
    await chat.save()
    return get_chat_text(chat)


@app.command('-чат имя ночь', filter=vq.filters.ChatOnly())
async def set_chat_name(ctx: vq.NewMessage):
    chat, _ = await Chat.get_or_create(id=ctx.msg.peer_id)
    chat.nigth_name = None
    await chat.save()
    return get_chat_text(chat)