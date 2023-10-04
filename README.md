# <img src="https://s8d5.turboimg.net/sp/5109159e6d4a480e1e2ad2e631178759/logo.png" width="24" height="24"> Блогикум

## Описание
Социальная сеть для публикации личных дневников.
Сайт, на котором пользователь может создать свою страницу и 
публиковать на ней сообщения («посты»).

## Функционал сайта
- Для каждого поста существует категория — например «путешествия», 
«кулинария» или «python-разработка», а также опционально можно указать
локацию, с которой связан пост.

- Пользователь может перейти на страницу любой категории и 
увидеть все посты, которые к ней относятся.

- Пользователи могут заходить на чужие страницы, читать 
и комментировать чужие посты.

- Для своей страницы автор может задать имя и уникальный адрес.

- Есть возможность модерировать записи и блокировать пользователей,
рассылающих спам.

### Необходимые инструменты

* [Python](https://www.python.org/)
* [Pip](https://pypi.org/project/pip/)
* [Django](https://www.djangoproject.com/)


### Как запустить проект:

* Клонировать репозиторий и перейти в его директорию

* Cоздать и активировать виртуальное окружение:

    * Windows
    ```shell
    python -m venv venv
    ```
    ```shell
    source venv/Scripts/activate
    ```

    * Linux/macOS
    ```shell
    python3 -m venv venv
    ```
    ```shell
    source venv/bin/activate
    ```


* Обновить PIP

    ```shell
    python -m pip install --upgrade pip
    ```

* Установить зависимости из файла requirements.txt:

    ```shell
    pip install -r requirements.txt
    ```

* Выполнить миграции:

    ```shell
    python manage.py makemigrations
    ```
    ```shell
    python manage.py migrate
    ```


* Запустить проект:

    ```shell
    python manage.py runserver
    ```

### Используемые технологии

[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

### Разработка проекта

* Максим Субботин — BackEnd Developer