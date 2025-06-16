from bs4 import BeautifulSoup
from req import add_task
import os
import requests
from urllib.parse import urljoin
from cert_load import ensure_ca_certificate

def init_bs(source):
    soup = BeautifulSoup(source,'html.parser')
    return soup

def find_id(soup):
    id_span = soup.find_all('span', class_='canselect')
    return id_span

def find_question(soup):
    conditions = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        hint_div = block.find('div', class_='hint')
        if hint_div:
            condition = hint_div.get_text(strip=True)
            conditions.append(condition)
    return conditions

def find_text(soup):
    question_texts = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        cell_0 = block.find('td', class_='cell_0')
        if cell_0:
            text = cell_0.get_text(separator=' ', strip=True)
            question_texts.append(text)
    return question_texts

def find_themes(soup):
    themes_on_page = []
    themes = soup.find_all('td',class_='param-row')
    for theme in themes:
        themes_on_page.append(theme)
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
    return response_types

def find_answer_options(soup):
    ans_opt = soup.find_all('td',class_='varinats-block') #xd fipi just piece of shit
    for option in ans_opt:
        if option.find('table'):
            return option.get_text(strip=True)
        elif option.find('input',type="text"):
            return 'text_field'
        elif option.find('input',type="radio"):
            return option.get_text(strip=True)
        else: return 'error:answer option not detected!'
def find_image(soup):

    output_dir = "images"
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
                response = requests.get(img_url, timeout=5,verify=cert)
                response.raise_for_status()
                with open(img_path, "wb") as f:
                    f.write(response.content)
                image_list.append(img_path)
                print(f"downloaded: {img_path}")
            except Exception as e:
                print(f"error while downloading: {img_url}: {e}")
                image_list.append(None)
        else:
            image_list.append(None)
    return image_list
def check_lists_equal_length(*lists):
    lengths = set(len(lst) for lst in lists)
    return len(lengths) == 1

def concatenate(source):
    soup = init_bs(source)
    task_ids = find_id(soup)
    texts = find_question(soup)
    answer_options = find_answer_options(soup)
    type_answers = find_type_answer(soup)
    themes = find_themes(soup)
    img = find_image(soup) # temporary
    if check_lists_equal_length(task_ids,texts,answer_options,type_answers,themes):
        for i in len(img): #all lists equal and no diff what we need use
            add_task(task_ids[i],texts[i],answer_options[i],type_answers[i],themes[i],img[i])
            return 'added page in db!'
    else:
        return 'error in parsing!'
    #def add_task(task_id,text,answer_options,type_answer,themes,img,created_at,updated_at):
