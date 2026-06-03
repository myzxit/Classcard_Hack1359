# main.py
import argparse
import time
import warnings
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from utility import (
    chd_wh,
    choice_class,
    choice_set,
    classcard_api_post,
    get_config,
    save_config,
    auto_login,
    manual_login,
    get_cookies,
    clear_console,
    word_get,
)
from learning_types import (
    memorization,
    recall,
    spelling,
    test,
    matching_game,
    matching_game_API,
    quiz_battle,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Classcard 자동화를 실행합니다. 로그인 모드와 디바이스 모드를 선택하세요."
    )
    parser.add_argument(
        "--login-mode",
        choices=["auto", "manual"],
        help="로그인 방식: auto(자동 로그인), manual(수동 로그인)",
    )
    parser.add_argument(
        "--device",
        choices=["desktop", "mobile"],
        help="실행 모드: desktop(PC), mobile(핸드폰 에뮬레이션)",
    )
    return parser.parse_args()


def setup_driver(device_mode: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    if device_mode == "mobile":
        options.add_experimental_option(
            "mobileEmulation", {"deviceName": "Pixel 2"}
        )
        options.add_argument("--window-size=412,914")
    else:
        options.add_argument("--window-size=1366,768")
    return webdriver.Chrome(options=options)


def collect_classes(driver):
    class_dict = {}
    anchors = driver.find_elements(
        By.CSS_SELECTOR, "a[href*='/ClassMain/']"
    )
    for index, anchor in enumerate(anchors):
        href = anchor.get_attribute("href") or ""
        if "/ClassMain/" not in href:
            continue
        class_id = href.rstrip("/").split("/")[-1]
        if class_id == "joinClass":
            continue
        class_dict[index] = {
            "class_name": anchor.text.strip() or f"Class {index + 1}",
            "class_id": class_id,
        }
    return class_dict


def collect_sets(driver):
    sets = []
    links = driver.find_elements(By.CSS_SELECTOR, "a[data-idx], .set-items a")
    for link in links:
        set_id = link.get_attribute("data-idx") or ""
        title = link.text.strip()
        card_num = ""
        match = re.search(r"(\d+)\s*개|\d+\s*카드|\d+", title)
        if match:
            card_num = match.group(0).strip()
            title = title.replace(card_num, "").strip()
        if not set_id:
            href = link.get_attribute("href") or ""
            if "/set/" in href:
                set_id = href.rstrip("/").split("/")[-1]
        if set_id:
            sets.append({"title": title or f"Set {len(sets)+1}", "card_num": card_num, "set_id": set_id})
    return sets


def wait_for_cards(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flip-body, div.flip-card"))
        )
    except Exception:
        pass


def get_card_count(driver):
    html = BeautifulSoup(driver.page_source, "html.parser")
    cards_ele = html.find("div", class_="flip-body") or html.find("div", id="tab_set_all")
    if cards_ele:
        flip_cards = cards_ele.find_all("div", class_="flip-card")
        if flip_cards:
            return len(flip_cards) + 1
    all_cards = html.find_all("div", class_="flip-card")
    return len(all_cards) + 1 if all_cards else 0


def login_to_classcard(driver, config):
    if config["login_mode"] == "manual":
        return manual_login(driver)
    return auto_login(driver, config)


def main(args=None):
    config = get_config()
    if args is None:
        args = parse_args()
    if args.login_mode:
        config["login_mode"] = args.login_mode
    if args.device:
        config["device_mode"] = args.device
    save_config(config)
    if config["login_mode"] == "auto" and (not config.get("id") or not config.get("pw")):
        config = get_config()
    time_1 = round(random.uniform(0.7, 1.3), 4)
    time_2 = round(random.uniform(1.7, 2.3), 4)

    driver = setup_driver(config["device_mode"])
    driver.implicitly_wait(10)

    try:
        logged_in = login_to_classcard(driver, config)
        if not logged_in:
            print("로그인에 실패했습니다. 로그인 정보를 확인하거나 수동 로그인 모드를 사용해보세요.")
            return

        class_dict = collect_classes(driver)
        if not class_dict:
            print("클래스 정보를 찾을 수 없습니다. 로그인 후 클래스 목록이 정상적으로 표시되는지 확인해주세요.")
            return

        if len(class_dict) == 1:
            choice_class_val = 0
        else:
            choice_class_val = choice_class(class_dict=class_dict)

        class_id = class_dict[choice_class_val].get("class_id")
        if not class_id:
            print("클래스 ID를 가져오지 못했습니다.")
            return

        driver.get(f"https://www.classcard.net/ClassMain/{class_id}")
        time.sleep(1)

        sets = collect_sets(driver)
        if not sets:
            print("세트 목록을 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
            return

        sets_dict = {i: s for i, s in enumerate(sets)}
        choice_set_val = choice_set(sets_dict)
        selected_set = sets_dict[choice_set_val]

        set_site = f"https://www.classcard.net/set/{selected_set['set_id']}/{class_id}"
        driver.get(set_site)
        time.sleep(1)

        user_id = None
        try:
            user_id = int(driver.execute_script("return c_u;"))
        except Exception:
            pass
        if user_id is None:
            print("사용자 정보를 가져오지 못했습니다. 일부 API 변조 기능이 정상 동작하지 않을 수 있습니다.")

        ch_d = chd_wh()

        try:
            driver.find_element(By.CSS_SELECTOR, "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a").click()
            driver.find_element(By.CSS_SELECTOR, "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)").click()
        except Exception:
            pass

        wait_for_cards(driver)
        num_d = get_card_count(driver)

        word_d = None
        try:
            word_d = __import__("utility").word_get(driver, num_d)
        except Exception as exc:
            print("단어 데이터 수집 중 오류가 발생했습니다:", exc)
            return

        da_e, da_k, da_kn, da_kyn, da_ked, da_sd = word_d

        if ch_d == 1:
            print("암기학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=selected_set["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=1,
                cookies=get_cookies(driver),
            )
        elif ch_d == 2:
            print("리콜학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=selected_set["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=2,
                cookies=get_cookies(driver),
            )
        elif ch_d == 3:
            print("스펠학습 API 요청 변조를 시작합니다.")
            classcard_api_post(
                user_id=user_id,
                set_id=selected_set["set_id"],
                class_id=class_id,
                view_cnt=num_d,
                activity=3,
                cookies=get_cookies(driver),
            )
        elif ch_d == 4:
            match_site = f"https://www.classcard.net/Match/{selected_set['set_id']}?c={class_id}"
            driver.get(match_site)
            matching_game_API.run_matching_game_api(driver, match_site)
        elif ch_d == 5:
            test.run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1)
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
            print("프로그램을 종료합니다.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
