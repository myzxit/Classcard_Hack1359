# utility.py
import time
import json
import re
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
    "login_mode": "auto",
    "device_mode": "desktop",
    "id": "",
    "pw": "",
}


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def load_config() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            if not isinstance(config, dict):
                return DEFAULT_CONFIG.copy()
            return {**DEFAULT_CONFIG, **config}
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def prompt_login_mode() -> str:
    print("\n로그인 모드를 선택해주세요.")
    print("[1] 자동 로그인 (저장된 계정 사용)")
    print("[2] 수동 로그인 (브라우저에서 직접 로그인)")
    while True:
        try:
            choice = int(input(">>> "))
            if choice == 1:
                return "auto"
            if choice == 2:
                return "manual"
            raise ValueError
        except ValueError:
            print("1 또는 2 중 하나를 선택해주세요.")
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            quit()


def prompt_device_mode() -> str:
    print("\n실행 모드를 선택해주세요.")
    print("[1] 컴퓨터용 (Desktop)")
    print("[2] 핸드폰용 (Mobile 에뮬레이션)")
    while True:
        try:
            choice = int(input(">>> "))
            if choice == 1:
                return "desktop"
            if choice == 2:
                return "mobile"
            raise ValueError
        except ValueError:
            print("1 또는 2 중 하나를 선택해주세요.")
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            quit()


def check_id(id, pw) -> bool:
    print("계정 정보를 확인하고 있습니다... 잠시만 기다리세요!!")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"login_id": id, "login_pwd": pw}
    try:
        res = requests.post(
            "https://www.classcard.net/LoginProc",
            headers=headers,
            data=data,
            timeout=15,
        )
        res.raise_for_status()
        status = res.json()
        return status.get("result") == "ok"
    except (requests.RequestException, ValueError):
        return False


def save_credentials(config: dict) -> dict:
    while True:
        id_value = input("아이디를 입력하세요 : ").strip()
        password = input("비밀번호를 입력하세요 : ").strip()
        if check_id(id_value, password):
            config["id"] = id_value
            config["pw"] = password
            save_config(config)
            print("아이디와 비밀번호가 저장되었습니다.\n")
            return config
        print("아이디 또는 비밀번호가 잘못되었습니다. 다시 시도해주세요.\n")


def get_config() -> dict:
    config = load_config()
    if config.get("login_mode") not in ("auto", "manual"):
        config["login_mode"] = prompt_login_mode()
    if config.get("device_mode") not in ("desktop", "mobile"):
        config["device_mode"] = prompt_device_mode()
    if config["login_mode"] == "auto" and (not config.get("id") or not config.get("pw")):
        config = save_credentials(config)
    save_config(config)
    return config


def save_id() -> dict:
    return save_credentials(load_config())


def get_id():
    config = load_config()
    return {"id": config.get("id", ""), "pw": config.get("pw", "")}


def auto_login(driver, config: dict) -> bool:
    if not config.get("id") or not config.get("pw"):
        config = save_credentials(config)
    driver.get("https://www.classcard.net/Login")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login_id"))
        )
        driver.find_element(By.NAME, "login_id").clear()
        driver.find_element(By.NAME, "login_id").send_keys(config["id"])
        driver.find_element(By.NAME, "login_pwd").send_keys(config["pw"])

        submit = None
        try:
            submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        except NoSuchElementException:
            pass
        if submit:
            driver.execute_script("arguments[0].click();", submit)
        else:
            driver.find_element(By.ID, "loginForm").submit()

        WebDriverWait(driver, 30).until(lambda d: "/Login" not in d.current_url and not d.find_elements(By.NAME, "login_id"))
        return True
    except (TimeoutException, NoSuchElementException):
        return False


def manual_login(driver) -> bool:
    driver.get("https://www.classcard.net/Login")
    print("\n수동 로그인 모드가 선택되었습니다.")
    print("브라우저가 열리면 이메일과 비밀번호를 입력하고 로그인 버튼을 눌러주세요.")
    print("로그인이 완료되면 자동으로 다음 단계로 넘어갑니다. (최대 5분 대기)")
    try:
        WebDriverWait(driver, 300).until(lambda d: "/Login" not in d.current_url and not d.find_elements(By.NAME, "login_id"))
        return True
    except TimeoutException:
        return False


def get_cookies(driver) -> str:
    return "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])


