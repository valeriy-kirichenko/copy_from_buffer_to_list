# copy_from_buffer_to_list:floppy_disk:
Описание скрипта
----------
Скрипт прослушивает события клавиатуры и реагирует на горячие клавишы "Ctrl+c" и "Ctrl+v", при копировании сохраняет текст в очередь, при вставке отдает данные по принципу FIFO(first in, first out). В консоль выводится пронумерованный список который обновляется после каждого события.

----------

# Установка
Системные требования
----------
* Python 3.9+

Стек технологий
----------
* Python 3.9

Запуск проекта
----------
1. Клонируйте репозиторий, наберите в командной строке:
```bash
git clone 'git@github.com:valeriy-kirichenko/copy_from_buffer_to_list.git'
```
2. Установите необходимые для работы скрипта модули и библиотеки:
```bash
pip install clipboard pynput rich
```
3. Запустите проект, выполните команду:
```bash
python copy_from_buffer_to_list.py
```
4. Надеюсь кому то пригодится!

----------
Автор:
----------
* **Кириченко Валерий Михайлович**
GitHub - [valeriy-kirichenko](https://github.com/valeriy-kirichenko)
----------
Документация к проекту
----------
На данный момент документация отсутствует.
