import requests
import hashlib
import os

URL = "https://example.com"   # webpage to monitor
HASH_FILE = "last_hash.txt"

def get_page_hash():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return hashlib.sha256(r.text.encode("utf-8")).hexdigest()

def main():
    new_hash = get_page_hash()

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hash = f.read().strip()
    else:
        old_hash = ""

    if old_hash != new_hash:
        print(f"::notice:: Webpage changed! {URL}")
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
    else:
        print("No change detected.")

if __name__ == "__main__":
    main()
