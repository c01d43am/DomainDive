import os
import sys
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re  # Import for domain validation

def check_and_install(module_name):
    """Check if module is installed and install if missing"""
    try:
        __import__(module_name)
    except ImportError:
        print(f"[INFO] Installing {module_name}...", end="\n", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_pip():
    """Ensure pip is installed"""
    try:
        import pip
    except ImportError:
        print("[INFO] Installing pip...", end="\n", flush=True)
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Ensure pip is installed and required libraries are present
install_pip()
for module in ["requests", "beautifulsoup4"]:
    check_and_install(module)

def sanitize_domain(domain):
    """Sanitize and validate the domain"""
    domain = domain.strip()  # Remove leading/trailing spaces
    # Check if the domain has valid characters and structure
    if re.match(r"^(?!-)[A-Za-z0-9.-]{1,253}(?<!-)\.[A-Za-z]{2,6}$", domain):
        return domain
    else:
        print("[ERROR] Invalid domain format. Please enter a valid domain.", end="\n", flush=True)
        return None

def bing_search(domain):
    """Search Bing for subdomains"""
    print("[INFO] Searching Bing for subdomains...", end="\n", flush=True)
    subdomains = set()
    base_url = f"https://www.bing.com/search?q=site:{domain}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(base_url, headers=headers, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            for link in links:
                href = link.get("href")
                if href:
                    parsed_url = urlparse(href)
                    if parsed_url.hostname and domain in parsed_url.hostname:
                        subdomains.add(parsed_url.hostname)
        else:
            print("[WARNING] Bing search did not return a 200 status code.", end="\n", flush=True)
    except Exception as e:
        print(f"[ERROR] Bing search failed: {e}", end="\n", flush=True)
    return subdomains

def crt_sh_search(domain):
    """Search crt.sh for subdomains"""
    print("[INFO] Searching crt.sh for subdomains...", end="\n", flush=True)
    subdomains = set()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            json_data = response.json()
            for entry in json_data:
                subdomain = entry["name_value"]
                subdomains.update(subdomain.split("\n"))
        else:
            print("[WARNING] crt.sh search did not return a 200 status code.", end="\n", flush=True)
    except Exception as e:
        print(f"[ERROR] crt.sh search failed: {e}", end="\n", flush=True)
    return subdomains

def format_subdomains(subdomains):
    """Format subdomains into a more readable format"""
    formatted_subdomains = []
    for subdomain in sorted(subdomains):
        formatted_subdomains.append(f"- {subdomain}")
    return "\n".join(formatted_subdomains)

def enumerate_subdomains(domain):
    """Enumerate subdomains from Bing and crt.sh"""
    print(f"\n[INFO] Starting subdomain enumeration for: {domain}", end="\n", flush=True)
    all_subdomains = set()

    # Bing search
    bing_subdomains = bing_search(domain)
    print(f"[DEBUG] Bing subdomains found: ", end="\n", flush=True)
    all_subdomains.update(bing_subdomains)

    # crt.sh search
    crt_sh_subdomains = crt_sh_search(domain)
    print(f"[DEBUG] crt.sh subdomains found: ", end="\n", flush=True)
    all_subdomains.update(crt_sh_subdomains)

    # Display and save results
    if all_subdomains:
        print("\n[RESULTS] Subdomains found:", end="\n", flush=True)
        formatted_results = format_subdomains(all_subdomains)
        print(formatted_results, end="\n", flush=True)

        # Save to file
        with open(f"{domain}_subdomains.txt", "w") as file:
            file.write(formatted_results)
        print(f"\n[INFO] Results saved to {domain}_subdomains.txt", end="\n", flush=True)
    else:
        print("\n[INFO] No subdomains found.", end="\n", flush=True)

if __name__ == "__main__":
    target_domain = input("Enter the target domain: ").strip()
    sanitized_domain = sanitize_domain(target_domain)
    if sanitized_domain:
        enumerate_subdomains(sanitized_domain)
    else:
        print("[ERROR] Exiting due to invalid domain input.", end="\n", flush=True)
