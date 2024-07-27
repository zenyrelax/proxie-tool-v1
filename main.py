from time import sleep
from modules.updater import check_update
from modules.variables import Checker, discord_name, discord_server
from modules.config import *
from modules.functions import *
from modules.start import starter,modules_list
import modules.tools.proxy_check as proxy_check
import modules.tools.proxy_scrape as proxy_scrape
import modules.tools.capture_remove as captureremover
import modules.tools.combo_edit as combo_edit
import modules.tools.domain_sort as domain_sort
import os
import tkinter.messagebox

if is_win():
    import win32api

def home():
    while 1:
        change_title(f"Calani AIO | Home | {discord_name}")
        clear()
        ascii()
        print(f"""    [{red}Main Menu{reset}]

    [{red}1{reset}] Modules
    [{red}2{reset}] Tools
    [{red}3{reset}] Settings
    [{red}4{reset}] Info

    [{red}5{reset}] Exit""")
        option = input(f"    [{red}>{reset}] ").lower()
        match option:
            case "1": modules()
            case "2": tools()
            case "3": settings()
            case "4": info()
            case "5": exit_program()

def info():
    clear()
    ascii()
    print(f"    [{red}Info{reset}]\n")
    print(f"""    [{red}>{reset}] Developed By: Zenyrelax
    [{red}>{reset}] Discord Server: https://discord.gg/zenyrelax
    [{red}>{reset}] Wanna Make A Donation?
        BTC: bc1qt6gcll4hp7wwqaap7x3lwunf9srw4enuxxddzn
        ETH: 0xd7F5C1AB4765Be15F738367905bF4E7Ea83eC9F7
        LTC: LdsjBD8ACvqUinrgbJJvCcELs2AxN5NSpc

    [{red}>{reset}] If you paid for this application, you were SCAMMED!

    Press Enter To Go Back""",end="")
    input()

def modules():
    selected_modules = []
    if Checker.api_key:
        balance = get_solver_balance()
    while 1:
        change_title(f"Calani AIO | Modules | {discord_name}")
        clear()
        ascii()
        print(f"    [{red}Modules{reset}]\n")
        
        disabled = []
        for module in modules_list:
            if module in selected_modules and module.split(' ')[0] in ['discord']:
                if not Checker.api_key or not balance or 'Invalid' in balance:
                    selected_modules.remove(module)
                    disabled.append(module.split(' ')[0])
            index = list(modules_list).index(module)+1
            selected = f"{red}+{reset}" if module in selected_modules else " "
            print(f"    [{selected}] [{red}{index}{reset}] {module.title()}")
        
        print(f"""
    [{red}>{reset}] Use CTRL+F To Search For A Module
    [{red}>{reset}] Choose A Number To Select/Deselect A Module
    [{red}>{reset}] Seperate Numbers With ',' To Select Multiple Modules Faster

    [{red}>{reset}] Selected Modules: {len(selected_modules)}/{len(modules_list)}
    [{red}A{reset}] Select/Deselect All
    [{red}S{reset}] Start Checking

    [{red}X{reset}] Back""")
        if disabled:
            disabled = "\n".join([module for module in disabled])
            tkinter.messagebox.showinfo('Modules Disabled',f'The following modules were disabled because the api key was invalid or the solver setting was disabled.\n\n{disabled.title()}')
        
        option = input(f"    [{red}>{reset}] ").lower()
        if option.isdigit():
            if int(option) <= len(modules_list) and int(option):
                module = list(modules_list)[int(option)-1]
                selected_modules.append(module) if module not in selected_modules else selected_modules.remove(module)
        
        elif "," in option:
            for module in option.split(","):
                if module.isdigit() and int(module) <= len(modules_list) and int(module):
                    module = list(modules_list)[int(module)-1]
                    selected_modules.append(module) if module not in selected_modules else selected_modules.remove(module)
        
        match option:
            case "s":
                if not selected_modules:
                    print(f"    [{red}>{reset}] Must select at least 1 module!")
                    sleep(1)
                    continue
                
                starter(selected_modules)
                selected_modules.clear()
        
            case "a":
                if selected_modules: 
                    selected_modules.clear()
                    continue
                
                for module in modules_list:
                    if module not in selected_modules: selected_modules.append(module)
            
            case "x": return

def settings():
    while 1:
        load_config()
        change_title(f"Calani AIO | Settings | {discord_name}")
        clear()
        ascii()
        if Checker.api_key:
            print(f'    [{red}Getting API Key Balance{reset}]')
            status = get_solver_balance()
            clear()
            ascii()
        else:
            status = f'{red}Disabled{reset}'
        
        print(f"""    [{red}Settings{reset}]

    [{red}1{reset}] Proxy Type: {Checker.proxy_type.title()}
    [{red}2{reset}] Proxy Timeout: {Checker.timeout}s
    [{red}3{reset}] Print Mode: {"CUI" if Checker.cui else "LOG"}
    [{red}4{reset}] Retries: {Checker.retries}
    [{red}5{reset}] Threads: {Checker.threads}
    [{red}6{reset}] Solver Service: {Checker.solver_serice.title()}
    [{red}7{reset}] Solver API Key: {Checker.api_key if Checker.api_key else None} | Status: {status}
    [{red}8{reset}] Discord Webhook: {Checker.discord_webhook.replace("https://discord.com/api/webhooks","...") if 'https://discord.com/api/webhooks/' in Checker.discord_webhook else None}
   
    [{red}ENTER{reset}] Reload Config

    [{red}O{reset}] Open Config File
    [{red}X{reset}] Back""")
        option = input(f"    [{red}>{reset}] ").lower()
        match option:
            case "1": change("proxy_type")
            case "2": change("proxy_timeout")
            case "3": change("print")
            case "4": change("retries")
            case "5": change("threads")
            case "6": change("solver_service")
            case "7": change("api_key")
            case "8": change("discord_webhook")
            case "o": os.startfile(os.path.join(os.getcwd(),'Data/config.json'))
            case "x": return

def tools():
    while 1:
        load_config()
        change_title(f"Calani AIO | Tools | {discord_name}")
        clear()
        ascii()
        print(f"""    [{red}Tools{reset}]

    [{red}1{reset}] Proxy Checker
    [{red}2{reset}] Proxy Scraper
    [{red}3{reset}] Capture Remover
    [{red}4{reset}] Combo Editor
    [{red}5{reset}] Domain Sorter

    [{red}X{reset}] Back""")
        option = input(f"    [{red}>{reset}] ").lower()
        match option:
            case "1": proxy_check.start()
            case "2": proxy_scrape.start()
            case "3": captureremover.start()
            case "4": combo_edit.start()
            case "5": domain_sort.start()
            case "x": return

if __name__ == "__main__":
    if is_win():
        win32api.SetConsoleCtrlHandler(exit_program, True)
    load_config()
    
    clear()
    ascii()
    
    set_title('Info')
    input(f"""    [{red}Creator Info{reset}]

    [{red}Discord{reset}] {discord_name}
    [{red}Github{reset}] zenyrelax

    [{red}Continue{reset}] Enter""")
    
    clear()
    ascii()
    check_update()
    home()
