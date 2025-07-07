# main.py

import time
from turtle import clear
import warnings
import random

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from utility import chd_wh, clear_console, word_get, choice_class, choice_set, classcard_api_post
from learning_types import (
    memorization,
    recall,
    spelling,
    test,
    matching_game,
    matching_game_API,
    quiz_battle
)

a = input(
    """
    ---------------------------------------------이용 약관-----------------------------------------------
    이 프로그램은 교육용 목적으로 만들어졌습니다. 절대 실제 수업에서의 사용을 금지합니다. 계속하시겠습니까? (y/n): 
    ----------------------------------------------------------------------------------------------------
    """
    )

if a == "n":
    print("프로그램을 종료합니다.")
    quit()

clear_console()

print(
        """

        -----------------------------------
        Classcard Hack v3.1.0
        -----------------------------------

        Developed by NellLucas(서재형)
        Fixed by SD HS Student

        몇가지 오류 메세지, 로그가 떠도 무시하세요
        작동만 되면 되잖아요 ㅎㅎ

        """
)

time.sleep(2)

print("""
    곧 크롬 창이 하나 뜰겁니다.
    클래스카드 로그인 페이지로 이동합니다.
    로그인 버튼까지 누른 후 이 창으로 돌아와서 엔터를 눌러주세요.
    로그인 후에는 아무것도 건들지 말아주세요.
    프로그램이 자동으로 웹사이트를 조작합니다.

    """)

time.sleep(3)

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    # account = get_id()  # 삭제
    
    time_1 = round(random.uniform(0.7, 1.3), 4)
    time_2 = round(random.uniform(1.7, 2.3), 4)

    # 웹드라이버 초기화
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)

    try:

        # 로그인
        driver.get("https://www.classcard.net/Login")

        input("크롬 창에서 로그인을 완료한 후 엔터를 눌러주세요...")  # 로그인 수동 대기

        class_dict = {}
        class_list_element = driver.find_element(
            By.CSS_SELECTOR,
            "body > div.mw-1080 > div:nth-child(6) > div > div > div.left-menu > div.left-item-group.p-t-none.p-r-lg > div.m-t-sm.left-class-list",
        )
        for class_item, i in zip(
            class_list_element.find_elements(By.TAG_NAME, "a"),
            range(len(class_list_element.find_elements(By.TAG_NAME, "a"))),
        ):
            class_temp = {}
            class_temp["class_name"] = class_item.text
            class_temp["class_id"] = class_item.get_attribute("href").split("/")[-1]
            if class_temp["class_id"] == "joinClass":
                break
            class_dict[i] = class_temp

        if len(class_dict) == 0:
            print("클래스가 없습니다.")
            quit()
        elif len(class_dict) == 1:
            choice_class_val = 0
        else:
            choice_class_val = choice_class(class_dict=class_dict)
        class_id = class_dict[choice_class_val].get("class_id")

        driver.get(f"https://www.classcard.net/ClassMain/{class_id}")
        time.sleep(1)

        sets_div = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div"
        )
        sets = sets_div.find_elements(By.CLASS_NAME, "set-items")
        sets_dict = {}
        for set_item, i in zip(sets, range(len(sets))):
            a_tag = set_item.find_element(By.TAG_NAME, "a")
            set_temp = {}
            set_temp["card_num"] = a_tag.find_element(By.TAG_NAME, "span").text
            set_temp["title"] = a_tag.text.replace(set_temp["card_num"], "")
            set_temp["set_id"] = a_tag.get_attribute("data-idx")
            sets_dict[i] = set_temp

        choice_set_vals = choice_set(sets_dict)
        ch_d_list = chd_wh()  # 여러 개 선택 가능
        for ch_d in ch_d_list:
            for choice_set_val in choice_set_vals:
                set_site = (
                    f"https://www.classcard.net/set/{sets_dict[choice_set_val]['set_id']}/{class_id}"
                )
                driver.get(set_site)
                time.sleep(1)

                user_id = int(driver.execute_script("return c_u;"))

                driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
                ).click()
                driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
                ).click()

                html = BeautifulSoup(driver.page_source, "html.parser")
                cards_ele = html.find("div", class_="flip-body")
                num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1

                time.sleep(0.5)

                word_d = word_get(driver, num_d)
                da_e, da_k, da_kn, da_kyn, da_ked, da_sd, da_e_clean, da_k_clean = word_d

                print(f"\n====== '{sets_dict[choice_set_val]['title']}' 세트 학습 시작 ======\n")

                if ch_d == 1:
                    print("암기학습 API 요청 변조 시작")
                    classcard_api_post(user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, activity=1)
                elif ch_d == 2:
                    print("리콜학습 API 요청 변조 시작")
                    classcard_api_post(user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, activity=2)
                elif ch_d == 3:
                    print("스펠학습 API 요청 변조 시작")
                    classcard_api_post(user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, activity=3)
                elif ch_d == 4:
                    match_site = f"https://www.classcard.net/Match/{sets_dict[choice_set_val]['set_id']}?c={class_id}"
                    driver.get(match_site)
                    matching_game_API.run_matching_game_api(driver, match_site)
                elif ch_d == 5:
                    test.run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1, da_e_clean, da_k_clean)
                elif ch_d == 6:
                    quiz_battle.run_quiz_battle(driver, da_e, da_k, da_sd)
                elif ch_d == 7:
                    memorization.run_memorization(driver, num_d)
                elif ch_d == 8:
                    recall.run_recall(driver, num_d, da_e, da_kyn, time_2)
                elif ch_d == 9:
                    spelling.run_spelling(driver, num_d, da_e, da_k)
                elif ch_d == 10:
                    matching_game.run_matching_game(driver, da_e, da_k)
                else:
                    print("잘못된 학습 유형, 프로그램 종료")
                    break

                print(f"\n====== '{sets_dict[choice_set_val]['title']}' 세트 학습 완료 ======\n")
                time.sleep(1)

        print("\n✅ 모든 선택한 세트 학습이 완료되었습니다.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
