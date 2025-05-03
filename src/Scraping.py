import string
from csv import writer
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def findArticleIdentifiers(decisionType : string, text : string):
    result = {"ΚΠολΔ" : [], "ΑΚ" : [], "ΚΠΔ" : [], "ΠΚ" : []}
    if(decisionType == "Πολιτικό"):
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
        result["ΑΚ"].extend(matchAKTypes)
    else:
        #finds the vast majority of articles for code of criminal procedure
        matchKPDTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\b(ΚΠΔ|Κ.Ποιν.Δ|ΚΠοινΔ)\b', text)
        cleanedKPDTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchKPDTypes]
        matchKPDTypesFirst = re.findall(r'(ΚΠΔ|Κ.Ποιν.Δ|ΚΠοινΔ)\s*(\d+(?:\s*,\s*\d+)*)', text)

        #finds the vast majority of articles for criminal code
        matchPKTypes = re.findall(r'(?:\([^\)]*\))?\s*(?:άρθρο|άρθρων|άρθρα|άρθρου|άρθρ\.|αρθ\.)\s*((?:\d+(?:\s*,\s*|\s*και\s*)?|\s*παρ\.\s*\d+\s*,?\s*)+)\s+[^ν]*?\b(ΠΚ)\b', text)
        cleanedPKTypes = [re.sub(r'\s*παρ\.\s*\d+', '', m[0], flags=re.IGNORECASE) for m in matchPKTypes]
        matchPKTypesFirst = re.findall(r'(ΠΚ)\s*(\d+(?:\s*,\s*\d+)*)', text)

        result["ΚΠΔ"].extend(cleanedKPDTypes)
        result["ΚΠΔ"].extend(matchKPDTypes)
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


decision1 = requests.get(neededUrl + "/" + anchors[2].get("href"))
decision1.encoding = decision1.apparent_encoding

decision1Soup = BeautifulSoup(decision1.text, "html.parser")

pNeeded = decision1Soup.find_all("p")[1]
#returns decision's number and year taken
match1 = re.search(r'Αριθμός\s+(?P<number>\d+)\s*/\s*(?P<year>\d+)', pNeeded.get_text())
finalResult["number"].append(match1.group("number"))
finalResult["year"].append(match1.group("year"))

#finds the section and department of the decision
match2 = re.search(r"(?P<section>Β\d)'\s+(?P<department>[Α-Ωά-ώ]+)", pNeeded.get_text())
finalResult["department"].append(match2.group("department"))
finalResult["department number"].append(match2.group("section"))

#finds the sentence which includes all the participating judges
matchJudgesText = re.search(r"Συγκροτήθηκε από τους δικαστές,.*?[\.]", pNeeded.get_text())
finalResult["judges"].append(matchJudgesText.group())

#finds the first text needed
matchText1 = re.search(r'((?:Τ\s*Ο\s*Δ\s*Ι\s*Κ\s*Α\s*Σ\s*Τ\s*Η\s*Ρ\s*Ι\s*Ο\s*Τ\s*Ο\s*Υ\s*Α\s*Ρ\s*Ε\s*Ι\s*Ο\s*Υ\s*Π\s*Α\s*Γ\s*Ο\s*Υ)[\s\S]*?)(?=Συγκροτήθηκε από τους δικαστές,)', pNeeded.get_text())
clean_result = re.sub(r'\s+', ' ', matchText1.group(0)).strip()
finalResult["entry text"].append(clean_result)

#finds the second text needed
matchText2 = re.search(r'(ΓΙΑ ΤΟΥΣ ΛΟΓΟΥΣ ΑΥΤΟΥΣ[\s\S]*)', pNeeded.get_text())
clean_result = re.sub(r'\s+', ' ', matchText2.group(0)).strip()
finalResult["final text"].append(clean_result)

result = findArticleIdentifiers(match2.group("department"), pNeeded.get_text())
finalResult["ΑΚ"].append(result["ΑΚ"])
finalResult["ΚΠΔ"].append(result["ΚΠΔ"])
finalResult["ΚΠολΔ"].append(result["ΚΠολΔ"])
finalResult["ΠΚ"].append(result["ΠΚ"])


#i have to subtitute manually the παρ. number text with blank text
driver.quit()

print("\nSaving data...")
with open(f"data.csv", "w", encoding="utf-8") as f:
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
