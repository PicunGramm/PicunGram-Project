from telethon import events
import os
import speech_recognition as sr
from pydub import AudioSegment
import asyncio

async def setup(client):
    @client.on(events.NewMessage(pattern=r'\.аудио'))
    async def audio_handler(event):
        # Проверяем, что команда от меня
        if event.sender_id != (await client.get_me()).id:
            return

        # Удаляем сообщение с командой
        try:
            await event.delete()
        except:
            pass

        # Проверяем reply
        if not event.is_reply:
            status_msg = await event.reply("🚫 Ответьте `.аудио` на голосовое/кружок")
            await asyncio.sleep(3)
            await status_msg.delete()
            return

        reply_msg = await event.get_reply_message()
        
        # Проверка типа сообщения
        if not (reply_msg.voice or reply_msg.video_note):
            status_msg = await event.reply("❌ Это не голосовое и не кружок!")
            await asyncio.sleep(3)
            await status_msg.delete()
            return

        # Отправляем статус обработки
        processing_msg = await event.reply("🔍 Обрабатываю аудио...")

        try:
            # Скачивание
            file_path = await reply_msg.download_media()
            await processing_msg.edit("🔧 Конвертирую в WAV...")
            
            # Конвертация
            audio = AudioSegment.from_file(file_path)
            wav_path = "temp_audio.wav"
            audio.export(wav_path, format="wav")
            
            # Распознавание
            await processing_msg.edit("🎤 Распознаю речь...")
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="ru-RU")
            
            # Результат
            await processing_msg.delete()
            result_msg = await event.reply(f"🔊 Результат:\n`{text}`")
            
        except sr.UnknownValueError:
            await processing_msg.edit("❌ Речь не распознана")
            await asyncio.sleep(3)
            await processing_msg.delete()
        except Exception as e:
            await processing_msg.edit(f"⚠️ Ошибка: {str(e)}")
            await asyncio.sleep(5)
            await processing_msg.delete()
        finally:
            # Удаляем временные файлы
            for path in [file_path, wav_path]:
                if path and os.path.exists(path):
                    os.remove(path)
print("Модуль запущен!(.аудио)")