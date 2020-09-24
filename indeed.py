import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)

  # indeed_result에서 html코드를 추출
  soup = BeautifulSoup(result.text, "html.parser")

  # indeed_soup에서 clss가 pagination인 div를 검색
  pagination = soup.find("div", {"class":"pagination"})

  # pagination에서 anchor태그를 전부 검색
  links = pagination.find_all('a')

  # 빈 배열 pages 생성
  pages = []

  # 반복문으로 pages배열에 anchor태그의 string값을 검색 후 int형으로 변환하여 저장
  for link in links[:-1]:
    pages.append(int(link.string))

  # 마지막 페이지
  max_page = pages[-1]

  return max_page

def extract_indeed_jobs(last_page):

  # 빈 배열 jobs 생성
  jobs = []

  # 반복문으로 동적인 url값을 생성하여 result값에 저장 (last_page의 값 만큼 반복)
  # for page in range(last_page):
  result = requests.get(f"{URL}&start={0*LIMIT}")
  # indeed_result에서 html코드를 추출
  soup = BeautifulSoup(result.text, "html.parser")

  # 일자리 목록을 추출
  results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
  
  # 반복문을 통해 추출한 일자리 목록에서 title만 따로 추출
  for result in results:
    title = result.find("h2", {"class":"title"}).find("a")["title"]
    # 추출한 title에서 span태그의 class가 company인 결과를 추출
    company = result.find("span",{"class":"company"})
    # 추출한 company에서 a태그를 추출
    company_anchor = company.find("a")
    # company_anchor가 존재하면
    if company_anchor is not None:
      company = str(company_anchor.string)
    # company_anchor가 존재하지 않으면
    else:
      company = str(company.string)
    # company의 문자 또는 문자열의 공백을 제거
    company = company.strip()
    
    print(title, company)
  return jobs