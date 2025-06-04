from telethon import TelegramClient, events

async def setup(client):
    @client.on(events.NewMessage(pattern=r'\.help'))
    async def handler(event):
        if event.sender_id != (await client.get_me()).id:
            return
        try:
            await event.delete()
        except Exception as e:
            print(f"Error {e}")
        
        msg = await event.reply("**Помощь:**\n__В начале везде точка__\n**spam** `<кол-во> <текст>`\n**doks**\n**секс**`(в ответ на сообщение)`\n**ping**\n**аудио**`(в ответ на гс\кружок)`\n**help**`(вызывает это меню)`")

    print("Модуль запущен!(.help)")
