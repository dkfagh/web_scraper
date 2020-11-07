import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    # URL에 request를 요청
    result = requests.get(URL)

    # result에서 html코드를 추출
    soup = BeautifulSoup(result.text, "html.parser")

    # soup에서 clss가 pagination인 div를 검색
    pagination = soup.find("div", {"class": "pagination"})

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


def extract_job(html):
    # 입력받은 html코드에서 class가 title인 h2를 검색하고 그 결과에서 a태그를 검색하여 어트리뷰트 title을 추출
    title = html.find("h2", {"class": "title"}).find("a")["title"]

    # 입력받은 html코드에서 class가 company인 span 결과를 검색
    company = html.find("span", {"class": "company"})

    if company:
        # 검색된 company에서 a태그를 검색
        company_anchor = company.find("a")

        # company_anchor가 존재하면
        if company_anchor is not None:
            company = str(company_anchor.string)
        # company_anchor가 존재하지 않으면
        else:
            company = str(company.string)
        # company의 문자 또는 문자열의 공백을 제거
        company = company.strip()
    else:
        company = None

    # 입력받은 html코드에서 class가 recJobLoc인 div를 검색하고 어트리뷰트 data-rc-loc을 추출
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    # 입력받은 html코드에서 어트리뷰트 data-jk를 추출
    job_id = html["data-jk"]

    # title과 company를 배열로 return
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }


# 변수로 입력받은 last_page의 크기만큼 반복 (0 ~ last_page)
def extract_jobs(last_page):

    # 빈 배열 jobs 생성
    jobs = []

    # 반복문으로 동적인 url값을 생성하여 result값에 저장 (last_page의 값 만큼 반복)
    for page in range(last_page):
        print(f"scrapping page {page}")
        # URL&start={page*LIMIT}에 request를 요청
        result = requests.get(f"{URL}&start={page*LIMIT}")
        # result에서 html코드를 추출
        soup = BeautifulSoup(result.text, "html.parser")

        # 추출한 soup에서 class가 jobsearch-SerpJobCard인 div를 전부 검색
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        # 반복문을 통해 extract_job의 return값을 jobs 배열에 저장
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()

    jobs = extract_jobs(last_page)

    return jobs
