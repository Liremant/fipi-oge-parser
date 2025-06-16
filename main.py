import logging
from get_source import get_src,get_url
from find_tasks import concatenate

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', encoding='utf-8')
def main():
    concatenate(get_src(get_url()))
    print('concatenated and added into db')
if __name__ == "__main__":
    
    main()



