import os
import time
import random
import requests
from datetime import datetime
from pytz import timezone
from collections import deque
from getpass import getpass

def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def realistic_typing_simulation(message):
    words = message.split()
    typed_message = ""
    for word in words:
        typed_message += word + " "
        delay = random.uniform(0.3, 0.9)
        time.sleep(delay)
    return typed_message.strip()

def get_unique_user_agent(token_index, token_user_agents, recent_agents, max_recent=3):
    choices = list(set(token_user_agents[token_index]) - set(recent_agents[token_index]))
    if not choices:
        choices = token_user_agents[token_index]
        recent_agents[token_index].clear()
    selected = random.choice(choices)
    recent_agents[token_index].append(selected)
    if len(recent_agents[token_index]) > max_recent:
        recent_agents[token_index].popleft()
    return selected

def colorful_login():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;36m" + "═" * 60)
    print("★ WELCOME TO ".center(60))
    print("★ BRANDED KAMEENA VIKRAM'S PRIVATE MESSENGER GROUP TOOL ★".center(60))
    print("═" * 60 + "\033[0m")

    username = input("\033[1;92mEnter Username: \033[0m")
    password = getpass("\033[1;91mEnter Password: \033[0m")

    if username.strip() == "VIKRAM SHARMA" and password.strip() == "VIKRAM XWD":
        print("\033[1;92m\n[✓] Access Granted. Welcome, TO MULTI CONVO ZONE!\033[0m")
        time.sleep(1)
    else:
        print("\033[1;91m[!] Access Denied! Invalid Credentials.\033[0m")
        time.sleep(2)
        exit()

def send_messages_from_file():
    os.system('cls' if os.name == 'nt' else 'clear')
    start_time = time.time()
    message_count = 0
    india = timezone('Asia/Kolkata')

    rest_durations = [120, 180, 240, 300]
    rest_index = 0

    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/90.0.4430.91 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 Chrome/91.0.4472.164 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
    ]

    tokens = read_file("tokennum.txt")
    speed = int(read_file("time.txt")[0]) if read_file("time.txt") and read_file("time.txt")[0].isdigit() else 5
    vikram_name = "\033[1;93m★『VIKRAM K1NG』★\033[0m"

    token_user_agents = {
        idx: random.sample(user_agents_pool, k=random.randint(3, len(user_agents_pool)))
        for idx in range(len(tokens))
    }
    recent_agents = {idx: deque(maxlen=3) for idx in range(len(tokens))}

    msg_index = 0
    hater_index = 0

    while True:
        convos = read_file("convo.txt")
        haters = read_file("hatersname.txt")
        messages_list = read_file("NP.txt")

        if not convos:
            print("\033[1;91m[!] convo.txt is empty. Add Group UIDs to continue.\033[0m")
            time.sleep(5)
            continue

        for token_index, token in enumerate(tokens):
            if len(convos) > 1:
                print("\n\033[1;33m" + "═" * 60)
                print(f"Token #{token_index + 1} starting next cycle...".center(60))
                print("═" * 60 + "\033[0m\n")

            for convo_index, convo_id in enumerate(convos):
                group_number = convo_index + 1
                group_display = f"\033[1;92mGroup ID #{group_number}: {convo_id}\033[0m"

                if not haters or not messages_list:
                    print("\033[1;91m[!] hatersname.txt or NP.txt is empty or missing!\033[0m")
                    continue

                hater_name = haters[hater_index % len(haters)]
                hater_index += 1

                message = messages_list[msg_index % len(messages_list)]
                msg_index = (msg_index + 1) % len(messages_list)

                selected_agent = get_unique_user_agent(token_index, token_user_agents, recent_agents)

                headers = {
                    "User-Agent": selected_agent,
                    "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "hi-IN,hi;q=0.9"]),
                    "Content-Type": "application/json"
                }

                typed_message = realistic_typing_simulation(f"{hater_name} {message}")
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"

                current_time_ist = datetime.now(india).strftime("%Y-%m-%d %I:%M:%S %p")
                formatted_time = f"\033[1;97mTime (IST): {current_time_ist}\033[0m"

                uptime_seconds = int(time.time() - start_time)
                uptime_formatted = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
                uptime_display = f"\033[1;94mUptime: {uptime_formatted}\033[0m"

                token_display = f"\033[1;93mToken #{token_index + 1}\033[0m"
                hater_colored = f"\033[1;35m{hater_name}\033[0m"
                message_colored = f"\033[1;96m{message}\033[0m"
                colored_message = f"{hater_colored} {message_colored}"

                try:
                    response = requests.post(url, json={"access_token": token, "message": typed_message}, headers=headers)
                    message_count += 1

                    print(f"\n\033[1;41m🚀 FROM BRANDED KAMEENA VIKRAM ☠️\033[0m")
                    print(formatted_time)
                    print(uptime_display)
                    print(group_display)
                    print(token_display)
                    print(f"⚔️━━━ {vikram_name} ━━━⚔️")

                    if response.ok:
                        print(f"\033[1;92m[✔] Sent ({message_count}): {colored_message}\033[0m")
                    else:
                        print(f"\033[1;91m[x] Failed ({message_count}): {colored_message}\033[0m")
                        print(f"Status Code: {response.status_code}, Response: {response.text}")

                    print("  \033[1;97m" + "═" * 60 + "\033[0m")

                except Exception as e:
                    print(f"\033[1;91m[!] Exception occurred: {e}\033[0m")

                if len(convos) > 1:
                    print(f"\033[1;96m[+] Next message in 4 seconds...\033[0m\n")
                    print("  \033[1;97m" + "─" * 50 + "\033[0m")
                    time.sleep(4)

                if message_count % 10 == 0:
                    rest_time = rest_durations[rest_index % len(rest_durations)]
                    print(f"\033[1;33m[!] Taking a break of {rest_time} seconds after {message_count} messages... 😴\033[0m")
                    time.sleep(rest_time)
                    print(f"\033[1;33m[✓] Resumed after {rest_time} seconds rest. 😃\033[0m")
                    rest_index += 1

            delay_used = round(random.uniform(speed, speed + 5), 2)
            print("  \033[1;97m" + "─" * 50 + "\033[0m")
            print(f"\033[1;95m[DELAY] Waiting {delay_used} seconds before next token cycle...\033[0m")
            print("  \033[1;97m" + "─" * 50 + "\033[0m\n")
            time.sleep(delay_used)

if __name__ == "__main__":
    colorful_login()
    send_messages_from_file()
    
