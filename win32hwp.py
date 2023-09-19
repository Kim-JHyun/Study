import time
import os
from datetime import datetime
import win32com.client as win32
import pandas as pd

def init(logger, data):
    names = data.keys()
    for name in names:
        write_hwp(logger,data,name)
        time.sleep(0.2)
        
def write_hwp(logger, data, name): 
    
    df = pd.DataFrame(data[name])
    now = datetime.now().strftime("%Y. %m. %d.")
    day = datetime.now().weekday() 
    dateDict = {0: '월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
             
    # 로깅 데이터 설정
    logger.info('Start Open sample.hwp')
        
    hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
    hwp.XHwpWindows.Item(0).Visible = True  # 숨김해제
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")
        
    hwp.Open(r'C:\퍼즐시스템즈\과제_0807_KJH\resource\input\sample.hwp')
    
    if len(df) == 0 : # scarp.py 에서 반환된 데이터가 없을시
        hwp.PutFieldText("날짜", now + "(" + dateDict[day]+ ")")
        time.sleep(0.2)
        hwp.Run("ParagraphShapeAlignCenter")
        time.sleep(0.2)
        hwp.PutFieldText("내용",f'{now} 일자 {name} 뉴스가 없습니다.')
        
    else :
        hwp.HAction.Run("CopyPage")#한글 페이지 복사
        time.sleep(0.2)
        
        for i in range(len(df)-1):
            hwp.HAction.Run('PastePage')
            time.sleep(0.2)
            
        for i in range(len(df)):
            date, title, contents = df.iloc[i]
                        
            logger.info(f'write {name} news {title} {i+1} 번째')
            
            hwp.PutFieldText(f"날짜{{{{{i}}}}}", now + "(" + dateDict[day]+ ")")
            time.sleep(0.2)
            
            hwp.MoveToField(f"내용{{{{{i}}}}}") 
            time.sleep(0.2)
            
            act = hwp.CreateAction("CharShape") #글자모양
            set = act.CreateSet() # 세트 생성
            act.GetDefault(set) # 세트 초기화
            time.sleep(0.2)
            
            # (08.08 KBS1 News) - 글씨크기 10, 중앙정렬
            news_txt = f"({date} {name} News)\r\n" 
            
            # news_txt양식
            hwp.HAction.Run("CharShapeBold")
            hwp.Run("ParagraphShapeAlignCenter")
            cs = hwp.CharShape
            cs.SetItem("Height",1000)
            hwp.CharShape = cs
            time.sleep(0.2)
            
            # news 텍스트 작성
            act1 = hwp.CreateAction("InsertText")
            pset1 = act1.CreateSet()
            pset1.SetItem("Text",news_txt)
                
            act1.Execute(pset1)
            time.sleep(0.2)
        
            # □ 제목 - 글씨크기 13, 굵게
            title_txt = f"□ {title}\r\n"
            
            hwp.HAction.Run("ParagraphShapeAlignLeft") # 왼쪽정렬
            time.sleep(0.2)
            cs = hwp.CharShape
            cs.SetItem("Height",1300)
            hwp.CharShape = cs
            time.sleep(0.2)
        
            # title 텍스트 작성
            act2 = hwp.CreateAction("InsertText")
            pset2 = act2.CreateSet()
            pset2.SetItem("Text",title_txt)        
            act2.Execute(pset2)
            time.sleep(0.2)
        
            # 글씨크기 11
            contents_txt=f'{contents}'
            contents_txt.replace("\n", "") + '\r\n\r\n'
            cs = hwp.CharShape
            cs.SetItem("Height",1100)
            hwp.CharShape = cs
            time.sleep(0.2)
            
            # contents 텍스트 작성
            act3 = hwp.CreateAction("InsertText")
            pset3 = act3.CreateSet()
            
            pset3.SetItem("Text",contents_txt)        
            act3.Execute(pset3)
            time.sleep(0.2)
        # for 종료    
    
    hwp_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + name + "_" + dateDict[day]
    # 한글 파일 저장을 위해 경로를 지정
    filepath = "C:/퍼즐시스템즈/과제_0807_KJH/resource/output/"
    
    # 한글 파일 저장
    hwp.SaveAs(rf'{filepath}{hwp_filename}.hwp')
    time.sleep(0.2)
    hwp.Clear(3) 
    hwp.Quit()
    logger.info('Process Complete')
    return 
