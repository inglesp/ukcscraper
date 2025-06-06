import csv
import os
from pathlib import Path

from bs4 import BeautifulSoup


userid = os.environ["UKC_USERID"]
username = os.environ["UKC_USERNAME"]


def main():
    with open("symonds-yat-logs.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, ["name", "grade", "user_id", "user_name", "date", "style"]
        )
        writer.writeheader()
        for path in sorted(Path("downloads").glob("*.html")):
            print(path)
            writer.writerows(extract_logs(path))


def extract_logs(path):
    doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    name, grade = doc.find(class_="nav-tabs-header").find("h1").text.splitlines()
    grade = grade.strip()
    for t in doc.find(id="logbooks").find_all("table"):
        if t.parent["id"] == "my_logbook":
            extractor = extract_my_logs
        else:
            extractor = extract_other_logs
        for log in extractor(t):
            log["name"] = name
            log["grade"] = grade
            yield (log)


def extract_my_logs(t):
    for tr in t.find("tbody").find_all("tr"):
        if "d-sm-none" in tr["class"]:
            continue

        tds = tr.find_all("td")

        yield {
            "user_id": userid,
            "user_name": username,
            "date": tds[0].text.strip(),
            "style": tds[1].text.strip(),
        }


def extract_other_logs(t):
    for tr in t.find("tbody").find_all("tr"):
        if "d-sm-none" in tr["class"]:
            continue

        tds = tr.find_all("td")
        user_name = tds[0].text.strip()
        if user_name == "Hidden":
            user_id = ""
        else:
            user_id = tds[0].find("a")["href"].split("=")[1]

        yield {
            "user_id": user_id,
            "user_name": user_name,
            "date": tds[1].text.strip(),
            "style": tds[2].text.strip(),
        }


if __name__ == "__main__":
    main()
