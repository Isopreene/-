import os
import re
import shutil
import time
import zipfile
from zipfile import ZipFile
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

pages = ('https://stepik.org/lesson/569748/step/1?unit=564262', 'https://stepik.org/lesson/569749/step/1?unit=564263',
         'https://stepik.org/lesson/609341/step/1?unit=604560', 'https://stepik.org/lesson/570048/step/1?unit=564591',
         'https://stepik.org/lesson/611754/step/1?unit=607091', 'https://stepik.org/lesson/570050/step/1?unit=564593',
         'https://stepik.org/lesson/571244/step/1?unit=565785', 'https://stepik.org/lesson/570055/step/1?unit=564599',
         'https://stepik.org/lesson/570049/step/1?unit=564592', 'https://stepik.org/lesson/745789/step/1?unit=747565',
         'https://stepik.org/lesson/520159/step/1?unit=512678', 'https://stepik.org/lesson/518491/step/1?unit=510939',
         'https://stepik.org/lesson/518492/step/1?unit=510940', 'https://stepik.org/lesson/623073/step/1?unit=618703',
         'https://stepik.org/lesson/547172/step/1?unit=540798', 'https://stepik.org/lesson/584474/step/1?unit=579234',
         'https://stepik.org/lesson/737724/step/1?unit=739371', 'https://stepik.org/lesson/624148/step/1?unit=619836',
         'https://stepik.org/lesson/624529/step/1?unit=620219', 'https://stepik.org/lesson/624150/step/1?unit=619838',
         'https://stepik.org/lesson/625739/step/1?unit=621492', 'https://stepik.org/lesson/624149/step/1?unit=619837',
         'https://stepik.org/lesson/590123/step/1?unit=585067', 'https://stepik.org/lesson/631917/step/1?unit=627943',
         'https://stepik.org/lesson/590034/step/1?unit=584966', 'https://stepik.org/lesson/740203/step/1?unit=741843',
         'https://stepik.org/lesson/590035/step/1?unit=584967', 'https://stepik.org/lesson/634520/step/1?unit=630783',
         'https://stepik.org/lesson/590120/step/1?unit=585064', 'https://stepik.org/lesson/635441/step/1?unit=631831',
         'https://stepik.org/lesson/634670/step/1?unit=630932', 'https://stepik.org/lesson/743710/step/1?unit=745474',
         'https://stepik.org/lesson/745796/step/1?unit=747574', 'https://stepik.org/lesson/656891/step/1?unit=653974',
         'https://stepik.org/lesson/640050/step/1?unit=636570', 'https://stepik.org/lesson/744448/step/1?unit=746216',
         'https://stepik.org/lesson/640051/step/1?unit=636571', 'https://stepik.org/lesson/640052/step/1?unit=636572',
         'https://stepik.org/lesson/594136/step/1?unit=589172', 'https://stepik.org/lesson/637962/step/1?unit=634429',
         'https://stepik.org/lesson/594137/step/1?unit=589173', 'https://stepik.org/lesson/594680/step/1?unit=589701',
         'https://stepik.org/lesson/640035/step/1?unit=636555', 'https://stepik.org/lesson/645394/step/1?unit=641995',
         'https://stepik.org/lesson/640036/step/1?unit=636556', 'https://stepik.org/lesson/647292/step/1?unit=643926',
         'https://stepik.org/lesson/651459/step/1?unit=648165', 'https://stepik.org/lesson/655394/step/1?unit=652334',
         'https://stepik.org/lesson/640039/step/1?unit=636559', 'https://stepik.org/lesson/640040/step/1?unit=636560',
         'https://stepik.org/lesson/751476/step/1?unit=753330', 'https://stepik.org/lesson/668458/step/1?unit=666568',
         'https://stepik.org/lesson/640044/step/1?unit=636564', 'https://stepik.org/lesson/668595/step/1?unit=666704',
         'https://stepik.org/lesson/669733/step/1?unit=667881', 'https://stepik.org/lesson/640048/step/1?unit=636568',
         'https://stepik.org/lesson/640049/step/1?unit=636569', 'https://stepik.org/lesson/673155/step/1?unit=671418',
         'https://stepik.org/lesson/640045/step/1?unit=636565', 'https://stepik.org/lesson/666563/step/1?unit=664567',
         'https://stepik.org/lesson/674263/step/1?unit=672698', 'https://stepik.org/lesson/674986/step/1?unit=673426',
         'https://stepik.org/lesson/680669/step/1?unit=679339', 'https://stepik.org/lesson/640164/step/1?unit=636683',
         'https://stepik.org/lesson/683127/step/1?unit=681950', 'https://stepik.org/lesson/680264/step/1?unit=678922',
         'https://stepik.org/lesson/690796/step/1?unit=690340', 'https://stepik.org/lesson/684549/step/1?unit=683502',
         'https://stepik.org/lesson/680263/step/1?unit=678921', 'https://stepik.org/lesson/680265/step/1?unit=678923',
         'https://stepik.org/lesson/680266/step/1?unit=678924', 'https://stepik.org/lesson/699083/step/1?unit=698988',
         'https://stepik.org/lesson/568065/step/1?unit=562441', 'https://stepik.org/lesson/568068/step/1?unit=562444')
