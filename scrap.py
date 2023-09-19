from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import time
import pandas as pd

# scrap_item - get_links_News - get_info - news_date 실행후 딕셔너리 형태의 데이터로 return

# 크롬 드라이버 실행
options=webdriver.ChromeOptions()
driver=webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{"source":"""Object.defineProperty(navigator, 'webdriver',{get: () => undefined})"""})
driver.implicitly_wait(10)

# News 링크 가지고 오기
def get_links_News(logger, name): # news 링크 가져오기
    logger.info(f'Start {name} NEWS')
    now = datetime.now().strftime(r'%Y%m%d')
    links=[]
    if name=='KBS1':
        query = f'https://news.kbs.co.kr/vod/program.do?bcd=0001&ref=pGnb#{now}&1'
        driver.get(query)
        time.sleep(2)
        items=driver.find_elements(By.XPATH, '//*[@id="thumbnailNewsList"]/li/a')
        
        if not items: #오늘 날짜 확인
            logger.info(f'No items {name} on {now}.')
            return links
            
    elif name == 'MBC':
        query = 'https://imnews.imbc.com/replay/2023/nwdesk/'
        driver.get(query)
        time.sleep(2)
        items = driver.find_elements(By.XPATH,'//*[@id="content"]/section/div[2]/div[5]/ul/li/a') 
        
    elif name == 'SBS': #오늘 날짜 확인
        query = f'https://news.sbs.co.kr/news/programMain.do?prog_cd=R1&broad_date={now}&plink=CAL&cooper=SBSNEWS'
        driver.get(query)
        time.sleep(2)
        items=driver.find_elements(By.XPATH, '//*[@id="article-list"]/li/a')
        
        if not items:
            logger.info(f'No items {name} on {now}.')
            return links
        
    elif name == 'JTBC': #오늘 날짜 확인(뉴스룸 다시보기)
            query = f'https://news.jtbc.co.kr/Replay/news_replay.aspx?fcode=PR10000403&strSearchDate={now}'
            driver.get(query)
            time.sleep(2)
            items=driver.find_elements(By.XPATH, '//*[@id="form1"]/div[4]/div[1]/div[2]/ul/li/div[2]/dl/dt/a')[2:]
            # 뉴스룸다시보기/오늘의 주요뉴스 외 기사 검색
            
            if not items:
                logger.info(f'No items {name} on {now}.')
                return links
    
    elif name == 'MBN':
        query = 'https://www.mbn.co.kr/vod/programContents/552/2636'
        driver.get(query)
        time.sleep(2)
        driver.find_element(By.ID,"btMore").click()    # 더보기 클릭
        items = driver.find_elements(By.CSS_SELECTOR,'#pge_vod > ul > li > a')  
      
    for item in items:
        links.append(item.get_attribute('href')) 
        print(f"links : {item.get_attribute('href')}")  
              
    return links

def news_date(keyword, date): # 날짜 전처리 하기
    if keyword == 'KBS1':
        date = date.split(' ')
        return date[1]
    elif keyword == 'MBC':
        date = date.split(' ')
        return date[1].replace('-','.')
    elif keyword == 'SBS' :
        date = date.split(' ')
        return date[0]
    elif keyword == 'JTBC' :
        date = date.split(' ')    # 입력 2023-08-08 19:56 이런형태
        return date[1].replace('-','.')
    elif keyword == 'MBN':
        return date     
    
def get_info(logger, link, keyword): # 개별 뉴스 item 
    item = {}
    logger.info(f'move to {link}')
    try: # timeout 관련 예외처리
        driver.get(link)
    except TimeoutException:
        logger.info(f'timeout - refresh : {link}')
        driver.refresh()
        driver.get(link)
    
    if keyword == 'KBS1':
        date = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[1]/div[1]/span/em[1]').text
        title = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[1]/div[1]/h5').text.strip() #제목
        contents = driver.find_element(By.ID,"cont_newstext" ).text #본문
    elif keyword == 'MBC':
        date = driver.find_element(By.XPATH,'//*[@id="content"]/div/section[1]/article/div[1]/div[3]/div[1]/span[1]').text
        title = driver.find_element(By.XPATH,'//*[@id="content"]/div/section[1]/article/div[1]/h2').text.strip()
        contents = driver.find_element(By.CLASS_NAME,'news_txt').text
    elif keyword == 'SBS' :
        date = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div[2]/div[1]/div/div[1]/div[2]/span[1]').text
        title = driver.find_element(By.ID,'news-title').text.strip()
        contents = driver.find_element(By.CLASS_NAME,'text_area').text
    elif keyword == 'JTBC' :
        date = driver.find_element(By.XPATH,'//*[@id="articletitle"]/div/span/span').text
        title = driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/div/form/div[6]/div[1]/div/h3').text.strip()
        contents = driver.find_element(By.XPATH,'//*[@id="articlebody"]/div[1]').text.replace('키보드 컨트롤 안내','') 
        #'키보드 컨트롤 안내' 삭제
    elif keyword == 'MBN' :
        date = driver.find_element(By.XPATH,'//*[@id="news_view"]/div/h1/p').text
        title = driver.find_element(By.ID,'news_view').find_element(By.CLASS_NAME,'wrp').find_element(By.CLASS_NAME,'article_tlt')
        title_date = title.find_element(By.CLASS_NAME,'daily_date')
        von = title.get_attribute("innerHTML").replace(title_date.get_attribute("outerHTML"),"")
        # 상위 ID(news_view) -> Class('wrp') -> Class('article_tlt') 까지 찾아내려감
        # Class 'article_tlt'안에 'daily_date' date 값이 있어 따로 변수에 저장
        # von 변수에 Class('article_tlt')에서 'daily_date' date 값을 replace를 이용해서 없애줌
        title = von.strip()
        contents = driver.find_element(By.XPATH,'//*[@id="textArea"]/p').text
             
    item['date'] = news_date(keyword, date)
    item['title'] = title
    item['contents'] = contents
    
    logger.info(f'날짜:{date}')
    logger.info(f'제목: {title}')
    logger.info(f'내용: {contents}')
    
    return item

def scrap_items(logger): # 스크랩 실행하기
    stations = ['KBS1', 'MBC', 'SBS', 'JTBC', 'MBN'] 
    result = {}
    for name in stations:
        links = get_links_News(logger, name)
        data = []
        
        for i, link in enumerate(links):
            tmp_data = get_info(logger, link, name)            
            
            if (name=='MBC' and i == 0) or (name=='MBN' and i == 0) :
                # MBC/MBN 뉴스 날짜 비교하기
                if tmp_data['date'].replace('.','') != datetime.now().strftime(r'%Y%m%d') :
                    break
            
            data.append(get_info(logger, link, name))
        result[name] = data    
    
    return result

