import requests
from bs4 import BeautifulSoup
import json
import time
from googletrans import Translator

translator = Translator()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

results = []

# -----------------------------
# دالة الترجمة
# -----------------------------
def translate_text(text):
    try:
        en = translator.translate(text, src='ar', dest='en').text
        ku = translator.translate(text, src='ar', dest='ku').text
        return en, ku
    except Exception as e:
        print(f"Translation error: {e}")
        return "", ""

# -----------------------------
# مواقع الفتاوى
# -----------------------------
def scrape_islamqa():
    urls = ["https://islamqa.info/ar/categories/topics/3"]
    for url in urls:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        links = soup.select("a.question-summary__link")
        for link in links[:10]:
            q_url = "https://islamqa.info" + link.get("href")
            try:
                r = requests.get(q_url, headers=HEADERS)
                s = BeautifulSoup(r.text, "lxml")
                question_ar = s.select_one("h1").text.strip()
                answer_block = s.select_one(".js-answer")
                if not answer_block: continue
                answer_ar = answer_block.get_text(separator="\n").strip()
                question_en, question_ku = translate_text(question_ar)
                answer_en, answer_ku = translate_text(answer_ar)
                results.append({
                    "question": {"ar": question_ar, "en": question_en, "ku": question_ku},
                    "answer": {"ar": answer_ar, "en": answer_en, "ku": answer_ku},
                    "source": "islamqa",
                    "url": q_url,
                    "category": "عام"
                })
                time.sleep(1)
            except: continue

def scrape_islamweb():
    url = "https://www.islamweb.net/ar/fatawa/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("a")
    for link in links[:20]:
        href = link.get("href", "")
        if "/ar/fatwa/" not in href: continue
        full_url = "https://www.islamweb.net" + href
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            question_block = s.select_one("h1")
            answer_block = s.select_one(".article-body")
            if not question_block or not answer_block: continue
            question_ar = question_block.text.strip()
            answer_ar = answer_block.get_text("\n").strip()
            question_en, question_ku = translate_text(question_ar)
            answer_en, answer_ku = translate_text(answer_ar)
            results.append({
                "question": {"ar": question_ar, "en": question_en, "ku": question_ku},
                "answer": {"ar": answer_ar, "en": answer_en, "ku": answer_ku},
                "source": "islamweb",
                "url": full_url,
                "category": "عام"
            })
            time.sleep(1)
        except: continue

def scrape_binbaz():
    url = "https://binbaz.org.sa/fatwas"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("a")
    for link in links[:20]:
        href = link.get("href", "")
        if "/fatwas/" not in href: continue
        full_url = "https://binbaz.org.sa" + href
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            title = s.select_one("h1")
            content = s.select_one(".article-content")
            if not title or not content: continue
            question_ar = title.text.strip()
            answer_ar = content.get_text("\n").strip()
            question_en, question_ku = translate_text(question_ar)
            answer_en, answer_ku = translate_text(answer_ar)
            results.append({
                "question": {"ar": question_ar, "en": question_en, "ku": question_ku},
                "answer": {"ar": answer_ar, "en": answer_en, "ku": answer_ku},
                "source": "binbaz",
                "url": full_url,
                "category": "عام"
            })
            time.sleep(1)
        except: continue

def scrape_uthaymeen():
    url = "https://binothaimeen.net/site/index"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    links = soup.select("a")
    for link in links[:20]:
        href = link.get("href", "")
        if "/content/" not in href: continue
        full_url = "https://binothaimeen.net" + href
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            title = s.select_one("h1")
            content = s.select_one(".article-content")
            if not title or not content: continue
            question_ar = title.text.strip()
            answer_ar = content.get_text("\n").strip()
            question_en, question_ku = translate_text(question_ar)
            answer_en, answer_ku = translate_text(answer_ar)
            results.append({
                "question": {"ar": question_ar, "en": question_en, "ku": question_ku},
                "answer": {"ar": answer_ar, "en": answer_en, "ku": answer_ku},
                "source": "uthaymeen",
                "url": full_url,
                "category": "عام"
            })
            time.sleep(1)
        except: continue

# -----------------------------
# تشغيل الكل وحفظ JSON
# -----------------------------
def run():
    scrape_islamqa()
    scrape_islamweb()
    scrape_binbaz()
    scrape_uthaymeen()
    unique = {item['question']['ar']: item for item in results}
    final_data = list(unique.values())
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(final_data)} items.")

if __name__ == "__main__":
    run()
