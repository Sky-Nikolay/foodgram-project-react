# praktikum_new_diplom

работает апи согласно ТЗ

http://127.0.0.1:8000/api


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:
```

### 1. Cоздать и активировать виртуальное окружение:

```
python -m venv env
source venv/bin/activate
python -m pip install --upgrade pip
```

### 2. Установить зависимости из файла requirements.txt и необходимые модули:

```
pip install -r requirements.txt
```

```
pip install django
pip install djangorestframework
pip install pillow
pip install cryptography==2.9.2  # to solve problems with Rust
pip install -U djoser
pip install djoser djangorestframework-simplejwt==4.7.2
```

### 3. Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

### 4. Запустить проект:

```
python manage.py runserver
```

### 5.  Примеры выполнения запросов: