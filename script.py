import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

results = []

# -----------------------------
# IslamQA
# -----------------------------
def scrape_islamqa():
    urls = [
        "https://islamqa.info/ar/categories/topics/3",  # مثال: الطهارة
    ]
    
    for url in urls:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        
        links = soup.select("a.question-summary__link")
        
        for link in links[:10]:
            q_url = "https://islamqa.info" + link.get("href")
            
            try:
                r = requests.get(q_url, headers=HEADERS)
                s = BeautifulSoup(r.text, "lxml")
                
                question = s.select_one("h1").text.strip()
                answer_block = s.select_one(".js-answer")
                
                if not answer_block:
                    continue
                
                answer = answer_block.get_text(separator="\n").strip()
                
                results.append({
                    "question": question,
                    "answer": answer,
                    "source": "islamqa",
                    "url": q_url,
                    "category": "عام"
                })
                
                time.sleep(1)
            except:
                continue


# -----------------------------
# IslamWeb
# -----------------------------
def scrape_islamweb():
    url = "https://www.islamweb.net/ar/fatawa/"

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    links = soup.select("a")

    for link in links[:20]:
        href = link.get("href", "")
        if "/ar/fatwa/" not in href:
            continue
        
        full_url = "https://www.islamweb.net" + href
        
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            
            question = s.select_one("h1")
            answer = s.select_one(".article-body")
            
            if not question or not answer:
                continue
            
            results.append({
                "question": question.text.strip(),
                "answer": answer.get_text("\n").strip(),
                "source": "islamweb",
                "url": full_url,
                "category": "عام"
            })
            
            time.sleep(1)
        except:
            continue


# -----------------------------
# BinBaz
# -----------------------------
def scrape_binbaz():
    url = "https://binbaz.org.sa/fatwas"

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    links = soup.select("a")

    for link in links[:20]:
        href = link.get("href", "")
        if "/fatwas/" not in href:
            continue
        
        full_url = "https://binbaz.org.sa" + href
        
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            
            title = s.select_one("h1")
            content = s.select_one(".article-content")
            
            if not title or not content:
                continue
            
            results.append({
                "question": title.text.strip(),
                "answer": content.get_text("\n").strip(),
                "source": "binbaz",
                "url": full_url,
                "category": "عام"
            })
            
            time.sleep(1)
        except:
            continue


# -----------------------------
# Ibn Uthaymeen
# -----------------------------
def scrape_uthaymeen():
    url = "https://binothaimeen.net/site/index"

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")

    links = soup.select("a")

    for link in links[:20]:
        href = link.get("href", "")
        if "/content/" not in href:
            continue
        
        full_url = "https://binothaimeen.net" + href
        
        try:
            r = requests.get(full_url, headers=HEADERS)
            s = BeautifulSoup(r.text, "lxml")
            
            title = s.select_one("h1")
            content = s.select_one(".article-content")
            
            if not title or not content:
                continue
            
            results.append({
                "question": title.text.strip(),
                "answer": content.get_text("\n").strip(),
                "source": "uthaymeen",
                "url": full_url,
                "category": "عام"
            })
            
            time.sleep(1)
        except:
            continue


# -----------------------------
# تشغيل الكل
# -----------------------------
def run():
    scrape_islamqa()
    scrape_islamweb()
    scrape_binbaz()
    scrape_uthaymeen()
    
    # إزالة التكرار
    unique = {item['question']: item for item in results}
    
    final_data = list(unique.values())

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(final_data)} items.")


if __name__ == "__main__":
    run()