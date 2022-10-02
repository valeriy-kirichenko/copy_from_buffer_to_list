import os
import time
from ctypes import windll

import clipboard
from pynput import keyboard
from rich.console import Console
from rich.table import Table

HELLO_MESSAGE = (
    'Скопированные строки сохраняются в списке который будет выводиться '
    'в окне программы.\nПри вставке из списка, строки отдаются по принципу '
    '"первая скопированная - отдается первой, вторая - второй и т.д."\n'
    'Все стандартно:\n\tКопировать - Ctrl+c.\n\tВствить - Ctrl+v.\n'
    'Если по ошибке скопировалась не та строка, можно кликнуть по пустому '
    'месту в окне \nпрограммы(не в поле ввода текста!) и нажать Ctrl+v, '
    'тогда ненужный текст удалиться из списка.\n'
    )


class Queue:
    def __init__(self) -> None:
        self.queue = []

    def push(self):
        if clipboard.paste():
            self.queue.append(clipboard.paste())
            clipboard.copy(self.queue[0])

    def pop(self):
        try:
            self.queue.pop(0)
            if self.queue:
                clipboard.copy(self.queue[0])
            else:
                clear_buffer()
        except IndexError:
            pass

    def get_queue(self):
        return self.queue


def clear_buffer():
    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_data(data, is_v=True):
    table_data = Table()
    table_data.add_column("Скопированные данные:", style="magenta")
    if data:
        for number, text in enumerate(data, 1):
            table_data.add_row(
                f'{number}. {text}', style="cyan", end_section=True
            )
        console.print(table_data)
    else:
        if is_v:
            clear_console()
            table_data.add_row('Нет данных', style="cyan")
            console.print(table_data)


def on_activate_c():
    time.sleep(1/10)
    queue.push()
    clear_console()
    print_data(queue.get_queue(), is_v=False)


def on_activate_v():
    time.sleep(1/10)
    queue.pop()
    clear_console()
    print_data(queue.get_queue())


if __name__ == '__main__':
    clear_buffer()
    table = Table()
    table.add_column("Описание:", style="magenta")
    table.add_row(HELLO_MESSAGE, style="cyan")

    console = Console()
    console.print(table)

    queue = Queue()
    with keyboard.GlobalHotKeys(
        {'<ctrl>+c': on_activate_c, '<ctrl>+v': on_activate_v}
    ) as h:
        h.join()
