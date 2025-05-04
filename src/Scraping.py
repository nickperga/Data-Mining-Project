import string
from csv import writer
import requests
import re
import regex
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#this function finds all the articles used in each decision
def findArticleIdentifiers(text : string):
    result = {"ΚΠολΔ" : [], "ΑΚ" : [], "ΚΠΔ" : [], "ΠΚ" : []}
    #finds the vast majority of articles for code of political justice
    matchKPolDTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\bΚΠολΔ\b', text)
    cleanedMatchKPolDTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchKPolDTypes]
    matchKPolDTypesFirst = re.findall(r'ΚΠολΔ\s*(\d+(?:\s*,\s*\d+)*)', text)

    #finds the vast majority of articles for civilian code
    matchAKTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\bΑΚ\b', text, re.DOTALL)
    cleanedMatchAKTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchAKTypes]
    matchAKTypesFirst = re.findall(r'ΑΚ\s*(\d+(?:\s*,\s*\d+)*)', text)

    result["ΚΠολΔ"].extend(cleanedMatchKPolDTypes)
    result["ΚΠολΔ"].extend(matchKPolDTypesFirst)
    result["ΑΚ"].extend(cleanedMatchAKTypes)
    result["ΑΚ"].extend(matchAKTypesFirst)

    #finds the vast majority of articles for code of criminal procedure
    matchKPDTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\b(ΚΠΔ|Κ.Ποιν.Δ|ΚΠοινΔ)\b', text)
    cleanedKPDTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchKPDTypes]
    matchKPDTypesFirst = re.findall(r'(ΚΠΔ|Κ.Ποιν.Δ|ΚΠοινΔ)\s*(\d+(?:\s*,\s*\d+)*)', text)

    #finds the vast majority of articles for criminal code
    matchPKTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\b(ΠΚ)\b', text)
    cleanedPKTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchPKTypes]
    matchPKTypesFirst = re.findall(r'(ΠΚ)\s*(\d+(?:\s*,\s*\d+)*)', text)

    result["ΚΠΔ"].extend(cleanedKPDTypes)
    result["ΚΠΔ"].extend(matchKPDTypesFirst)
    result["ΠΚ"].extend(cleanedPKTypes)
    result["ΠΚ"].extend(matchPKTypesFirst)
    return result

#Here i define the selenium's driver's options
options = Options()
options.add_argument("--headless")
#optional
options.add_argument('--disable-gpu')

#initial page's url
page_url = "https://areiospagos.gr/"
r = requests.get(page_url)
#necessary to correctly recognize greek
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.content, "html.parser")

#finds the area of the page which has the href i want
frame = soup.find("frameset").find("frame", {"name" : "contents"})
frame_src = frame.get("src")

#creates a valid url with the teo hrefs
if not frame_src.startswith("http"):
    from urllib.parse import urljoin
    frame_src = urljoin("https://areiospagos.gr/", frame_src)

frame_html = requests.get(frame_src)
frame_html.encoding = frame_html.apparent_encoding

frame_soup = BeautifulSoup(frame_html.text, "html.parser")
#here i find the needed anchor element
a_decisions = frame_soup.find("body").find("a", {"href" : "nomologia/apofaseis.asp"})
next_page_url = urljoin(page_url, a_decisions["href"])

#opens a selenium driver as the page has javascript
driver = webdriver.Chrome(options=options)
driver.get(next_page_url)

inputElement = driver.find_element(By.NAME, "x_ETOS")
inputElement.send_keys("2024")

submitButton = driver.find_element(By.NAME, "submit_krit")
submitButton.click()

#makes the driver to wait until every needed html element has loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
)

wantedPageSoup = BeautifulSoup(driver.page_source, "html.parser")

pattern = re.compile(r'ΠΟΛΙΤΙΚΕΣ|ΠΟΙΝΙΚΕΣ', re.UNICODE)

