# rand_scraper

미국의 싱크탱크인 랜드 연구소(The RAND Corporation, https://www.rand.org)의 자료들을 받아오는 크롤러입니다. 랜드 연구소내의 2가지 자료들(Blog post, Reserch paper)들에 대한 자료를 받아옵니다.

## User guide

크롤러의 파이썬 파일은 util.py, scraper.py, parser.py, downloader.py 그리고 scraping_latest_news.py 총 다섯가지로 구성되어 있습니다. 
util.py는 크롤링 한 파이썬의 beautifulsoup 패키지를 받아서 url내의 html정보를 정리하는 등 scraper가 필요한 기본적인 기능을 가지고 있습니다.
parser.py는 모아진 url리스트를 통해서 각 분석들의 제목/일자/내용 등의 문자, 시간 데이터들을 parsing 합니다.
scraper.py는 사이트내의 url 링크들을 get_soup함수를 통해 모아주고, parser를 통해서 json형식으로 변환시킵니다.
downloader.py는 reserch paper와 Brookings papers on economy activity article의 pdf파일을 다운로드 하는 파일입니다.
scraping_latest_news.py는 scraper.py를 통해 만들어진 json파일을 저장시켜줍니다. scraping_latest_news.py파일의 parameter는 다음과 같습니다.

Using Python script with arguments

| Argument name | Default Value | Note |
| --- | --- | --- |
| begin_date | 2018-07-01 | datetime YYYY-mm-dd |
| directory | ./output/ | Output directory |
| max_num | 1000 | Maximum number of news to be scraped |
| sleep | 1.0 | Sleep time for each news |
| verbose | False, store_true | If True use verbose mode |

만일 2018년 7월 1일부터 작성된 자료를 1000개까지 받고 싶다면 다음과 같이 실행코드를 입력해주시면 됩니다.

```
scraping_latest_news.py --begin_date 2018/07/01 --directory ./output --max_num 1000 --sleep 1.0
```
최근 순서대로 크롤링한 파일을 살펴보고 싶을때는 usage.ipynb를 사용하세요.

```
from rand_scraper import yield_latest_report

begin_date = '2018-12-01'
max_num = 10
sleep = 1.0

for i, json_obj in enumerate(yield_latest_report(begin_date, max_num, sleep)):
    title = json_obj['title']
    time = json_obj['date']
    print('[{} / {}] ({}) {}'.format(i+1, max_num, time, title))
```

```
[1 / 10] (2019-03-12 00:00:00) Military Compensation to Support Retention, Performance, and Talent Management
[2 / 10] (2019-03-07 00:00:00) Reducing Disagreements on Gun Policy Through Scientific Research and an Improved Data Infrastructure
[3 / 10] (2019-03-12 00:00:00) The Hidden Components of the North Korean Military Challenge
[4 / 10] (2019-03-12 00:00:00) Increasing Groundwater Reliance in L.A. County Means Dealing with Extensive Contamination
[5 / 10] (2019-03-12 00:00:00) Military Compensation to Support Retention, Performance, and Talent Management
[6 / 10] (2019-03-12 00:00:00) Changes in Outpatient Services and Medication Use Following a Non-fatal Opioid Overdose in the West Virginia Medicaid Program
[7 / 10] (2019-03-12 00:00:00) Responsible E-Prescribing Needs E-Discontinuation
[8 / 10] (2019-03-11 00:00:00) How frequent night-time bathroom visits can negatively impact sleep, well-being and productivity
[9 / 10] (2019-03-11 00:00:00) The Relationship Between Disability Evaluation and Accession Medical Standards
[10 / 10] (2019-03-08 00:00:00) Experiences of Medicaid Programs and Health Centers in Implementing Telehealth
```


## 참고 코드

본 코드는 https://github.com/lovit/whitehouse_scraper를 참조하여 만들어졌습니다.
