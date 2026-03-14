# Автотест для saucedemo.com

автотест на Python с использованием фреймворка Selenium, который:
* Авторизуется на сайте (логин/пароль).
* Добавляет любой товар в корзину.
* Проверяет, что товар появился в корзине

## Структура проекта
#### Travel_Designer/
#### │
#### ├── requirements.txt
#### ├── test_cart_functionality.py
#### └── README.md

## Требования

* Python 3.8+
* Chrome Browser (последней версии)
* ChromeDriver (совместимый с версией браузера)

### Установка зависимостей

> `pip install -r requirements.txt`
 
### Запустить тесты с генерацией Allure-отчёта

> `pytest --alluredir=allure-results test_cart_functionality.py`

### Сгенерировать и просмотреть отчёт Allure

> `allure serve allure-results`

