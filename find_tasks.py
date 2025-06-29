from bs4 import BeautifulSoup
from req import add_task
import os
import requests
from urllib.parse import urljoin
from cert_load import ensure_ca_certificate
import logging

logger = logging.getLogger(__name__)
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def init_bs(source):
    soup = BeautifulSoup(source,'html.parser')
    return soup

def find_id(soup):
    id_spans = soup.find_all('span', class_='canselect')
    texts = [span.get_text() for span in id_spans]
    logger.debug(f'id found!{texts}')
    return texts

def find_question(soup):
    conditions = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        hint_div = block.find('div', class_='hint')
        if hint_div:
            condition = hint_div.get_text(strip=True)
            conditions.append(condition)
    logger.debug(f'question found {conditions}')
    return conditions

def find_text(soup):
    question_texts = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        cell_0 = block.find('td', class_='cell_0')
        if cell_0:
            text = cell_0.get_text(separator=' ', strip=True)
            question_texts.append(text)
    logger.debug(f'question text found {question_blocks}')
    return question_texts

def find_themes(soup):
    themes_on_page = []
    themes = soup.find_all('td', class_='param-row')
    for theme in themes:
        theme_text = theme.get_text(strip=True)
        themes_on_page.append(theme_text)
        logger.debug(f'themes found {themes_on_page}')
    return themes_on_page

def find_type_answer(soup):
    response_types = []
    task_info_panels = soup.find_all('div', class_='task-info-panel')
    for panel in task_info_panels:
        table = panel.find('div', class_='task-info-content').find('table')
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2 and cells[0].get_text(strip=True) == 'Тип ответа:':
                response_type = cells[1].get_text(strip=True)
                response_types.append(response_type)
                break
    logger.debug(f'response types found {response_types}')
    return response_types

def find_answer_options(soup):
    question_blocks = soup.find_all("td", class_="varinats-block")
    ans = []
    for block in question_blocks:
        match True:
            case _ if block.find('option'):
                table_variants = block.get_text(strip=True)
                ans.append(f'TABLE {str(table_variants)}')
                logger.debug(f'TABLE {str(table_variants)}')
            
            case _ if block.find('input', type="text"):
                ans.append("TEXT FIELD")
            
            case _ if block.find('input', type="radio"):
                radio_variants = block.get_text()
                logger.debug(f"RADIO VARIANTS {radio_variants}")
                ans.append(f"RADIO VARIANTS {radio_variants}")
            
            case _:
                ans.append('NoneType')
    logger.debug(f'answer options found {ans}')
    return ans 
   
def find_image(soup):

    output_dir = ".cache/images"
    os.makedirs(output_dir, exist_ok=True)
    base_url = "https://oge.fipi.ru"
    image_list = []
    qblocks = soup.find_all("div", class_="qblock")
    cert = ensure_ca_certificate()
    for qblock in qblocks:
        guid = qblock.find("input", {"name": "guid"})["value"] if qblock.find("input", {"name": "guid"}) else "unknown"
        
        cell_0 = qblock.find("td", class_="cell_0")
        img_tag = cell_0.find("img") if cell_0 else None
        
        if img_tag and img_tag.get("src"):
            img_url = urljoin(base_url, img_tag["src"])
            
            img_extension = os.path.splitext(img_url)[1] or ".jpg"
            img_filename = f"{guid}{img_extension}"
            img_path = os.path.join(output_dir, img_filename)
            
            try:
                response = requests.get(img_url, timeout=30,verify=cert,headers=headers)
                response.raise_for_status()
                with open(img_path, "wb") as f:
                    f.write(response.content)
                image_list.append(img_path)
            except Exception:
                image_list.append(None)
        else:
            image_list.append(None)
    logger.debug('image found {image_list}')
    return image_list

def check_lists_equal_length(*lists):    
    first_len = len(lists[0])
    return all(len(lst) == first_len for lst in lists[1:])

def concatenate(source,page_num):
    soup = init_bs(source)
    task_ids = find_id(soup)
    texts = find_text(soup)
    question = find_question(soup)
    answer_options = find_answer_options(soup)
    type_answers = find_type_answer(soup)
    themes = find_themes(soup)
    img = find_image(soup)

    if check_lists_equal_length(task_ids,texts,question,answer_options,type_answers,themes,img):
        for i in range(len(img)): #all lists equal and no diff what we need use
            add_task(task_ids[i],texts[i],question[i],answer_options[i],type_answers[i],themes[i],img[i])
            logger.debug(f'task {task_ids[i]} added')
        logger.info('all concatenated')
    else:
        logger.error(f'error in concatenating on page {page_num} !Parser not find element on page')



 