url = 'https://stepik.org/course/82541'


def enter_the_void():
    """входим в систему"""
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(
        (By.ID, 'ember46'))).click()
    browser.find_element(By.ID, 'id_login_email').send_keys('####')
    browser.find_element(By.ID, 'id_login_password').send_keys('####')
    # browser.find_element(By.CLASS_NAME, 'sign-form__btn').click()
    browser.find_element(By.CSS_SELECTOR, 'button[class="sign-form__btn button_with-loader "]').click()
    time.sleep(10)


path_to_downloads = '/Users/mirnauki/Downloads'
mainfolder = 'Архив Степика'
if not os.path.isdir(path_to_downloads + '/' + mainfolder):
    os.mkdir(path_to_downloads + '/' + mainfolder)

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('user-data-dir=/Users/mirnauki/Library/Application Support/Google/Chrome')
with webdriver.Chrome(options=options) as browser:
    browser.get(url=url)
    # пытаемся ввести логин-пароль. Иногда просит, иногда нет
    try:
        enter_the_void()
    except:
        pass
    # если выскакивает ошибка 404. Пока что не работает, неправильно подобран CLASS_NAME
    try:
        if browser.find_element(By.CLASS_NAME, 'error-page__status').text == 'Страница не найдена':
            print(browser.page_source)
            exit()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    # итерируемся по списку страниц курса
    for page in tqdm(pages[25:]):
        browser.get(url=page)
        print(browser.title)
        #time.sleep(5)
        WebDriverWait(browser, 15).until(expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'rich-text-viewer')))
        # print(browser.page_source)
        # ищем ссылки на задания (вверху страницы таксбар)
        all_pages_of_tasks = [element for element in browser.find_elements(By.XPATH, '//div/a')
                              if element.get_attribute('class') == 'active ember-view m-step-pin__link' or
                              element.get_attribute('class') == 'ember-view m-step-pin__link']
        tasks = [task.get_attribute('href') for task in all_pages_of_tasks if
                 re.search('/step/', task.get_attribute('href'))]
        # print(tasks)
        if tasks:
            themefolder = browser.title.split(' · ')[1].strip()  # заголовок темы
            if not os.path.isdir(path_to_downloads + '/' + mainfolder + '/' + themefolder):
                os.mkdir(path_to_downloads + '/' + mainfolder + '/' + themefolder)

        for number, task in enumerate(tasks, 1):
            # print(task)
            browser.get(url=task)
            # time.sleep(6)
            WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'rich-text-viewer')))
            test_data = [el.get_attribute('href') for el in browser.find_elements(By.XPATH, '//p/a')
                         if re.search('attachments', el.get_attribute('href')) and el.get_attribute('rel')]
            if test_data:
                # print(test_data)
                try:
                    head = browser.find_element(By.XPATH, '//span/h2').text.strip()
                except selenium.common.exceptions.NoSuchElementException:
                    head = 'Задание без заголовка'
                if not os.path.exists(f'{path_to_downloads}/{mainfolder}/{themefolder}/{number} - {head}'):
                    os.mkdir(f'{path_to_downloads}/{mainfolder}/{themefolder}/{number} - {head}')
                for downloadurl in test_data:
                    name_of_downloaded_file = downloadurl.split('/')[-1].strip()
                    path_to_file = f'{path_to_downloads}/{mainfolder}/{themefolder}/{number} - {head}/{name_of_downloaded_file}'
                    browser.get(url=downloadurl)
                    while not os.path.exists(f'{path_to_downloads}/{name_of_downloaded_file}'):
                        time.sleep(1)
                    if os.path.exists(f'{path_to_downloads}/{name_of_downloaded_file}'):
                        # time.sleep(3)  # ждём, пока файл скачается, не могу подобрать явное ожидание
                        # WebDriverWait(browser, 5).until(os.path.exists(path_to_downloads + "/" + zipname))
                        shutil.move(f'{path_to_downloads}/{name_of_downloaded_file}',
                                    path_to_file)
                        if zipfile.is_zipfile(path_to_file):
                            with ZipFile(path_to_file) as file:
                                dir_with_extracted_files = f'{path_to_downloads}/{mainfolder}/{themefolder}/{number} - {head}/{re.sub(".zip$", "", name_of_downloaded_file)}'
                                if not os.path.exists(dir_with_extracted_files):
                                    os.mkdir(dir_with_extracted_files)
                                ZipFile.extractall(file, dir_with_extracted_files)
