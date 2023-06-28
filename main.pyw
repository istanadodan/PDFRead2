from view import View
import logging

def main():
    setup_logging()
    view = View('이트너스 업무용')
    view.show()

def setup_logging():    
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s:%(funcName)s - %(message)s',
        level=logging.DEBUG,
        encoding='utf-8',
        )

if __name__=='__main__':
    main()    