import PySimpleGUI as pg
from glob import glob
import os
import re
import pandas as pd
from model.bs_model import Model
import logging

OUTPUT_COLUMN_NAMES = ['프로젝트코드','프로젝트명','현장주소','공사기간','총금액']
OUTPUT_FILENAME = '도급계약서_추출결과'

log = logging.getLogger(__name__)
parser = Model()

def convert(directory, q, window):
    """_summary_
        args=[self.directory, q, self.window, self.context]
    """        
    HTML_YN = window['-HTML_YN-'].get()
    
    file_generator = glob(os.path.join(directory,'*.pdf'))
    
    total_cnt = len(file_generator)
    if total_cnt ==0:
        window.write_event_value('-COMPLETE-', f'PDF파일이 존재하지 않습니다')        
        return
    
    df = pd.DataFrame()
    complete_cnt = 0
    count = 0    
    keyMap = dict(type1=[11,12,14,14,15], type2=[13,14,16,16,17], type3=[8,9,11,12,13])
    
    try:
            
        for file_path in file_generator:
            filename = os.path.basename(file_path)            
            send_message(window, f'{filename} 처리 중...')    
            
            result = parser.read_pdf(file_path)        
            if result==False:
                show_error(window)
                return        
            
            if parser.find_byTxt('span', '1\.\s*공사명\s*\*\s*\(?\w+'):
                doc_type ='type3'
                
            elif parser.find_byTxt('span', '도급계약서'):
                doc_type ='type2'
            else:
                doc_type ='type1'
            
            pos_list = keyMap[doc_type]
            
            #프로젝트코드
            code = filename[:12]
            #프로젝트명
            name= pickOne(parser.find_byTag('div',pos_list[0]), doc_type)
            #프로젝트 현장주소
            place= pickOne(parser.find_byTag('div',pos_list[1]), doc_type)
            #공사기간
            period = pickOne(parser.find_byTag('div',pos_list[2]), doc_type)
            #총금액
            amount = pickOne(parser.find_byTag('div',pos_list[3],False), doc_type, 2)
            if not amount:
                amount = pickOne(parser.find_byTag('div',pos_list[4],False), doc_type)
            
            if HTML_YN:
                with open(f'{file_path[:-4]}.html', 'w', encoding='utf-8') as f:
                    f.write(parser.html)
                        
            if None in (code, name, place, amount) or amount.strip()=='' or amount.strip().replace(',','').isnumeric()==False:
                show_error(window, f'[데이터취득 불가] {filename}') 
            else:
                df = df.append(pd.Series([code,name,place,period,int(amount.replace(',',''))]), ignore_index=True)        
                
                complete_cnt +=1
                send_message(window, f'{filename} 처리완료')                
                log.debug(f'c={complete_cnt}')
                
            count +=1            
            window.write_event_value('-PG-V-', f'{count} / {total_cnt}') 
            window.write_event_value('-PG-', int(count / total_cnt * 100))            
            
            check_stop(q)
        
        if len(df)>0:
            df.columns=OUTPUT_COLUMN_NAMES 
            df = df.sort_values(by="프로젝트코드", ascending=True)
            df.index = pd.RangeIndex(start=1, stop=complete_cnt+1, name="번호")
            log.debug(f'{df.head()}')
        
            df.to_excel(os.path.join(directory,OUTPUT_FILENAME+'.xlsx'), sheet_name="도급계약현황")
                
        window.write_event_value('-COMPLETE-', f'{complete_cnt}건')         
        
    except Exception as e:        
        show_error(window, e)
        return
    
def check_stop(q):
    if not q.empty() and q.get(block=False)=='stop':
        q.task_done()
        raise Exception('강제 중단')

def pickOne(sent:str, docType, order:int=1)->str:
    if not sent:
        return
    arr = sent.split(';')
    if len(arr) < order:
        return
    txt = arr[order-1]
    r = re.sub('[^\w|,|~|\s+\w+]','', txt)    
    if not r:
        return
    
    if docType =='type3':
        r = re.sub('\d\s\w+\s+','', r)        
    return r

def send_message(view:pg.Window, message:str):
    log.debug(message)
    view.write_event_value('-PG-S-', message)
    

def change_state(view:pg.Window, state:str):
    log.debug(f'state={state}')
    view.write_event_value('-PG-V-', state)
    
def show_error(window:pg.Window, message)->None:    
    log.debug(message)
    window.write_event_value('-ERR-',message)