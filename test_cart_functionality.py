import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class TestCartFunctionality(unittest.TestCase):
    """
    Автотест для проверки добавления товара в корзину на сайте saucedemo.com
    """

    def setUp(self):
        """
        Настройка драйвера и открытие сайта перед каждым тестом
        """
        # Инициализируем драйвер Chrome
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # Разворачиваем окно на весь экран
        self.driver.get("https://www.saucedemo.com/")

        # Ждём загрузки страницы и элементов
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )

    def test_add_item_to_cart(self):
        """
        Тест: авторизация → добавление товара в корзину → проверка наличия товара
        """
        driver = self.driver

        # Шаг 1: Авторизация на сайте
        print("Шаг 1: Выполняем авторизацию...")

        # Ввод логина
        username_field = driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")

        # Ввод пароля
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")

        # Нажатие кнопки входа
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Ожидаем загрузки каталога товаров
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        print("Авторизация успешна!")

        # Шаг 2: Добавление товара в корзину
        print("Шаг 2: Добавляем товар в корзину...")

        # Находим первый доступный товар и кнопку "Add to cart"
        add_to_cart_button = driver.find_element(
            By.CSS_SELECTOR, ".inventory_item:first-child .btn_primary"
        )
        add_to_cart_button.click()

        # Ждём изменения счётчика корзины
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
        )
        print("Товар добавлен в корзину!")

        # Шаг 3: Проверка наличия товара в корзине
        print("Шаг 3: Проверяем наличие товара в корзине...")

        # Переходим в корзину
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        # Ожидаем загрузки корзины
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )

        # Проверяем, что в корзине есть хотя бы один товар
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertGreaterEqual(len(cart_items), 1, "В корзине нет товаров!")

        # Дополнительно проверяем счётчик корзины (должен быть 1)
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(cart_badge.text, "1", "Счётчик корзины не соответствует ожидаемому")

        print("Тест пройден успешно: товар успешно добавлен в корзину и отображается корректно!")

    def tearDown(self):
        """
        Закрытие браузера после завершения теста
        """
        self.driver.quit()



if __name__ == "__main__":
    unittest.main()
