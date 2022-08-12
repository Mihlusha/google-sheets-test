# google-sheets-test
Скрипт считывающий данные из таблицы гугл и записывающий в базу данных


Чтобы запустить скрипты необходимо на сервере поднять базу данных postgresql. 
Данные для подключения базу необходимо добавить в файл data_auth.txt в формате: адрес_подключения пользователь пароль название_базы порт
Например (localhost postgres 12345678 test_base 5432).

Из папки с проектом в териминале выполнить команду pip install -r requirements.txt

Теперь выполняем команду python3 main.py

Если увидели текст:
XMLParsedAsHTMLWarning: It looks like you're parsing an XML document using an HTML parser. If this really is an HTML document (maybe it's XHTML?), you can ignore or filter this warning. If it's XML, you should know that using an XML parser will be more reliable. To parse this document as XML, make sure you have the lxml package installed, and pass the keyword argument `features="xml"` into the BeautifulSoup constructor.
  warnings.warn(

Значит скрипт запустился, теперь можно пользоваться таблицей https://docs.google.com/spreadsheets/d/1lOKNBD1sdYi53OrQBHY4jZSVRLtyRyRyhe8L3A6UOCU/edit?usp=sharing с аккаунта amkolotov@gmail.com


Изменения можно смотреть в базе данных удобным для вас способом.
