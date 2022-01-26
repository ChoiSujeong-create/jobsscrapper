import csv

def save_to_file(jobs):
  file = open("jobs.csv",mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","company","location","link"])
  #jobs안에 있는 각 job을 가지고
  for job in jobs:
    #row를 작성
    #job이 가진 값을 리스트로 만들어 row로 저장
    writer.writerow(list(job.values()))
  return