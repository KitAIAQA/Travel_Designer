import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import allure
from allure_commons.types import AttachmentType




# Фикстура для инициализации драйвера (вместо setUp/tearDown)
@pytest.fixture
def driver():
    chrome_options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()  # Автоматически закроет драйвер после теста


# Основной тест
@allure.epic("Функциональное тестирование")
@allure.feature("Корзина покупок")
@allure.story("Добавление товара в корзину")
@allure.title("Тест: авторизация → добавление товара → проверка корзины")
def test_add_item_to_cart(driver):
    """
    Тест: авторизация → добавление товара в корзину → проверка наличия товара
    """

    # Шаг 1: Авторизация на сайте
    @allure.step("Шаг 1: Авторизация на сайте")
    def authorize():
        driver.get("https://www.saucedemo.com/")
        allure.attach(driver.get_screenshot_as_png(),
                     name="Перед авторизацией",
                     attachment_type=AttachmentType.PNG)

        username_field = driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Ждём загрузки каталога товаров
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        allure.attach(driver.get_screenshot_as_png(),
                     name="После авторизации",
                     attachment_type=AttachmentType.PNG)
        print("Авторизация успешна!")

    authorize()

    # Шаг 2: Добавление товара в корзину
    @allure.step("Шаг 2: Добавление товара в корзину")
    def add_to_cart():
        add_to_cart_button = driver.find_element(
            By.CSS_SELECTOR, ".inventory_item:first-child .btn_primary"
        )
        add_to_cart_button.click()

        # Ждём изменения счётчика корзины
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
        )
        allure.attach(driver.get_screenshot_as_png(),
                     name="Товар добавлен в корзину",
                     attachment_type=AttachmentType.PNG)
        print("Товар добавлен в корзину!")

    add_to_cart()

    # Шаг 3: Проверка наличия товара в корзине
    @allure.step("Шаг 3: Проверка наличия товара в корзине")
    def check_cart():
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        # Ожидаем загрузки корзины
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        allure.attach(driver.get_screenshot_as_png(),
                     name="Содержимое корзины",
                     attachment_type=AttachmentType.PNG)

        # Проверяем, что в корзине есть хотя бы один товар
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) >= 1, "В корзине нет товаров!"

        # Проверяем счётчик корзины (должен быть 1)
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1", "Счётчик корзины не соответствует ожидаемому"

        print("Тест пройден успешно: товар успешно добавлен в корзину и отображается корректно!")

    check_cart()
