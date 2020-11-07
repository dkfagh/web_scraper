import csv


def save_to_file(jobs):
    # 변수 file로 jobs.csv 열기
    # mode=w : 쓰기만 가능
    file = open("jobs.csv", mode="w")
    # 변수 writer에 file을 입력
    writer = csv.writer(file)
    # 첫 행(row) 입력
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        # 파라미터로 받은 jobs의 job에서 각 값들만 뽑아서(divtionary의 value 기능) 리스트화시킨 후 writer로 입력
        writer.writerow(list(job.values()))
    return
