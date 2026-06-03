# learning_types/matching_game.py
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

def run_matching_game(driver, da_e, da_k):
    print("매칭게임을 시작합니다...")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[5]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        "#wrapper-learn > div.start-opt-body > div > div.container-bottom > div > div.btn-blue.btn-opt-start"
                        ).click()
    time.sleep(3.5)
    past_cards = ""
    while True:
        try:
            html = BeautifulSoup(driver.page_source, "html.parser")
            match_body = html.find("div", class_="match-body")
            if not match_body:
                raise NoSuchElementException

            cards = match_body.get_text(strip=True)
            if past_cards == cards:
                time.sleep(0.5)
                continue

            unsorted_cards = {}
            for i in range(4):
                left_card = html.find("div", id=f"left_card_{i}")
                if not left_card:
                    continue
                score_tag = left_card.find("span", class_="card-score")
                score = int(score_tag.get_text(strip=True)) if score_tag else i
                if score_tag:
                    score_tag.decompose()
                question = left_card.get_text(strip=True)
                unsorted_cards[f"{question}_{i}"] = score

            sorted_lists = sorted(unsorted_cards.items(), key=lambda item: item[1])
            matched = False
            for k, _ in sorted_lists:
                word, order = k.split("_")
                if word not in da_e:
                    continue
                answer = da_k[da_e.index(word)]

                for j in range(4):
                    right_card_tag = html.find("div", id=f"right_card_{j}")
                    if not right_card_tag:
                        continue
                    right_card = right_card_tag.get_text(strip=True)
                    if right_card == answer:
                        left_element = driver.find_element(By.ID, f"left_card_{order}")
                        right_element = driver.find_element(By.ID, f"right_card_{j}")
                        try:
                            left_element.click()
                            right_element.click()
                        except ElementClickInterceptedException:
                            action = ActionChains(driver)
                            action.click(on_element=left_element)
                            action.click(on_element=right_element)
                            action.perform()
                            action.reset_actions()
                        matched = True
                        break
                if matched:
                    break

            if matched:
                try:
                    rank_info = driver.find_element(By.CLASS_NAME, "rank-info")
                    if rank_info.size["height"] > 0:
                        print("매칭게임이 완료되었습니다.")
                        driver.find_element(By.CSS_SELECTOR, ".btn-default").click()
                        time.sleep(1)
                        break
                except NoSuchElementException:
                    pass
                past_cards = cards
            else:
                time.sleep(0.5)
        except NoSuchElementException:
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            break
