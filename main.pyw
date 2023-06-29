from view.view import View

def main():
    setup_logging()
    
    view = View('이트너스 업무용V1')
    view.show()

def setup_logging():     
    import logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s:%(funcName)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8',
        )

if __name__=='__main__':
    main()    