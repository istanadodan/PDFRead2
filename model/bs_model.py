import io, re
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from bs4 import BeautifulSoup as soup
import logging

logging.getLogger('pdfminer').setLevel(logging.CRITICAL)
    
class Model:

   def __init__(self):
      self.initialize()
      
   def initialize(self):
        self.body=''
        self.html=''
   
   def read_pdf(self, pdf_path:str) -> bool:
      try:
         retstr = io.BytesIO()
         laparams=LAParams()
         with open(pdf_path, 'rb') as fp:               
            extract_text_to_fp(fp, retstr, output_type='html',laparams=laparams)

            report = retstr.getvalue()
            if report:
               self.html = report.decode('utf-8')      
               self.body = soup(self._replace(self.html), 'html.parser')
               
            retstr.close()
            
         return True
            
      except Exception as e:
         print(f'## ERR ## file path={pdf_path}, error={e}')
         return False
   
   def find_byTxt(self, tag_name:str, pattern:str)->bool:
         # if regex:            
         # else:
         #    found_tag = self.body.find(tag_name, text=lambda t: t and pattern in t)
         found_tag = self.body.find(tag_name, text=re.compile(pattern))
         return found_tag !=None
          
   def find_byTag(self, tag_name:str, order:int, unicode=True) -> str:
         tags = self.body.find_all(tag_name)
         if not tags: return
         
         text = tags[order-1].get_text()
         if unicode:
            return text
         else:
            pattern = r'[^\x00-\x7F]+'  # ASCII 범위 이외의 문자 패턴
            return re.sub(pattern, '', text)
                       
   def _replace(self, txt):
      patterns = [('(style=".*?")|(\\n)',''), ('\<br\/?\>',';')]      
      for pattern in patterns:
         txt = re.sub(pattern[0],pattern[1],txt)
      return txt   