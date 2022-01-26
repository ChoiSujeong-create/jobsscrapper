import requests
from bs4 import BeautifulSoup
LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit={LIMIT}"

def get_last_pages():
  result = requests.get(URL)
  #print(indeed_result.text) 
  #모든 html 가져오기
  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("ul", {"class":"pagination-list"})

  #page는 list
  links = pagination.find_all('span')
  spans =[]
  for link in links[0:-2]:
    spans.append(int(link.string))

  #제일 큰 페이지 숫자 추출
  max_page = spans[-1]
  return max_page

def extract_job(html):
    jobTitle = html.find("h2",{"class":"jobTitle"})
    title = jobTitle.find("span").string
    company = html.find("span",{"class":"companyName"})
    if title == "new":
      title = jobTitle.find_all("span")[1].string
    if company is not None:
      company = company.string
    else:
      company = None
    location = html.find("div",{"class":"companyLocation"}).string
    job_id = html["data-jk"]
    return {'title':title, 'company':company, 'location':location, "link":f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"}


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed : Page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a",{"class":"tapItem"})
    # ("div", {"class": "job_seen_beacon"}) -> ("a",{"class":"tapItem"}) : data-jk가 job_seen_beacon보다 상위에 있기 때문
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_pages = get_last_pages()
  jobs = extract_jobs(last_pages)
  return jobs

  