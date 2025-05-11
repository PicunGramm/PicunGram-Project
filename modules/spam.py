from telethon.sync import TelegramClient, events
import time
import re

stop_spam_flag = False

async def setup(client):
    @client.on(events.NewMessage(pattern=r'\.spam\s+(\d+)\s+(.+)?'))
    async def spam_handler(event):
        if event.sender_id != (await client.get_me()).id:
            return
        global stop_spam_flag

        try:
            await event.delete()
        except Exception as del_err:
            print("Не удалось удалить сообщение!")

        match = re.match(r'\.spam\s+(\d+)\s+(.+)', event.text)
        if not match:
            msg = await event.reply("⚠️Неправильный формат⚠️ ✅Используйте: `.spam <кол-во> <текст>`✅")
            time.sleep(3)
            await msg.delete()
            return
    
        count = int(match.group(1))
        text = match.group(2)

        if count > 500:
            msg = await event.reply("‼️Максисмум 500 сообщений за раз‼️")
            time.sleep(3)
            await msg.delete()
            return
    
        stop_spam_flag = False
        sent = 0

        for i in range(count):
            if stop_spam_flag:
                break
            try:
                await event.respond(text)
                sent += 1
                time.sleep(0.1)
            except Exception as e:
                print(f"Ошибка!: {e}")
                break
    
        result_msg = await event.reply(f"🟢Отправлено {sent}/{count} сообщений!🟢")
        time.sleep(3)
        await result_msg.delete()

    @client.on(events.NewMessage(pattern=r'\.stopspam'))
    async def spam_handler(event):
        if event.sender_id != (await client.get_me()).id:
            return

        try:
            await event.delete()
        except Exception as del_err:
            print("Не удалось удалить сообщение!")
        global stop_spam_flag
        stop_spam_flag = True
        error_msg = await event.reply("⛔Спам остновлен!⛔")
        time.sleep(3)
        await error_msg.delete()

    print("Модуль был запущен. Введите .spam <кол-во> <текст> для спама.")