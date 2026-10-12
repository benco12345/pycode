import sys
import msvcrt
import site
import time
import json
import os
import webbrowser
import urllib.request

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[34m"

# שומר את קובץ ההגדרות תמיד בתיקייה שבה נמצא הסקריפט (מושלם לדיסק-און-קי)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "chatbot_config.json")

def load_config():
    """טוען את ההגדרות מה-JSON אם הן קיימות, אחרת מחזיר ברירות מחדל"""
    default_prompt = f"{RED} >>> {RESET}"
    default_error_msg = f"{RED}{BOLD} [ERROR] {RESET}{RED}sorry but i dont know what you really are talking about \n [PYTHON] you said '{{user_input}}' so itll not a command{RESET}"
    default_clicker_data = {
        "score": 0,
        "click_power": 1,
        "upgrade_cost": 10,
        "auto_power": 0,
        "auto_cost": 50,
        "multiplier_level": 1,
        "mult_cost": 100,
        "custom_setting": "default_value",
        "set_cost": 250,
        "ab1_unlocked": False,
        "ab1_cost": 200,
        "ab1_cooldown": 30, # seconds
        "ab1_cd_cost": 150,
        "ab2_unlocked": False,
        "ab2_cost": 1000,
        "ab2_cooldown": 60,
        "ab2_cd_cost": 500,
        "ab3_unlocked": False,
        "ab3_cost": 5000,
        "ab3_cooldown": 120,
        "ab3_cd_cost": 1500,
        "last_ab1_use": 0,
        "last_ab2_use": 0,
        "last_ab3_use": 0
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return (
                    data.get("prompt", default_prompt), 
                    data.get("error_msg", default_error_msg),
                    data.get("clicker_data", default_clicker_data)
                )
        except Exception:
            pass
    return default_prompt, default_error_msg, default_clicker_data

def save_config(prompt, error_msg, clicker_data):
    """שומר את ההגדרות והקליקר לקובץ JSON בנתיב המדויק"""
    data = {
        "prompt": prompt,
        "error_msg": error_msg,
        "clicker_data": clicker_data
    }
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def run_chatbot():
    print(f"{GREEN}Command mod has been activated! type 'help' to view the commands{RESET}")
    
    # טעינת ההגדרות הראשונית
    input_input, custom_error_msg, clicker_data = load_config()
    default_error_msg = f"{RED}{BOLD} [ERROR] {RESET}{RED}sorry but i dont know what you really are talking about \n [PYTHON] you said '{{user_input}}' so itll not a command{RESET}"
    
    while True:
        try:
            user_input = input(input_input).strip().lower()
            
            if not user_input:
                continue

            if user_input in ["go to sleep", "..."]:
                print(f"{GREEN}Good night!{RESET}")

            elif user_input == 'im him':
                print(f"{RED}HOW DID YOU DID IT???{RESET}")
                sub_input = input(input_input).strip().lower()
                
                if sub_input == "im really him":
                    print(f"{GREEN}W man{RESET}")
                elif sub_input == "i just typed it":
                    print(f"{YELLOW} oh so idc man{RESET}")
                else:
                    print(f"{RED} this is not a valid answer, sorry but there are only two valid answers.{RESET}")
            
            # --- CLICKER MODE ---
            elif user_input == "clicker":
                print(f"{GREEN}Welcome to Clicker Mode! Press ENTER to score, type 'upgrades' for shop, 'ab' for abilities, or 'exitc' to leave.{RESET}")
                clicker_prompt = f"{YELLOW}<<> {RESET}"
                
                while True:
                    click_input = input(clicker_prompt).strip().lower()
                    
                    if click_input == "exitc":
                        save_config(input_input, custom_error_msg, clicker_data)
                        print(f"{GREEN}Exiting Clicker Mode... Progress saved! Final score was {clicker_data['score']}{RESET}")
                        break
                        
                    elif click_input in ["1", ""]:  
                        earned = clicker_data["click_power"] * clicker_data["multiplier_level"]
                        clicker_data["score"] += earned
                        print(f"{GREEN}Score: {clicker_data['score']} (+{earned}){RESET}")
                        
                    elif click_input == "upgrades":
                        print(f"{BLUE}--- UPGRADES SHOP ---\n"
                              f"1. Better Clicks (Cost: {clicker_data['upgrade_cost']} | You have: {clicker_data['score']} | Need: {max(0, clicker_data['upgrade_cost'] - clicker_data['score'])})\n"
                              f"2. Auto Clicker (Cost: {clicker_data['auto_cost']} | You have: {clicker_data['score']} | Need: {max(0, clicker_data['auto_cost'] - clicker_data['score'])})\n"
                              f"3. Score Multiplier (Cost: {clicker_data['mult_cost']} | You have: {clicker_data['score']} | Need: {max(0, clicker_data['mult_cost'] - clicker_data['score'])})\n"
                              f"Type 'buy 1', 'buy 2', or 'buy 3' to purchase once, or add 'max' (e.g. 'buy 1 max'){RESET}")
                            
                    elif click_input == "ab":
                        ab1_status = "Unlocked" if clicker_data["ab1_unlocked"] else f"Cost: {clicker_data['ab1_cost']}"
                        ab2_status = "Unlocked" if clicker_data["ab2_unlocked"] else f"Cost: {clicker_data['ab2_cost']}"
                        ab3_status = "Unlocked" if clicker_data["ab3_unlocked"] else f"Cost: {clicker_data['ab3_cost']}"
                        print(f"{BLUE}--- ABILITIES SHOP & MENU ---\n"
                              f"ab 1 [Clicks 10x]: {ab1_status} | Cooldown: {clicker_data['ab1_cooldown']}s (Upgrade CD: 'up ab 1', Cost: {clicker_data['ab1_cd_cost']})\n"
                              f"ab 2 [OP 1.5X Boost]: {ab2_status} | Cooldown: {clicker_data['ab2_cooldown']}s (Upgrade CD: 'up ab 2', Cost: {clicker_data['ab2_cd_cost']})\n"
                              f"ab 3 [Ultra 3X Boost]: {ab3_status} | Cooldown: {clicker_data['ab3_cooldown']}s (Upgrade CD: 'up ab 3', Cost: {clicker_data['ab3_cd_cost']})\n"
                              f"Type 'buy ab 1', 'buy ab 2', 'buy ab 3' to unlock, or type 'ab 1', 'ab 2', 'ab 3' to use!{RESET}")

                    elif click_input == "set":
                        print(f"{BLUE}Current custom setting: {clicker_data['custom_setting']}{RESET}")
                        print(f"{BLUE}Changing custom setting costs {clicker_data['set_cost']} score. (You have: {clicker_data['score']}){RESET}")
                        new_set_val = input(f"{GREEN}Enter new setting value > {RESET}").strip()
                        if new_set_val:
                            if clicker_data["score"] >= clicker_data["set_cost"]:
                                clicker_data["score"] -= clicker_data["set_cost"]
                                clicker_data["custom_setting"] = new_set_val
                                clicker_data["set_cost"] = int(clicker_data["set_cost"] * 1.5)
                                print(f"{GREEN}Setting updated! Current score: {clicker_data['score']}. Next change cost: {clicker_data['set_cost']}{RESET}")
                            else:
                                need = clicker_data['set_cost'] - clicker_data['score']
                                print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score.{RESET}")
                        else:
                            print(f"{RED}Setting cannot be empty.{RESET}")

                    # --- BUY ABILITIES ---
                    elif click_input == "buy ab 1":
                        if clicker_data["ab1_unlocked"]:
                            print(f"{YELLOW}You already unlocked Ability 1!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab1_cost"]:
                            clicker_data["score"] -= clicker_data["ab1_cost"]
                            clicker_data["ab1_unlocked"] = True
                            print(f"{GREEN}Ability 1 unlocked! Current score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab1_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['ab1_cost']}).{RESET}")

                    elif click_input == "buy ab 2":
                        if clicker_data["ab2_unlocked"]:
                            print(f"{YELLOW}You already unlocked Ability 2!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab2_cost"]:
                            clicker_data["score"] -= clicker_data["ab2_cost"]
                            clicker_data["ab2_unlocked"] = True
                            print(f"{GREEN}Ability 2 unlocked! Current score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab2_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['ab2_cost']}).{RESET}")

                    elif click_input == "buy ab 3":
                        if clicker_data["ab3_unlocked"]:
                            print(f"{YELLOW}You already unlocked Ability 3!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab3_cost"]:
                            clicker_data["score"] -= clicker_data["ab3_cost"]
                            clicker_data["ab3_unlocked"] = True
                            print(f"{GREEN}Ability 3 unlocked! Current score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab3_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['ab3_cost']}).{RESET}")

                    # --- UPGRADE ABILITY COOLDOWNS ---
                    elif click_input == "up ab 1":
                        if not clicker_data["ab1_unlocked"]:
                            print(f"{RED}Unlock Ability 1 first!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab1_cd_cost"]:
                            clicker_data["score"] -= clicker_data["ab1_cd_cost"]
                            clicker_data["ab1_cooldown"] = max(2, clicker_data["ab1_cooldown"] - 3)
                            clicker_data["ab1_cd_cost"] = int(clicker_data["ab1_cd_cost"] * 1.5)
                            print(f"{GREEN}Ab 1 Cooldown reduced! New CD: {clicker_data['ab1_cooldown']}s. Score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab1_cd_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    elif click_input == "up ab 2":
                        if not clicker_data["ab2_unlocked"]:
                            print(f"{RED}Unlock Ability 2 first!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab2_cd_cost"]:
                            clicker_data["score"] -= clicker_data["ab2_cd_cost"]
                            clicker_data["ab2_cooldown"] = max(5, clicker_data["ab2_cooldown"] - 5)
                            clicker_data["ab2_cd_cost"] = int(clicker_data["ab2_cd_cost"] * 1.6)
                            print(f"{GREEN}Ab 2 Cooldown reduced! New CD: {clicker_data['ab2_cooldown']}s. Score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab2_cd_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    elif click_input == "up ab 3":
                        if not clicker_data["ab3_unlocked"]:
                            print(f"{RED}Unlock Ability 3 first!{RESET}")
                        elif clicker_data["score"] >= clicker_data["ab3_cd_cost"]:
                            clicker_data["score"] -= clicker_data["ab3_cd_cost"]
                            clicker_data["ab3_cooldown"] = max(10, clicker_data["ab3_cooldown"] - 10)
                            clicker_data["ab3_cd_cost"] = int(clicker_data["ab3_cd_cost"] * 1.8)
                            print(f"{GREEN}Ab 3 Cooldown reduced! New CD: {clicker_data['ab3_cooldown']}s. Score: {clicker_data['score']}{RESET}")
                        else:
                            need = clicker_data["ab3_cd_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    # --- USE ABILITIES ---
                    elif click_input == "ab 1":
                        if not clicker_data["ab1_unlocked"]:
                            print(f"{RED}Ability 1 is locked! Type 'ab' to view shop.{RESET}")
                            continue
                        current_time = time.time()
                        elapsed = current_time - clicker_data["last_ab1_use"]
                        if elapsed < clicker_data["ab1_cooldown"]:
                            remaining = int(clicker_data["ab1_cooldown"] - elapsed)
                            print(f"{RED}Ability 1 is on cooldown! Wait {remaining} seconds.{RESET}")
                        else:
                            clicker_data["last_ab1_use"] = current_time
                            gained = (clicker_data["click_power"] * clicker_data["multiplier_level"]) * 10
                            clicker_data["score"] += gained
                            print(f"{BLUE}[ABILITY 1 ACTIVATED] Clicked 10x instantly! Gained +{gained} score. Total: {clicker_data['score']}{RESET}")

                    elif click_input == "ab 2":
                        if not clicker_data["ab2_unlocked"]:
                            print(f"{RED}Ability 2 is locked! Type 'ab' to view shop.{RESET}")
                            continue
                        current_time = time.time()
                        elapsed = current_time - clicker_data["last_ab2_use"]
                        if elapsed < clicker_data["ab2_cooldown"]:
                            remaining = int(clicker_data["ab2_cooldown"] - elapsed)
                            print(f"{RED}Ability 2 is on cooldown! Wait {remaining} seconds.{RESET}")
                        else:
                            clicker_data["last_ab2_use"] = current_time
                            added = int(clicker_data["score"] * 0.5) 
                            clicker_data["score"] += added
                            print(f"{BLUE}[ABILITY 2 ACTIVATED - OP BOOST] Added +50% score boost (+{added})! Total: {clicker_data['score']}{RESET}")

                    elif click_input == "ab 3":
                        if not clicker_data["ab3_unlocked"]:
                            print(f"{RED}Ability 3 is locked! Type 'ab' to view shop.{RESET}")
                            continue
                        current_time = time.time()
                        elapsed = current_time - clicker_data["last_ab3_use"]
                        if elapsed < clicker_data["ab3_cooldown"]:
                            remaining = int(clicker_data["ab3_cooldown"] - elapsed)
                            print(f"{RED}Ability 3 is on cooldown! Wait {remaining} seconds.{RESET}")
                        else:
                            clicker_data["last_ab3_use"] = current_time
                            added = clicker_data["score"] * 2 
                            clicker_data["score"] += added
                            print(f"{BLUE}[ULTRA ABILITY 3 ACTIVATED] Tripled your score! Added +{added}. Total: {clicker_data['score']}{RESET}")

                    # --- BUY UPGRADE 1 ---
                    elif click_input == "buy 1":
                        if clicker_data["score"] >= clicker_data["upgrade_cost"]:
                            clicker_data["score"] -= clicker_data["upgrade_cost"]
                            clicker_data["click_power"] += 1
                            clicker_data["upgrade_cost"] = int(clicker_data["upgrade_cost"] * 1.5)
                            print(f"{GREEN}Upgrade 1 purchased! Power: {clicker_data['click_power']} | Score: {clicker_data['score']} | Next cost: {clicker_data['upgrade_cost']}{RESET}")
                        else:
                            need = clicker_data["upgrade_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['upgrade_cost']}).{RESET}")
                            
                    elif click_input == "buy 1 max":
                        bought_count = 0
                        while clicker_data["score"] >= clicker_data["upgrade_cost"]:
                            clicker_data["score"] -= clicker_data["upgrade_cost"]
                            clicker_data["click_power"] += 1
                            clicker_data["upgrade_cost"] = int(clicker_data["upgrade_cost"] * 1.5)
                            bought_count += 1
                        if bought_count > 0:
                            print(f"{GREEN}Max bought! Purchased {bought_count}x. Click power: {clicker_data['click_power']} | Score: {clicker_data['score']} | Next cost: {clicker_data['upgrade_cost']}{RESET}")
                        else:
                            need = clicker_data["upgrade_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score to buy even one! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    # --- BUY UPGRADE 2 ---
                    elif click_input == "buy 2":
                        if clicker_data["score"] >= clicker_data["auto_cost"]:
                            clicker_data["score"] -= clicker_data["auto_cost"]
                            clicker_data["auto_power"] += 1
                            clicker_data["auto_cost"] = int(clicker_data["auto_cost"] * 1.6)
                            print(f"{GREEN}Upgrade 2 purchased! Auto power: {clicker_data['auto_power']} | Score: {clicker_data['score']} | Next cost: {clicker_data['auto_cost']}{RESET}")
                        else:
                            need = clicker_data["auto_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['auto_cost']}).{RESET}")
                            
                    elif click_input == "buy 2 max":
                        bought_count = 0
                        while clicker_data["score"] >= clicker_data["auto_cost"]:
                            clicker_data["score"] -= clicker_data["auto_cost"]
                            clicker_data["auto_power"] += 1
                            clicker_data["auto_cost"] = int(clicker_data["auto_cost"] * 1.6)
                            bought_count += 1
                        if bought_count > 0:
                            print(f"{GREEN}Max bought! Purchased {bought_count}x. Auto power: {clicker_data['auto_power']} | Score: {clicker_data['score']} | Next cost: {clicker_data['auto_cost']}{RESET}")
                        else:
                            need = clicker_data["auto_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score to buy even one! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    # --- BUY UPGRADE 3 ---
                    elif click_input == "buy 3":
                        if clicker_data["score"] >= clicker_data["mult_cost"]:
                            clicker_data["score"] -= clicker_data["mult_cost"]
                            clicker_data["multiplier_level"] += 1
                            clicker_data["mult_cost"] = int(clicker_data["mult_cost"] * 2.0)
                            print(f"{GREEN}Upgrade 3 purchased! Multiplier: x{clicker_data['multiplier_level']} | Score: {clicker_data['score']} | Next cost: {clicker_data['mult_cost']}{RESET}")
                        else:
                            need = clicker_data["mult_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score! You have {clicker_data['score']}, you need {need} more score (Cost: {clicker_data['mult_cost']}).{RESET}")
                            
                    elif click_input == "buy 3 max":
                        bought_count = 0
                        while clicker_data["score"] >= clicker_data["mult_cost"]:
                            clicker_data["score"] -= clicker_data["mult_cost"]
                            clicker_data["multiplier_level"] += 1
                            clicker_data["mult_cost"] = int(clicker_data["mult_cost"] * 2.0)
                            bought_count += 1
                        if bought_count > 0:
                            print(f"{GREEN}Max bought! Purchased {bought_count}x. Multiplier: x{clicker_data['multiplier_level']} | Score: {clicker_data['score']} | Next cost: {clicker_data['mult_cost']}{RESET}")
                        else:
                            need = clicker_data["mult_cost"] - clicker_data["score"]
                            print(f"{RED}Not enough score to buy even one! You have {clicker_data['score']}, you need {need} more score.{RESET}")

                    else:
                        print(f"{RED}Invalid clicker command. Press ENTER to score, type 'upgrades', 'ab', 'set', or 'exitc'.{RESET}")
                    
                    save_config(input_input, custom_error_msg, clicker_data)
            # ------------------------
            
            elif user_input in ["run code", "exec"]:
                print(f"{BLUE}Enter your Python code line by line. Type 'end' to finish, or type 'kill123' to cancel:{RESET}")
                code_lines = []
                cancelled = False
                
                while True:
                    line = input(f"{GREEN}{RESET}")
                    if line.strip().lower() == "kill123":
                        print(f"{YELLOW}The code is killed! Now returning to the Original code...{RESET}")
                        cancelled = True
                        break
                    if line.strip().lower() == "end":
                        break
                    code_lines.append(line)
                
                if not cancelled:
                    full_code = "\n".join(code_lines)
                    try:
                        exec(full_code)
                        print(f"{GREEN}Code ended, and SUCCESSFULLY RUNNED{RESET}")
                    except Exception as e:
                        print(f"{RED}[ERROR] An error occurred while running your code: {e}{RESET}")

            elif user_input in ["ip", "what is my ip"]:
                print(f"{GREEN}hmmm finding it...{RESET}")
                try:
                    public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf-8')
                    print(f"{BLUE}Your IP address is {GREEN}{public_ip}{RESET}")
                except Exception:
                    print(f"{RED}{BOLD}[ERROR]{RESET}{RED} We didnt find your IP. Check WIFI and if it still not working there are a thing blocking us to go to the ONLINE.{RESET}")
            
            elif user_input in ["run site", "open site", "site"]:
                print(f"{BLUE}What browser domain would you like to open? (e.g. google.com){RESET}")
                domain = input(f"{GREEN}domain > {RESET}").strip()
                if domain:
                    if not domain.startswith("http://") and not domain.startswith("https://"):
                        url = "https://" + domain
                    else:
                        url = domain
                    webbrowser.open(url)
                    print(f"{GREEN}Success! Opening {url} in your browser.{RESET}")
                else:
                    print(f"{RED}Domain cannot be empty!{RESET}")

            elif user_input in ["reread", "reload"]:
                input_input, custom_error_msg, clicker_data = load_config()
                print(f"{GREEN}Success! Config and Clicker data reloaded from {CONFIG_FILE}.{RESET}")
            
            elif user_input in ["key", "c d"]:
                print(f"{BLUE}We are un-connecting your keyboard to the on screen keyboard to be opened... \n note: this is just a joke.")
                time.sleep(2)
                os.system("start osk")
                print(f"{GREEN}DELIVERY! \n Your un-connected keyboard has been opened{RESET}")
            
            elif user_input in ["cmd prompt", "cd"]:
                print(f"{RED}We are preparing to start Command Prompt for you...{RESET}")
                time.sleep(1)
                print(f"{GREEN}We are running the cmd prompt...{RESET}")
                os.system("start cmd")

            elif user_input in ["change input", "change"]:
                print(f"{BLUE}Enter new prompt. Use \\n for newline, colors like {{red}}, {{green}}, and [{{reset}}] to reset:{RESET}")
                new_prompt = input(f"{GREEN}new prompt > {RESET}")
                if new_prompt.strip() == "[{reset}]":
                    input_input = f"{RED} >>> {RESET}"
                    print(f"{GREEN}Prompt reset to default.{RESET}")
                else:
                    new_prompt = (new_prompt
                                  .replace("\\n", "\n")
                                  .replace("{red}", RED)
                                  .replace("{green}", GREEN)
                                  .replace("{yellow}", YELLOW)
                                  .replace("{blue}", BLUE)
                                  .replace("{bold}", BOLD)
                                  .replace("{reset}", RESET))
                    input_input = new_prompt
                    print(f"{GREEN}Success! Input prompt updated.{RESET}")
                save_config(input_input, custom_error_msg, clicker_data)

            elif user_input in ["change error", "error msg"]:
                print(f"{BLUE}Enter new error message. Use \\n, colors, and type [{{reset}}] to reset:{RESET}")
                new_err = input(f"{GREEN}new error > {RESET}")
                if new_err.strip() == "[{reset}]":
                    custom_error_msg = default_error_msg
                    print(f"{GREEN}Error message reset to default.{RESET}")
                else:
                    new_err = (new_err
                               .replace("\\n", "\n")
                               .replace("{red}", RED)
                               .replace("{green}", GREEN)
                               .replace("{yellow}", YELLOW)
                               .replace("{blue}", BLUE)
                               .replace("{bold}", BOLD)
                               .replace("{reset}", RESET))
                    custom_error_msg = new_err
                    print(f"{GREEN}Success! Error message updated.{RESET}")
                save_config(input_input, custom_error_msg, clicker_data)

            elif user_input in ["all commands", "list commands"]:
                print(f"{GREEN}{BOLD}All Available Commands (Secret one is hidden!):{RESET}\n"
                      f" - help / 1\n"
                      f" - how do i get out / 2\n"
                      f" - clicker (Opens clicker game mode)\n"
                      f" - change input / change\n"
                      f" - change error / error msg\n"
                      f" - reread / reload\n"
                      f" - run site / site\n"
                      f" - run code / exec\n"
                      f" - ip / what is my ip\n"
                      f" - cmd prompt / cd\n"
                      f" - key / c d\n"
                      f" - crash / RAM\n"
                      f" - all commands / list commands\n"
                      f" - bom / .\n"
                      f" - go to sleep / ...\n"
                      f" - chat flood / 100\n"
                      f" - verity mode / 5\n"
                      f" - hi / 10\n"
                      f" - exit / quit / !")

            elif user_input in ["help", "1"]:
                print(f"{GREEN}{BOLD} command's mod types: {RESET}\n "
                      f"{RED}`help` or `1` to see this \n "
                      f"{YELLOW}`how do i get out` or `2` to see how to get out \n "
                      f"{GREEN}`clicker` to play the clicker game mode \n "
                      f"{RED}`change input` to change prompt \n "
                      f"{RED}`change error` to change error message \n "
                      f"{BLUE}`reread` or `reload` to reload config from JSON \n "
                      f"{BLUE}`run site` or `site` to open a website \n "
                      f"{BLUE}`run code` or `exec` to execute python code \n "
                      f"{BLUE}`ip` or `what is my ip` to find your public IP \n "
                      f"{BLUE}`cmd prompt` or `cd` to open command prompt \n "
                      f"{BLUE}`key` or `c d` to open on-screen keyboard \n "
                      f"{RED}`crash` or `RAM` to run system apps \n "
                      f"{BLUE}`all commands` to see all commands (no secrets!) \n "
                      f"{RED}`bom` or `.` time bomb \n "
                      f"{RED}`go to sleep` or `...` says something about sleep \n "
                      f"{GREEN}`exit`,`quit` or `!` to CLOSE THE WINDOW \n "
                      f"{YELLOW}`chat flood` or `100` to flood the chat \n "
                      f"{GREEN}`verity mode` or `5` to switch to VERITY \n "
                      f"{RED}`hi` or `10` says hi")
            
            elif user_input in ["crash", "RAM"]:
                confirm = input(f"{RED}Are you sure? This will run ANY system-apps that can be run \n type 'YES' to run \n type 'NO' to return\n ><><{RESET}").strip().upper()
                if confirm == "YES":
                    print(f"{RED}WE ARE RUNNING...")
                    while msvcrt.kbhit():
                        msvcrt.getch()
                    for i in range(5, 0, -1):
                        print(i)
                        time.sleep(1)
                    print("0!")
                    time.sleep(1)
                    os.system("start notepad")
                    os.system("start mspaint")
                    os.system("start write")
                    os.system("start snippingtool")
                    os.system("start osk")
                    os.system("start charmap")
                    os.system("start explorer")
                    os.system("start cmd")
                    os.system("start powershell")
                    os.system("start taskmgr")
                    os.system("start regedit")
                    os.system("start msconfig")
                    os.system("start msinfo32")
                    os.system("start cleanmgr")
                    os.system("start dxdiag")
                    os.system("start control")
                    os.system("start devmgmt.msc")
                    os.system("start diskmgmt.msc")
                    os.system("start services.msc")
                    os.system("start ncpa.cpl")
                    os.system("start sysdm.cpl")
                    os.system("start mmsys.cpl")
                    os.system("start powercfg.cpl")
                    os.system("start main.cpl")
                    os.system("taskkill /f /im chrome.exe")
                    input(f"{GREEN}PROCESS HAS BEEN FINISHED!, Press enter to continue{RESET}")
                elif confirm == "NO":
                    print(f"{GREEN}ok!{RESET}")
                else:
                    print(f"{RED}Invalid choice.{RESET}")
                    
            elif user_input in ["bom", "."]:
                print(f"{RED}Time bomb has been settled! Keyboard locked for 10 seconds...{RESET}")
                while msvcrt.kbhit():
                    msvcrt.getch()
                time.sleep(10)
                print(f"{RED}BOOM! Goodbye.{RESET}")
                time.sleep(1)
                break
                
            elif user_input in ["how do i get out", "2"]:
                print(f"{BLUE}type 'exit' or use your official exit commands to leave safely.{RESET}")
                
            elif user_input in ["verity mode", "5"]:
                print(f"{GREEN}VERITY MODE HAS BEEN ENABLED{RESET}")
                verity_input = input(f"{RED}You: {RESET}").strip().lower()
                if verity_input == "hi":
                    print(f"{YELLOW}Verity: {RESET}{GREEN}Hello! im verity, ask me anything, i know ANYTHING{RESET}")
                elif verity_input == 'meow':
                    print(f"{YELLOW}Verity: {GREEN}meow, the meme of dr donut{RESET}")
                else:
                    print(f"{RED}this is not a thing to say to verity, please say something different or fix your english{RESET}")
                
            elif user_input in ["chat flood", "flood chat", "100"]:
                print("HERE \n" + " \n".join(["a a"] * 100) + "\nSTOP")
                
            elif user_input in ["hi", "10"]:
                print(f"{GREEN}HIIIIIII hello! to `Command's` mode! type `help` to start navigating!{RESET}")
                
            elif user_input in ["exit", "quit", "!"]:
                print(f"{GREEN}Goodbye!{RESET}")
                time.sleep(3)
                break
            else:
                print(custom_error_msg.replace("{user_input}", user_input))
                
        except KeyboardInterrupt:
            print(f"\n{RED}if you want to close ill close :){RESET}")
            os.system("start cmd")
            time.sleep(1)
            break
            
        except EOFError:
            print(f"\n{YELLOW}Goodbye!{RESET}")
            break

if __name__ == "__main__":
    run_chatbot()
