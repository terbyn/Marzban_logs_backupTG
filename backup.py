bot_token = 'token'
chat_id = 'chat id'
import asyncio
import shutil
import tarfile
from datetime import datetime
import os
from aiogram import Bot, types

async def cleanup_temporary_directories(var_dir, opt_dir):
    shutil.rmtree(var_dir)
    shutil.rmtree(opt_dir)

async def send_to_telegram(archive_path, chat_id, api_token):
    bot = Bot(token=api_token)
    with open(archive_path, 'rb') as archive_file:
        try:
            await bot.send_document(chat_id, types.InputFile(archive_file, filename='backup.tar.gz'))
            print("Архив отправлен")
        except Exception as e:
            print(f"Ошибка при отправке архива в Telegram: {e}")
        finally:
            await bot.session.close()

async def send_large_file_to_telegram(archive_path, max_size, chat_id, api_token):
    bot = Bot(token=api_token)
    with open(archive_path, 'rb') as archive_file:
        file_part_number = 1
        while True:
            chunk = archive_file.read(max_size)
            if not chunk:
                break
            try:
                file_part = types.InputFile(archive_file, filename=f"backup_part_{file_part_number}.tar.gz")
                await bot.send_document(chat_id, file_part)
                file_part_number += 1
            except Exception as e:
                print(f"Ошибка при отправке архива в Telegram: {e}")
            finally:
                await bot.session.close()
                print("Архив отправлен")

async def backup_directories():
    while True:
        source_directory_1 = "/var/lib/marzban"  # Указать свой путь
        source_directory_2 = "/opt/marzban"      # Указать свой путь
        backup_directory = "/root/backup/"        # Указать свой путь
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"backup_{timestamp}.tar.gz"
        archive_path = os.path.join(backup_directory, archive_name)
        # Создаем структуру каталогов внутри /root/backup
        backup_var_dir = os.path.join(backup_directory, 'var')
        backup_opt_dir = os.path.join(backup_directory, 'opt')
        # Копируем данные в соответствующие каталоги
        shutil.copytree(source_directory_1, backup_var_dir)
        shutil.copytree(source_directory_2, backup_opt_dir)
        with tarfile.open(archive_path, "w:gz") as archive:
            # Архивируем содержимое каталогов var и opt
            archive.add(backup_var_dir, arcname='var')
            archive.add(backup_opt_dir, arcname='opt')
        print("Архив создан")
        try:
            # Проверяем размер архива
            file_size = os.path.getsize(archive_path)
            max_size = 50 * 1024 * 1024  # 50 MB
            if file_size > max_size:
                await send_large_file_to_telegram(archive_path, max_size, chat_id, bot_token)
            else:
                await send_to_telegram(archive_path, chat_id, bot_token)
        except Exception as e:
            print(f"Ошибка при выполнении резервного копирования: {e}")
        finally:
            # Удаляем временные каталоги
            await cleanup_temporary_directories(backup_var_dir, backup_opt_dir)
        
        # Ожидание 5 минут перед следующей итерацией
        await asyncio.sleep(5 * 60)

if __name__ == "__main__":
    asyncio.run(backup_directories())
