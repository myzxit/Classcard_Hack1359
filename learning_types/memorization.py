# learning_types/memorization.py
import time
from selenium.webdriver.common.by import By

def run_memorization(driver, num_d):
    print("암기학습을 시작합니다...")
    try:
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a").click()
    except NoSuchElementException:
        print("암기학습 초기화 요소를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
        return

    for i in range(1, num_d):
        time.sleep(2.5)
        try:
            driver.find_element(By.CSS_SELECTOR,
                                "#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box"
                                ).click()
            time.sleep(0.5)
            driver.find_element(By.CSS_SELECTOR,
                                "#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box"
                                ).click()
        except NoSuchElementException:
            print("암기할 카드가 더 이상 존재하지 않거나 버튼 위치가 변경되었습니다.")
            break
    time.sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR,
                            "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a"
                            ).click()
    except NoSuchElementException:
        pass
    print("암기학습 프로세스를 종료했습니다.")
