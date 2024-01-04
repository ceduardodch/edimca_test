from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.firefox.options import Options
import time
import re
import random

def task(url,thread_number):

    try:
        
        print(f"Hilo {thread_number}: iniciado")

        # Path to the GeckoDriver executable
        geckodriver_path = 'driver\\geckodriver.exe'  # Replace with the actual path to geckodriver

        # Set up the service for GeckoDriver
        service = Service(executable_path=geckodriver_path)

        # Initialize the Firefox WebDriver
        firefox_options = Options()
        firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

        firefox_options.add_argument("--headless")  # Activa el modo sin cabeza
        driver = webdriver.Firefox(service=service, options=firefox_options)
        print(f"Hilo {thread_number}: Navegador iniciado, accediendo a {url}")

        driver.get(url)

        # Wait for the page to load
        time.sleep(2)  # It's better to use explicit waits instead of time.sleep()

        # Enter the username
        username_input = driver.find_element(By.XPATH, '//input[@placeholder="usuario"]')
        username_input.send_keys('TEST_POS4')  # Replace with the actual username

        # Enter the password
        password_input = driver.find_element(By.XPATH, '//input[@placeholder="contraseña"]')
        password_input.send_keys('lepton')  # Replace with the actual password

        # Click the submit button
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # Wait for the next page to load or for login to complete
        time.sleep(5)  # It's better to use explicit waits here as well

        # After login, wait for the image with alt "sierra" to be clickable
        sierra_image = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//img[@alt="sierra"]'))
        )

        # Click the image
        sierra_image.click()
        time.sleep(5)  # It's better to use explicit waits here as well
        client_input = driver.find_element(By.XPATH, '//input[@id="srchCUstId"]')
        client_input.send_keys('19994')  # Replace with the actual username

        search_button = driver.find_element(By.XPATH, '//button[@id="idSearchInputButton"]')
        search_button.click()
        time.sleep(25)  # It's better to use explicit waits here as well


        input_table_body = driver.find_element(By.CLASS_NAME, "p-datatable-tbody")
        children_rows = input_table_body.find_elements(By.XPATH, 'tr')

        for child_row in children_rows:
            children_columns = child_row.find_elements(By.XPATH, 'td')
            children_columns_list = []

            for child_column in children_columns:
                if child_column.get_attribute("class") == 'p-editable-column' and re.search(r'_([1-3])$', child_column.get_attribute('id')):
                    children_columns_list.append(child_column)

            for col in children_columns_list:
                try:
                    # Espera hasta que el elemento sea clickeable
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(col))
                    col.click()
                    try:
                        # Espera hasta que el input esté presente en el elemento
                        input_field = WebDriverWait(col, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'input'))
                        )
                        random_int = random.randint(100, 200)
                        input_field.clear()  # Limpia cualquier texto existente antes de escribir
                        input_field.send_keys(f'{random_int}')
                    except TimeoutException:
                        print("Timeout esperando el campo de entrada")
                    except StaleElementReferenceException:
                        print("Referencia obsoleta del elemento")
                except TimeoutException:
                    print("Timeout esperando que la columna sea clickeable")
                except NoSuchElementException:
                    print("Elemento no encontrado")

        print(f"Hilo {thread_number}: Ingresando cantidades de material")

        time.sleep(10)  # It's better to use explicit waits here as well

            
        client_input = driver.find_element(By.XPATH, '//input[@name="value4"]')
        client_input.send_keys('COCINA')  # Replace with the actual username
        time.sleep(5)  # It's better to use explicit waits here as well
        sierra_image2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//img[@alt="sierra"]'))
            )
        sierra_image2.click()
        time.sleep(25)  # It's better to use explicit waits here as well
        sierra_image3 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//img[@alt="close"]'))
            )
        sierra_image3.click()

        time.sleep(5)  # It's better to use explicit waits here as well
        sierra_image4 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//img[@alt="proforma"]'))
            )

                # Click the image
        sierra_image4.click()
        time.sleep(4)  # It's better to use explicit waits here as well
        
        xpath_expression = '//button[text()="Generar orden"]'    
        submit_button2 = driver.find_element(By.XPATH, xpath_expression)
        submit_button2.click()
        time.sleep(20)  # It's better to use explicit waits here as well
        print(f"Hilo {thread_number}: Tarea completada")
        driver.save_screenshot(f"printscreenshots/printscreenshot{thread_number}.png")
        driver.quit()
    except Exception as e:
        print(f"Hilo {thread_number}: Error occurred - {str(e)}")
    finally:
        driver.quit()



def launch_tasks_in_batches(urls, batch_size, delay_between_batches):
    executor = ThreadPoolExecutor(max_workers=batch_size)
    futures = []
    thread_number = 0  # Contador para el número de hilo

    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i + batch_size]
        for url in batch_urls:
            future = executor.submit(task, url, thread_number)
            futures.append(future)
            thread_number += 1  # Incrementa el contador para cada nuevo hilo
        print(f"Lanzando lote {i // batch_size + 1}")
        time.sleep(delay_between_batches)

    # Esperar a que todas las tareas se completen
    for future in as_completed(futures):
        future.result()  # Esto bloqueará hasta que la tarea específica se complete

    executor.shutdown(wait=True)

urls = ["http://172.16.148.130:5000/login#/login"] * 100  # Lista de URLs
BATCH_SIZE = 10
DELAY_BETWEEN_BATCHES = 150  # 30 segundos de retraso entre cada lote

launch_tasks_in_batches(urls, BATCH_SIZE, DELAY_BETWEEN_BATCHES)
