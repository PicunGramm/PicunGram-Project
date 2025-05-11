from telethon.sync import TelegramClient
import asyncio
from importlib import import_module
import os

api_id = 26881961
api_hash = 'f3e8b6c96cbbb02eca435c60318ff338'
session_name = 'session_name'
modules_dir = 'modules'
number_file = 'number.txt'

def get_phone_numder():
    """Получает номер телефона: из файла или запрашивает у пользователя"""
    if os.path.exists(number_file):
        with open(number_file, 'r') as f:
            saved_phone = f.read().strip()
            if saved_phone:
                return saved_phone
    
    while True:
        try:
            phone = input("Введите номер телефона (в формате +79123456789): ").strip()
            if not phone.startswith('+'):
                print("Номер должен начинаться с '+'")
                continue
            if not phone[1:].isdigit():
                print("Номер должен содержать только цифры после '+'")
                continue
            if len(phone) < 12:
                print("Слишком короткий номер")
                continue

            with open(number_file, 'w') as f:
                f.write(phone)
            return phone
        except Exception as e:
            print(f"ОШИБКА: {e}. Попробуйте снова")

async def load_module(client, module_name):
    """Загружает и инициализирует модуль"""
    try:
        module = import_module(f'modules.{module_name}')
        if hasattr(module, 'setup'):
            await module.setup(client)
        else:
            print(f"В {module_name} нет функции setup()")
    except Exception as e:
        print(f"ОШИБКА!!! В {module_name}: {str(e)}")

async def main():
    phone = get_phone_numder()
    print(f"Используется номер: {phone}")
    
    client = TelegramClient('session', api_id, api_hash)

    try:
        await client.start(phone)
        print("Авторизация прошла успешно!!!")

        module_files = [
            f[:-3] for f in os.listdir(modules_dir)
            if f.endswith('.py') and not f.startswith('_')
        ]

        for module_name in module_files:
            await load_module(client, module_name)

        print("Бот запущен! Ожидание команд...")
        await client.run_until_disconnected()

    except Exception as e:
        print(f"ОШИБКА!!! : {str(e)}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())