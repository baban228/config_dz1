# Эмулятор оболочки

Это эмулятор оболочки на основе Python, который позволяет пользователю взаимодействовать с ZIP-архивом как с файловой системой. Он поддерживает стандартные команды оболочки, такие как `ls`, `cd`, `echo` и `uniq`, а также несколько других функций. Эмулятор работает с ZIP-архивом, который содержит каталоги и файлы, с которыми можно работать: навигация, вывод списка файлов и папок, а также редактирование файлов.

## Возможности

- **Навигация**: Перемещение по виртуальной файловой системе, хранящейся в ZIP-архиве.
- **Вывод списка файлов**: Используйте команду `ls` для отображения файлов и каталогов в текущем каталоге.
- **Смена каталога**: Используйте команду `cd <путь>` для смены текущего каталога.
- **Вывод сообщения**: Используйте команду `echo <сообщение>` для вывода сообщения в терминал.
- **Уникальные строки**: Используйте команду `uniq <файл>` для отображения уникальных строк из файла.
- **Дерево каталогов**: Просмотр структуры каталогов в ZIP-архиве.
- **Выход**: Выход из эмулятора оболочки.

## Требования

Убедитесь, что на вашей системе установлены следующие модули Python:

- `zipfile` (входит в стандартную библиотеку Python, не требует установки)

## Использование

1. **Настройка среды**:
   - Эмулятор ожидает наличие файла `config.xml` в той же директории.
   - Первая строка файла `config.xml` должна содержать имя эмулятора (например, `shell_name`).
   - Во второй строке указывается путь к ZIP-архиву, который будет использоваться как файловая система.

2. **Запуск эмулятора**:
   - Клонируйте этот репозиторий на свою локальную машину.
   - Убедитесь, что файл `config.xml` настроен правильно.
   - Запустите скрипт:

     ```bash
     python shell_emulator.py
     ```

3. **Команды**:
   Эмулятор поддерживает следующие команды:

   - **ls**: Вывести список файлов и каталогов в текущем каталоге.
   
     Пример:
     ```
     <shell_name: /># ls
     file1.txt
     dir1/
     ```

   - **cd <путь>**: Переместиться в указанный каталог.
   
     Пример:
     ```
     <shell_name: /># cd dir1
     <shell_name: /dir1># 
     ```

   - **echo <сообщение>**: Вывести указанное сообщение.
   
     Пример:
     ```
     <shell_name: /dir1># echo Hello World!
     Hello World!
     ```

   - **uniq <файл>**: Отобразить уникальные строки из файла.
   
     Пример:
     ```
     <shell_name: /dir1># uniq file1.txt
     line1
     line2
     line3
     ```

   - **tree**: Показать структуру каталогов ZIP-архива.
   
     Пример:
     ```
     <shell_name: /># tree
     /file1.txt
     /dir1/
         /file2.txt
     ```

   - **exit**: Выход из эмулятора.

## Структура кода

Основной класс в коде называется `shell_emulator`, который инкапсулирует логику взаимодействия с ZIP-архивом как с файловой системой. Основные компоненты:

- `__init__(self)`: Инициализация эмулятора оболочки, загрузка конфигурации и открытие ZIP-архива.
- `ls(self)`: Выводит список файлов и каталогов в текущем пути.
- `cd(self, com)`: Меняет текущий каталог в соответствии с указанным путем.
- `uniq(self, filename)`: Отображает уникальные строки из указанного файла.
- `sawed_off_path(self, path)`: Вспомогательный метод для удаления последней части пути.
- `create_path(self, path)`: Обеспечивает правильный формат пути.

## Пример файла `config.xml`

```xml
shell_name
путь_к_zip_архиву.zip
```

Замените `shell_name` на имя, которое вы хотите, чтобы эмулятор отображал, а `путь_к_zip_архиву.zip` на путь к ZIP-архиву, который будет использоваться как файловая система.

## Лицензия

Этот проект распространяется под лицензией MIT — смотрите файл [LICENSE](LICENSE) для подробностей.

