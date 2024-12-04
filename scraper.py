import json
import os
import re
import time
from getpass import getpass
from pathlib import Path

from playwright.sync_api import sync_playwright


username = os.environ["UKC_USERNAME"]

if "UKC_PASSWORD" in os.environ:
    password = os.environ["UKC_PASSWORD"]
else:
    password = getpass()


playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)

p = browser.new_page()
p.goto("https://www.ukclimbing.com/user/")
p.locator("#email").fill(username)
p.locator("#password").fill(password)
p.get_by_title("Login as Existing User ").click()

p.goto("https://www.ukclimbing.com/logbook/crags/symonds_yat-403/")

records = json.loads(re.search(r"table_data = (\[.*\])", p.content()).groups()[0])

download_dir = Path("downloads")
download_dir.mkdir(exist_ok=True)

for i, r in enumerate(records):
    file_path = download_dir / f"{r['slug']}.html"
    if file_path.exists():
        continue
    time.sleep(10)
    url = f"https://www.ukclimbing.com/logbook/crags/symonds_yat-403/{r['slug']}"
    print(f"{i} / {len(records)} / {url}")
    p.goto(url)
    file_path.write_text(p.content())
