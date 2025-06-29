from get_source import init_driver, get_page_frame, get_url, get_current_page, go_to_next_page, resume_prev
from find_tasks import concatenate
from req import check_database_data
import logging
import sys



def init_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'), # DEBUG by default  
            logging.StreamHandler(sys.stdout)  
        ] 
    )

    # Adjust console handler to WARNING level
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(logging.WARNING)

    # Configure SQLAlchemy logger
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_file_handler = logging.FileHandler('sqlalchemy.log', encoding='utf-8')
    sql_file_handler.setLevel(logging.DEBUG)  # Log DEBUG and above to sqlalchemy.log
    sql_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    sql_logger.addHandler(sql_file_handler)
    sql_logger.setLevel(logging.DEBUG)
    sql_logger.propagate = True  # Propagate to root for console output of WARNING and above

def load_page(driver):
    page_num = get_current_page(driver)
    source = get_page_frame(driver, page_num)
    concatenate(source,page_num)
    go_to_next_page(driver,page_num)

def check_prev_parse(driver):
    count = check_database_data()
    if count !=0:
        resume_prev(driver,count)
def main():
    init_logging()
    has_page = True
    url = get_url()
    driver = init_driver(url)
    check_prev_parse(driver)
    while has_page:
        load_page(driver)

if __name__ == "__main__":
    main()