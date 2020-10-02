Mobile Balance
==============

Операторы частенько ломают ручки, через которые библиотека запрашивает состояние баланса.
Посему приходится это чинить и публиковать багфиксы. Следите за обновлениями на AllMyChanges.com:  
[![ChangeLog](http://allmychanges.com/p/python/mobile-balance/badge/)](http://allmychanges.com/p/python/mobile-balance/)

Поддерживаемые операторы
------------------------

* МТС
* Мегафон
* TELE2
* ТТК
* Билайн

Установка
---------

Делаем как обычно: `pip install mobile-balance`

Установка из исходников
---------

`pip install .`

Использование
-----

Указываем мобильного оператора, номер телефона и пароль от личного кабинета:

    $ mobile-balance mts --phone=9154041111 --password=too-secret-to-share
    196.513792

Кому спасибо
------------

* [Артеменко Александру](https://github.com/svetlyak40wt) — за первоначальный релиз.
* [Владимиру Улупову](https://github.com/vaal-) — за поддержку TELE2.
* [Денису Рыкову](https://github.com/drnextgis) - за поддержку ТрансТелеком и исправления TELE2.

Хочешь помочь и попасть в список? Пришли pull-request!
