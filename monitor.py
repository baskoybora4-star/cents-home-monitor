print("CEnT-S Monitor başlatıldı")

import requests
from bs4 import BeautifulSoup

URL = "https://testcisia.it/calendario.php?tolc=cents&l=gb&lingua=inglese"


def check_dates():
    print("CEnT-S Monitor başlatılıyor...")

    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    home_dates = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        values = [cell.get_text(" ", strip=True) for cell in cells]

        if len(values) < 8:
            continue

        exam_format = values[0].upper()

        if "CENT@HOME" not in exam_format:
            continue

        university = values[1]
        seats = values[5]
        status = values[6]
        date = values[7]

        home_dates.append({
            "university": university,
            "seats": seats,
            "status": status,
            "date": date
        })

    print("\n--- CENT@HOME TARİHLERİ ---")

    if not home_dates:
        print("Takvimde CEnT@HOME tarihi bulunamadı.")
        return

    for item in home_dates:
        print(
            f"{item['date']} | "
            f"{item['university']} | "
            f"{item['seats']} kontenjan | "
            f"{item['status']}"
        )

    print("\nKontrol tamamlandı.")


if __name__ == "__main__":
    check_dates()
