import asyncio
import threading

from weather import periodic_task
from export_excel import export_to_excel


def run_weather() -> None:
    """Запуск получения данных и запись в бд"""
    asyncio.run(periodic_task(60))


def run_excel(file_name: str) -> None:
    asyncio.run(export_to_excel(file_name))


def command_handler() -> None:
    """Запуск всех задач"""
    weather_thread = threading.Thread(target=run_weather, args=())
    weather_thread.daemon = True
    weather_thread.start()

    while True:
        command = input("Введите команду (export <filename> для экспорта в Excel\n")
        if command.startswith("export"):
            _, filename = command.split()
            excel_thread = threading.Thread(target=run_excel, args=(filename,))
            print(f'Создается файл {filename}')
            excel_thread.start()
            excel_thread.join()
            print(f'Файл {filename} создан')
        

if __name__ == '__main__':
    command_handler()
