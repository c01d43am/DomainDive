import os
import sys
import subprocess

def print_banner():
    green = '\033[92m'  # Green color
    red = '\033[91m'    # Red color
    reset = '\033[0m'   # Reset color

    banner = f"""
{green}██████╗░░█████╗░███╗░░░███╗░█████╗░██╗███╗░░██╗██████╗░██╗██╗░░░██╗███████╗{reset}
{green}██╔══██╗██╔══██╗████╗░████║██╔══██╗██║████╗░██║██╔══██╗██║██║░░░██║██╔════╝{reset}
{green}██║░░██║██║░░██║██╔████╔██║███████║██║██╔██╗██║██║░░██║██║╚██╗░██╔╝█████╗░░{reset}
{green}██║░░██║██║░░██║██║╚██╔╝██║██╔══██║██║██║╚████║██║░░██║██║░╚████╔╝░██╔══╝░░{reset}
{green}██████╔╝╚█████╔╝██║░╚═╝░██║██║░░██║██║██║░╚███║██████╔╝██║░░╚██╔╝░░███████╗{reset}
{green}╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝╚═════╝░╚═╝░░░░╚═╝░░░╚══════╝{reset}
{red}                                                          v 0.0.1  c01d43am  {reset}
"""
    print(banner)

def execute_main_script():
    """Execute the main script (subdomain.py in the 'main' folder)"""
    try:
        # Get the absolute path of the current directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_directory, "main", "subdomain.py")  # Path to subdomain.py in the 'main' folder
        
        # Check if the file exists before running
        if not os.path.exists(script_path):
            print(f"[ERROR] The script file {script_path} does not exist.", end="\n", flush=True)
            return
        
        print(f"[INFO] Running the subdomain enumeration script: {script_path}...", end="\n", flush=True)
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error occurred while running the main script: {e}", end="\n", flush=True)

def main_menu():
    """Display the main menu and handle user selection"""
    while True:
        print("\n[MENU] Choose an option:")
        print("1. Start subdomain enumeration")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            execute_main_script()
        elif choice == "2":
            print("[INFO] Exiting program.", end="\n", flush=True)
            break
        else:
            print("[ERROR] Invalid choice, please try again.", end="\n", flush=True)

if __name__ == "__main__":
    print_banner()  # Display the banner
    main_menu()  # Show the menu and handle user input