anchors = wantedPageSoup.find_all("a", href=pattern)
neededUrl = urljoin(page_url, "nomologia")
finalResult = {
    "year" : [],
    "number" : [],
    "department" : [],
    "department number" : [],
    "judges" : [],
    "entry text" : [],
    "final text" : [],
    "ΠΚ" : [],
    "ΚΠΔ" : [],
    "ΚΠολΔ" : [],
    "ΑΚ" : []
}
pagesToIgnore = [ 2318, 2159, 1923, 1881, 1882, 1838, 1669, 1666, 1622, 1590, 1500, 1460, 1310, 1229, 1199, 1284, 1218, 1067, 1040, 1380, 1021, 995, 996, 997, 998, 994, 993, 899, 774, 745, 719, 641, 637, 1444, 593, 534, 1464, 464, 1493, 1508, 339, 1495, 328, 286, 2425, 2426, 1810, 1577, 2274, 1670, 1487, 2306, 261, 196, 183, 158, 46]

for i in range(2425):
    if(i in pagesToIgnore):
        continue
    decision1 = requests.get(neededUrl + "/" + anchors[i].get("href"))
    decision1.encoding = decision1.apparent_encoding

    decision1Soup = BeautifulSoup(decision1.text, "html.parser")
    text = decision1Soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    
    match_decision = re.search(r'(?:ΑΡΙΘΜΟΣ|Αριθμός|Απόφαση)\s*(\d+)\s*/\s*(\d{4})\s*\(([^,]+),\s*([^)]+)\)', text)

    if match_decision:
        decision_id, decision_year, division_number, raw_division_type = match_decision.groups()
        if "ΠΟΛΙΤΙΚΕΣ" in raw_division_type.upper():
            division_type = "Πολιτικό"
        elif "ΠΟΙΝΙΚΕΣ" in raw_division_type.upper():
            division_type = "Ποινικό"
        else:
            division_type = None
    else:
        decision_id, decision_year, division_number, division_type = None, None, None, None
    finalResult["number"].append(decision_id)
    finalResult["year"].append(decision_year)
    finalResult["department number"].append(division_number)
    finalResult["department"].append(division_type)
    #finds the sentence which includes all the participating judges
    matchJudgesText = re.search(r'(?:Συγκροτήθηκε|ΣΥΓΚΡΟΤΗΘΗΚΕ) από τους (?:Δικαστές|δικαστές)[,:]?\s*(.*?)(ΣΥΝΗΛΘΕ|Συνήλθε|Με την παρουσία|Συνεδρίασε|ΣΥΝΕΔΡΙΑΣΕ|και του Γραμματέα|Κατόπιν|Ακολούθως)',text, re.DOTALL)
    finalResult["judges"].append(matchJudgesText.group())

    #finds the first text needed
    matchText1 = re.search(r'((?:Τ\s*Ο\s*Δ\s*Ι\s*Κ\s*Α\s*Σ\s*Τ\s*Η\s*Ρ\s*Ι\s*Ο\s*Τ\s*Ο\s*Υ\s*Α\s*Ρ\s*Ε\s*Ι\s*Ο\s*Υ\s*Π\s*Α\s*Γ\s*Ο\s*Υ)[\s\S]*?)(?=(Συγκροτήθηκε|ΣΥΓΚΡΟΤΗΘΗΚΕ))', text)
    clean_result = re.sub(r'\s+', ' ', matchText1.group()).strip()
    finalResult["entry text"].append(clean_result)

    #finds the second text needed
    pattern = regex.compile(r'ΓΙΑ ΤΟΥ(Σ)?\s*ΛΟΓΟΥΣ(?: ΑΥΤΟΥΣ)?[\s\S]*', flags=regex.UNICODE)
    matchText2 = pattern.search(text)
    clean_result = re.sub(r'\s+', ' ', matchText2.group()).strip()
    finalResult["final text"].append(clean_result)

    result = findArticleIdentifiers(text)
    finalResult["ΑΚ"].append(result["ΑΚ"])
    finalResult["ΚΠΔ"].append(result["ΚΠΔ"])
    finalResult["ΚΠολΔ"].append(result["ΚΠολΔ"])
    finalResult["ΠΚ"].append(result["ΠΚ"])

#manually shutting down the driver
driver.quit()

#Here i write all my data in a csv file in a transpose format
with open(f"save/data.csv", "w", encoding="utf-8") as f:
    wr = writer(f)
    #Headers
    wr.writerow(finalResult.keys())
    lists : list = list(finalResult.values())
    for i in range(len(lists[0])):
        row = []
        for column in lists:
            row.append(column[i])
        wr.writerow(row)
print("Saved data...")
