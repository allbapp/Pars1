from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Функция для инициализации браузера
def init_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # для работы без открытия окна браузера
    driver = webdriver.Chrome(options=options)
    return driver

# Функция для поиска в Википедии
def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # ожидание загрузки страницы
    return driver.current_url

# Функция для получения параграфов статьи
def get_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    return [p.text for p in paragraphs if p.text.strip()]

# Функция для получения ссылок на связанные статьи
def get_links(driver):
    links = driver.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    return {link.text: link.get_attribute("href") for link in links if link.text.strip()}

def main():
    driver = init_browser()

    try:
        while True:
            query = input("Введите запрос для поиска в Википедии: ")
            if query.lower() in ['выход', 'exit']:
                break

            url = search_wikipedia(driver, query)
            driver.get(url)

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Выйти из программы")

                choice = input("Введите номер действия: ")

                if choice == '1':
                    paragraphs = get_paragraphs(driver)
                    for i, paragraph in enumerate(paragraphs):
                        print(f"\nПараграф {i+1}:\n{paragraph}\n")
                        if input("Нажмите Enter для продолжения или 'q' для выхода: ").lower() == 'q':
                            break

                elif choice == '2':
                    links = get_links(driver)
                    print("\nСвязанные страницы:")
                    for i, (text, link) in enumerate(links.items()):
                        print(f"{i+1}. {text}")

                    link_choice = int(input("Введите номер связанной страницы для перехода: ")) - 1
                    selected_link = list(links.values())[link_choice]
                    driver.get(selected_link)

                elif choice == '3':
                    return
                else:
                    print("Неверный выбор, попробуйте снова.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