def classcard_api_post(
    user_id: int,
    set_id: int,
    class_id: int,
    view_cnt: int,
    activity: int,
    cookies: str = None,
) -> None:
    url = "https://www.classcard.net/ViewSetAsync/resetAllLog"
    payload = f"set_idx={set_id}&activity={activity}&user_idx={user_id}&view_cnt={view_cnt}&class_idx={class_id}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.classcard.net",
        "Referer": f"https://www.classcard.net/set/{set_id}/{class_id}",
    }
    if cookies:
        headers["Cookie"] = cookies
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=20)
        response.raise_for_status()
        print("API 요청 변조에 성공하였습니다!")
    except requests.RequestException as exc:
        print("API 요청 중 오류가 발생했습니다:", exc)


def word_get(driver, num_d) -> list:
    da_e, da_k, da_kn, da_kyn, da_ked, da_sd = [[""] * num_d for _ in range(6)]

    for i in range(1, num_d):
        da_e[i] = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[1]/div/div"
        ).text
    
    try:
        for i in range(1, num_d):
            url = driver.find_element(By.XPATH, f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[1]/div[3]/a").get_attribute('data-src')
            lv = [part for part in url.split("/") if part]
            upload_index = next((index for index, part in enumerate(lv) if "uploads" in part), None)
            if upload_index is not None:
                lv = lv[upload_index:]
            da_sd[i] = "/" + "/".join(lv)
    except NoSuchElementException:
        pass

    driver.find_element(By.CSS_SELECTOR,
        "#tab_set_all > div.card-list-title > div > div:nth-child(1) > a"
    ).click()
    time.sleep(0.5)
    
    for i in range(1, num_d):
        ko_d = driver.find_element(By.XPATH,
            f"//*[@id='tab_set_all']/div[2]/div[{i}]/div[4]/div[2]/div[1]/div/div"
        ).text
        ko_d = ko_d.split("\n")
        
        POS_MARKERS = ['명', '동', '형', '부']
        pattern = r'\b(?:' + '|'.join(POS_MARKERS) + r')\.\s*'
        edit_ko_d = [re.sub(pattern, '', line) for line in ko_d]

        if len(ko_d) == 1:
            da_k[i] = ko_d[0]
            da_kn[i] = ko_d[0]
            da_kyn[i] = ko_d[0]
            da_ked[i] = edit_ko_d[0]
        else:
            da_k[i] = "\n".join(ko_d)
            da_kn[i] = ", ".join(ko_d)
            da_kyn[i] = " ".join(ko_d)
            da_ked[i] = ", ".join(edit_ko_d)

    return [da_e, da_k, da_kn, da_kyn, da_ked, da_sd]


def chd_wh() -> int:
    print(
        """
학습 유형을 선택해주세요!!
[1] 암기학습(API 요청 변조)
[2] 리콜학습(API 요청 변조)
[3] 스펠학습(API 요청 변조)
[4] 매칭게임(API 요청 변조)
[5] 테스트학습(매크로)
[6] QuizBattle(매크로)
[7] 암기학습(매크로)
[8] 리콜학습(매크로)
[9] 스펠학습(매크로)
[10] 매칭게임(매크로)
---------------------------
Developed by NellLucas(서재형)
        """
    )
    while True:
        try:
            ch_d = int(input(">>> "))
            if 1 <= ch_d <= 10:
                break
            else:
                raise ValueError
        except ValueError:
            print("올바른 학습 유형(1~10)을 선택해주세요.")
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            quit()
    return ch_d


def choice_set(sets: dict) -> int:
    clear_console()
    print("학습할 세트를 선택해주세요.")
    print("Ctrl + C 를 눌러 종료")
    for set_item in sets:
        print(
            f"[{set_item+1}] {sets[set_item].get('title')} | {sets[set_item].get('card_num')}"
        )
    while True:
        try:
            ch_s = int(input(">>> "))
            if ch_s >= 1 and ch_s <= len(sets):
                break
            else:
                raise ValueError
        except ValueError:
            print("세트를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()
    clear_console()
    print(f"{sets[ch_s-1].get('title')}를 선택하셨습니다.")
    return ch_s - 1


def choice_class(class_dict: dict) -> int:
    clear_console()
    print("학습할 클래스를 선택해주세요.")
    print("Ctrl + C 를 눌러 종료")
    for class_item in class_dict:
        print(f"[{class_item+1}] {class_dict[class_item].get('class_name')}")
    while True:
        try:
            ch_c = int(input(">>> "))
            if ch_c >= 1 and ch_c <= len(class_dict):
                break
            else:
                raise ValueError
        except ValueError:
            print("클래스를 다시 입력해주세요.")
        except KeyboardInterrupt:
            quit()
    clear_console()
    print(f"{class_dict[ch_c-1].get('class_name')}를 선택하셨습니다.")
    return ch_c - 1


