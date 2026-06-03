# learning_types/recall.py
import time
from selenium.webdriver.common.by import By
import random

def run_recall(driver, num_d, da_e, da_kyn, time_2):
    print("리콜학습을 시작합니다...")
    try:
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a").click()
    except NoSuchElementException:
        print("리콜학습 시작 요소를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
        return

    time.sleep(time_2)
    for i in range(1, num_d):
        try:
            cash_d = driver.find_element(By.XPATH,
                                         f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[1]/div/div/div/div[1]/span"
                                         ).text

            cash_dby = []
            for j in range(0, 3):
                cash_dby.append(driver.find_element(By.XPATH,
                                                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j + 1}]/div[2]/div"
                                                    ).text)

            selected = False
            if cash_d.upper() != cash_d.lower():
                for j, answer in enumerate(cash_dby):
                    try:
                        if da_e.index(cash_d) == da_kyn.index(answer):
                            driver.find_element(By.XPATH,
                                                f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{j + 1}]/div[2]"
                                                ).click()
                            selected = True
                            break
                    except ValueError:
                        continue
            if not selected:
                print("\n데이터를 찾지 못했습니다. 랜덤 선택을 시도합니다.\n")
                option_index = min(len(cash_dby), 4)
                if option_index == 0:
                    raise NoSuchElementException
                driver.find_element(By.XPATH,
                                    f"//*[@id='wrapper-learn']/div/div/div[2]/div[2]/div[{i}]/div[3]/div[{random.randint(1, option_index)}]/div[2]"
                                    ).click()
                time.sleep(time_2)
                try:
                    driver.find_element(By.XPATH,
                                        f"//*[@id='wrapper-learn']/div/div/div[3]/div[2]"
                                        ).click()
                except NoSuchElementException:
                    pass
            time.sleep(time_2)
        except NoSuchElementException:
            print("리콜학습 진행 중 오류가 발생했습니다. 리콜학습을 종료합니다.")
            try:
                driver.find_element(By.XPATH,
                                    "/html/body/div[1]/div/div[1]/div[1]"
                                    ).click()
                time.sleep(1)
                driver.find_element(By.XPATH,
                                    "//*[@id='wrapper-learn']/div[2]/div/div/div/div[5]/a[3]"
                                    ).click()
            except NoSuchElementException:
                pass
            break
    print("리콜학습이 완료되었습니다.")
