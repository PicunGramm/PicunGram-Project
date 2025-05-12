from telethon import TelegramClient, events
from telethon.tl.functions import PingRequest
import time
import statistics

async def setup(client):
    @client.on(events.NewMessage(pattern=r'\.ping'))
    async def handler(event):
        if event.sender_id != (await client.get_me()).id:
            return
        try:
            await event.delete()
        except Exception as e:
            print(f"Error {e}")
        pings = []
        for _ in range(3):
            start_time = time.time()
            await client(PingRequest(ping_id=12345))
            pings.append((time.time() - start_time) * 1000)

        avg_ping = statistics.mean(pings)
        median_ping = statistics.median(pings)

        status = (
            "🚀Пиздец ты флеш нахуй!🚀" if avg_ping < 100 else
            "🔵Ну сойдет🔵" if avg_ping < 300 else
            "🐢АХАХХАХАХААХАХАХ НУ ТЫ И ЛОХ🐢"
        )

        result_msg = (
            f"🛜 **Реальный пинг до тг**\n\n"
            f"🛜 Средний: `{avg_ping:.2f} мс `\n"
            f"🛜 Медиана: `{median_ping:.2f} мс `\n"
            f"🛜 Статус : {status}" 
        )

        msg = await event.reply("**Измеряем реальный пинг до тг...**")
        time.sleep(5)
        await client.edit_message(event.chat_id, msg.id, result_msg)

    print("Модуль запущен!(.ping)")
