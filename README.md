# google-sheets-test
Скрипт считывающий данные из таблицы гугл и записывающий в базу данных


Чтобы запустить скрипты необходимо на сервере поднять базу данных postgresql. 
Данные для подключения базу необходимо добавить в файл data_auth.txt в формате: адрес_подключения пользователь пароль название_базы порт
Например (localhost postgres 12345678 test_base 5432).

Из папки с проектом в териминале выполнить команду pip install -r requirements.txt
Далее необходимо создать телеграмм бота и в папке с проектом создать файл token.txt куда добавить токен от телеграмм бота.

Теперь выполняем команду python3 main.py

Учитывая, что бот еще не знает вас, после запуска скрипта надо будет пойти в бота и написать ему /start, после этого он пришлет уведомления по всем поставкам, срок которых истек.

Скрипт запустился, теперь можно пользоваться таблицей https://docs.google.com/spreadsheets/d/1lOKNBD1sdYi53OrQBHY4jZSVRLtyRyRyhe8L3A6UOCU/edit?usp=sharing с аккаунта amkolotov@gmail.com

Изменения можно смотреть в базе данных удобным для вас способом.
