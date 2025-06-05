from telethon.sync import TelegramClient
import asyncio
from importlib import import_module
import os
import time

api_id = 26881961
api_hash = 'f3e8b6c96cbbb02eca435c60318ff338'
session_name = 'session_name'
modules_dir = 'modules'
number_file = 'number.txt'

def clear_terminal():
    os.system('clear')

clear_terminal()

def get_phone_numder():
    """Получает номер телефона: из файла или запрашивает у пользователя"""
    if os.path.exists(number_file):
        with open(number_file, 'r') as f:
            saved_phone = f.read().strip()
            if saved_phone:
                return saved_phone
    
    while True:
        try:
            print("\033[32m██████╗ ██╗ ██████╗██╗   ██╗███╗   ██╗ ██████╗ ██████╗  █████╗ ███╗   ███╗\n██╔══██╗██║██╔════╝██║   ██║████╗  ██║██╔════╝ ██╔══██╗██╔══██╗████╗ ████║\n██████╔╝██║██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║██╔████╔██║\n██╔═══╝ ██║██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║\n██║     ██║╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║\n╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝\033[0m")
            phone = input("\033[33m╔══════════════════════════════════════════════════─\n║\n╚\033[0m \033[35mВведите номер телефона (в формате +79123456789):\033[0m ").strip()
            if not phone.startswith('+'):
                print("\033[35mНомер должен начинаться с '+'\033[0m")
                time.sleep(5)
                clear_terminal()
                continue
            if not phone[1:].isdigit():
                print("\033[35mНомер должен содержать только цифры после '+'\033[0m")
                time.sleep(5)
                clear_terminal()
                continue
            if len(phone) < 12:
                print("\033[35mСлишком короткий номер\033[0m")
                time.sleep(5)
                clear_terminal()
                continue

            with open(number_file, 'w') as f:
                f.write(phone)
            return phone
        except Exception as e:
            print(f"\033[35mОШИБКА: {e}. Попробуйте снова\033[0m")

async def load_module(client, module_name):
    """Загружает и инициализирует модуль"""
    try:
        module = import_module(f'modules.{module_name}')
        if hasattr(module, 'setup'):
            await module.setup(client)
        else:
            print(f"\033[35mВ {module_name} нет функции setup()\033[0m")
    except Exception as e:
        print(f"\033[35mОШИБКА!!! В {module_name}: {str(e)}\033[0m")

async def main():
    phone = get_phone_numder()
    
    client = TelegramClient('session', api_id, api_hash)

    try:
        await client.start(phone)
        clear_terminal()
        print("\033[32m██████╗ ██╗ ██████╗██╗   ██╗███╗   ██╗ ██████╗ ██████╗  █████╗ ███╗   ███╗\n██╔══██╗██║██╔════╝██║   ██║████╗  ██║██╔════╝ ██╔══██╗██╔══██╗████╗ ████║\n██████╔╝██║██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║██╔████╔██║\n██╔═══╝ ██║██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║\n██║     ██║╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║\n╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝\033[0m")
        print(f"\033[35mИспользуется номер: {phone}\033[0m")
        print("\033[35mАвторизация прошла успешно!!!\033[0m")

        module_files = [
            f[:-3] for f in os.listdir(modules_dir)
            if f.endswith('.py') and not f.startswith('_')
        ]

        for module_name in module_files:
            await load_module(client, module_name)

        print("\033[35mУспешно!\033[0m")
        await client.run_until_disconnected()

    except Exception as e:
        print(f"\033[35mОШИБКА!!! : {str(e)}\033[0m")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())