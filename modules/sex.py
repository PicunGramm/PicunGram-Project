from telethon import events
import asyncio

async def setup(client):
    @client.on(events.NewMessage(pattern=r'\.секс'))
    async def handler(event):
        if event.sender_id != (await client.get_me()).id:
            return
        if not event.is_reply:
            await event.delete()
            return
        
        reply_msg = await event.get_reply_message()
        target = await reply_msg.get_sender()
        target_username = f"@{target.username}" if target.username else target.first_name

        try:
            await event.delete()
        except:
            pass

        await event.respond(f"{target_username} выебан")
        
    print("Модуль запущен!(.секс)")