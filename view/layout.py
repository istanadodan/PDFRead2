import PySimpleGUI as pg
import os
from config import get_config

current_directory = get_config('FILE/base_folder')
if current_directory==None or len(current_directory)==0:
    current_directory = os.path.abspath('.')

layout = [
    [
        [pg.Text('도급계약서 변환', size=(None, 1), pad=(1,3))],
        [pg.HorizontalSeparator(color='#808080')]
    ],    
    [
        [pg.Text('파일위치', size=(7,1), pad=(3,6)),
         pg.Input(current_directory, key='-BASE-FOLDER-', size=(15,1), pad=(3,6), expand_x=True),
         pg.FolderBrowse('선택',  pad=(3,6), target='-BASE-FOLDER-')
        ], 
        [
          pg.Stretch(),          
          pg.Checkbox('html변환', default=False, key='-HTML_YN-'),          
        ]       
    ],        
    [
        [
        pg.Push(),
        pg.Button('START', size=(13,1), key='-START-',pad=(3,9)), 
        pg.Button('STOP', size=(6,1), key='-STOP-',pad=(3,9), disabled=True), 
        pg.Button('EXIT', size=(8,1), key='-EXIT-',pad=(3,9)),
        pg.Push()
        ],
        [pg.HorizontalSeparator(color='#404040')],        
    ],
    [
        [
        pg.Text('대기상태', key='-PG-V-'),
        pg.ProgressBar(max_value=100, orientation='h', size=(100,18), border_width=1, key='-PG-', bar_color=('yellow','black'))
        ],
        [pg.HorizontalSeparator(color='#404040')]
    ],
    [
        pg.Text('', expand_x=True, key='-PG-S-', font = ('Helvetica', 8), text_color='red', background_color='#d5d5c5', pad=(5,1)),
    ]
]