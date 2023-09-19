import pandas as pd
from datetime import datetime
import os

def save_data(logger, data): #방송사별 저장
    now = datetime.now().strftime(r'%Y%d%m_%H%M%S')    
    files = data.keys()
    
    if len(files) == 0 :
        return
    else :
        for file in files:
            df = pd.DataFrame(data[file])
            df.to_excel(rf'C:\퍼즐시스템즈\과제_0807_KJH\resource\output\{file}_{now}.xlsx')    
            logger.info(f'output: {file}_{now}.xlsx')
      