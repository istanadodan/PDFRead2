import PySimpleGUI as pg
from service.converter import convert
import queue, threading

class View:
    def __init__(self, title:str):
        from .layout import layout
        self.window:pg.Window=pg.Window(title, layout, resizable=True, size=(315,215),element_padding=(5,1),finalize=True)        

    def show(self):        
        q = queue.Queue()
                
        while True:
            event, values = self.window.read()
            
            if event in ('-EXIT-', pg.WIN_CLOSED, pg.WIN_X_EVENT):
                q.put('stop')
                break
            
            elif event=='-START-':
                down_directory = values['-BASE-FOLDER-']
                if len(down_directory)==0:
                    pg.popup_error('처리대상 폴더명이 입력되지 않았습니다')
                    continue
                self.window['-PG-V-'].update('개시상태')
                self.window['-PG-S-'].update('')
                self.window['-PG-'].update(0)
                
                self.directory = down_directory.replace('/','\\')                
                th = threading.Thread(target=convert, args=[self.directory, q, self.window])
                th.start()     
                
                self.window['-START-'].update(disabled=True)
                self.window['-STOP-'].update(disabled=False)
                
            elif event=='-STOP-':
                q.put('stop')                
                self.window['-PG-V-'].update('작업중지')
                self.window['-START-'].update(disabled=False)
                self.window['-STOP-'].update(disabled=True)
                
            elif event=='-ERR-':                
                pg.popup_error(values[event]) 
                self.window['-START-'].update(disabled=False)
                self.window['-STOP-'].update(disabled=True)
            
            elif event=='-PG-S-':
                self.window['-PG-S-'].update(f'{values["-PG-S-"]}')
                
            elif event=='-PG-V-':
                self.window['-PG-V-'].update(f'{values["-PG-V-"]}')
                
            elif event=='-PG-':                
                self.window['-PG-'].update(values['-PG-'])
                
            elif event=='-COMPLETE-':
                self.window['-PG-V-'].update('처리완료')
                self.window['-PG-S-'].update(f'{values["-COMPLETE-"]} 완료되었습니다.')
                self.window['-START-'].update(disabled=False)
                self.window['-STOP-'].update(disabled=True)
            
        self.window.close()