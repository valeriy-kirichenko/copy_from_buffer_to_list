import os
import time
from ctypes import windll
from typing import List

import clipboard
from pynput import keyboard
from rich.console import Console
from rich.table import Table

INFO_MESSAGE: str = (
    'Скопированные строки сохраняются в списке который будет выводиться '
    'в окне программы.\nПри вставке из списка, строки отдаются по принципу '
    '"первая скопированная - отдается первой, вторая - второй и т.д."\n'
    'Для отправки множества копий одного текста достаточно включить режим '
    '"∞" нажав Ctrl+b. Перед первым элементом в списке появится знак '
    'бесконечности. При повторном нажатии - отключается режим "∞", из списка '
    'убирается первый элемент.\n'
    'Все стандартно:\n\tКопировать - Ctrl+c.\n\tВствить - Ctrl+v.\n'
    'Если по ошибке скопировалась не та строка, можно кликнуть по пустому '
    'месту в окне \nпрограммы(не в поле ввода текста!) и нажать Ctrl+v, '
    'тогда ненужный текст удалиться из списка.\n'
    )


class Queue:
    """Класс для хранения очереди скопированных из буфера обмена данных в
    текстовом формате.
    """

    def __init__(self) -> None:
        self.queue: List[str] = []
        self.many_copies: bool = False

    def push(self) -> None:
        """Добавляет в очередь скопированный текст."""
        paste_data = clipboard.paste()
        if paste_data:
            self.queue.append(paste_data)
            clipboard.copy(self.queue[0])

    def pop(self) -> None:
        """Убирает из очереди первый элемент и копирует его в буфер обмена."""

        try:
            if not self.many_copies:
                self.queue.pop(0)
                if self.queue:
                    clipboard.copy(self.queue[0])
                else:
                    clear_buffer()
            else:
                pass
        except IndexError:
            pass

    def get_queue(self) -> list:
        """Возвращает список со скопированными данными."""

        return self.queue


def clear_buffer() -> None:
    """Очищает буфер обмена."""

    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()


def clear_console() -> None:
    """Очищает консоль."""

    os.system('cls' if os.name == 'nt' else 'clear')


def print_data(data: List[str], is_v: bool = True) -> None:
    """Выводит в консоль данные из очереди в виде таблицы.

    Args:
        data (List[str]): список со скопированными данными.
        is_v (bool, optional): Флаг для "Ctrl+v". По умолчанию True.
    """

    table_data: Table = Table()
    table_data.add_column("Скопированные данные:", style="magenta")
    if data:
        for number, text in enumerate(data, 1):
            if number == 1 and queue.many_copies:
                table_data.add_row(
                    f'∞ {number}. {text}', style="cyan", end_section=True
                )
            else:
                table_data.add_row(
                    f'{number}. {text}', style="cyan", end_section=True
                )
        console.print(table_data)
    else:
        if is_v:
            clear_console()
            if queue.many_copies:
                table_data.add_row('Нет данных (∞)', style="cyan")
            else:
                table_data.add_row('Нет данных', style="cyan")
            console.print(table_data)


def on_activate_ctrl_c() -> None:
    """Выполняется при нажатии "Ctrl+c", копирует текст в очередь."""

    time.sleep(1/10)
    queue.push()
    clear_console()
    print_data(queue.get_queue(), is_v=False)


def on_activate_ctrl_v() -> None:
    """Выполняется при нажатии "Ctrl+v", вставляет текст из очереди."""

    time.sleep(1/10)
    queue.pop()
    clear_console()
    print_data(queue.get_queue())


def on_activate_ctrl_b() -> None:
    """Включает режим "∞" позволяющий копировать первый элемент в списке
    множество раз."""

    if queue.many_copies:
        if queue.get_queue():
            queue.queue.pop(0)
            try:
                clipboard.copy(queue.queue[0])
            except IndexError:
                pass
        else:
            clear_buffer()
        queue.many_copies = False
        clear_console()
        print_data(queue.get_queue())
    else:
        queue.many_copies = True
        clear_console()
        print_data(queue.get_queue())


if __name__ == '__main__':
    clear_buffer()  # Очишаем буфер перед началом работы.

    # Создаем таблицу для информационного сообщения.
    table_info: Table = Table()
    table_info.add_column("Описание:", style="magenta")
    table_info.add_row(INFO_MESSAGE, style="cyan")

    console: Console = Console()
    console.print(table_info)

    queue: Queue = Queue()
    with keyboard.GlobalHotKeys(
        {
            '<ctrl>+c': on_activate_ctrl_c,
            '<ctrl>+с': on_activate_ctrl_c,
            '<ctrl>+v': on_activate_ctrl_v,
            '<ctrl>+м': on_activate_ctrl_v,
            '<ctrl>+b': on_activate_ctrl_b,
            '<ctrl>+и': on_activate_ctrl_b,
        }
    ) as h:
        h.join()
