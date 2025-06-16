from bs4 import BeautifulSoup
from req import add_task
import os
import requests
from collections import defaultdict
from urllib.parse import urljoin
from cert_load import ensure_ca_certificate
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def init_bs(source):
    soup = BeautifulSoup(source,'html.parser')
    return soup

def find_id(soup):
    id_spans = soup.find_all('span', class_='canselect')
    texts = [span.get_text() for span in id_spans]
    print(texts)
    return texts

def find_question(soup):
    conditions = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        hint_div = block.find('div', class_='hint')
        if hint_div:
            condition = hint_div.get_text(strip=True)
            conditions.append(condition)
    print(len(conditions))
    return conditions

def find_text(soup):
    question_texts = []
    question_blocks = soup.find_all('div', class_='qblock')
    for block in question_blocks:
        cell_0 = block.find('td', class_='cell_0')
        if cell_0:
            text = cell_0.get_text(separator=' ', strip=True)
            question_texts.append(text)
    print(len(question_texts))
    return question_texts

def find_themes(soup):
    themes_on_page = []
    themes = soup.find_all('td', class_='param-row')
    for theme in themes:
        theme_text = theme.get_text(strip=True)
        themes_on_page.append(theme_text)
    print(len(themes_on_page))
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
    print(len(response_types))
    return response_types

def find_answer_options(soup):
    """
    Parses HTML content to extract the answer options for each question.

    Args:
        html_content: A string containing the HTML of the webpage.

    Returns:
        A list of lists, where each inner list contains the answer
        options for a single question.
    """
    question_blocks = soup.find_all('div', class_='qblock')
    
    final_options_list = []

    for block in question_blocks:
        options = []
        
        # type 1: 2th part of exam
        hint_div = block.find('div', class_='hint')
        if hint_div and "Дайте развернутый ответ" in hint_div.get_text():
            options.append("Развернутый ответ (нет вариантов)")
            final_options_list.append(options)
            continue

        # type 2 (radio buttons)
        radio_buttons = block.find_all('input', {'type': 'radio'})
        if radio_buttons:
            distractors = block.find_all('tr', class_='active-distractor')
            for distractor in distractors:
                text_cell = distractor.find('td', align='left')
                if text_cell:
                    option_text = text_cell.get_text(strip=True)
                    options.append(option_text)
            final_options_list.append(options)
            continue
            
        # type 3: choose from list
        select_inputs = block.find_all('select')
        if select_inputs:
            list_header = block.find('b', text=lambda t: t and 'Список слов' in t)
            if list_header:
                table = list_header.find_parent('table')
                if table:
                    option_rows = table.find_all('tr')[1:] 
                    for row in option_rows:
                        cells = row.find_all('td')
                        if len(cells) > 1:
                            option_text = cells[1].get_text(strip=True)
                            options.append(option_text)
                    final_options_list.append(options)
                    continue

        # type 4:short answer
        text_input = block.find('input', {'type': 'text'})
        if text_input:

            possible_options_table = block.find('table', class_='MsoNormalTable')
            if possible_options_table:
                rows = possible_options_table.find_all('tr')
                is_option_list = all(')' in row.get_text() for row in rows)
                if is_option_list:
                    for row in rows:
                        options.append(row.get_text(separator=' ', strip=True))
                    final_options_list.append(options)
                    continue

            options.append("Текстовое поле для краткого ответа")
            final_options_list.append(options)
            continue

        # if error:
        if not options:
            options.append("Не удалось определить варианты ответа")
            final_options_list.append(options)
            
    return final_options_list

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
                response = requests.get(img_url, timeout=5,verify=cert,headers=headers)
                response.raise_for_status()
                with open(img_path, "wb") as f:
                    f.write(response.content)
                image_list.append(img_path)
                print(f"downloaded: {img_path}")
            except Exception as e:
                print(f"error while downloading: {img_url}: {e}")
                image_list.append(None)
        else:
            print('None added')
            image_list.append(None)
    print(len(image_list))
    return image_list
def check_lists_equal_length(*lists):    
    first_len = len(lists[0])
    return all(len(lst) == first_len for lst in lists[1:])

def concatenate(source):
    soup = init_bs(source)
    task_ids = find_id(soup)
    texts = find_question(soup)
    answer_options = find_answer_options(soup)
    type_answers = find_type_answer(soup)
    themes = find_themes(soup)
    img = find_image(soup)
    print(f"\n\n\n\n\n\n\n\n{task_ids}\n{answer_options}\n\n\n\n\n")
    print(f'{type(task_ids)},{type(texts)},{type(answer_options)},{type(type_answers)},{type(themes)},{type(img)}')
    print(f'{len(task_ids)},{len(texts)},{len(answer_options)},{len(type_answers)},{len(themes)},{len(img)}') # temporary
    print('images downloaded!')
    if check_lists_equal_length(task_ids,texts,answer_options,type_answers,themes,img):
        for i in range(len(img)): #all lists equal and no diff what we need use
            add_task(task_ids[i],texts[i],answer_options[i],type_answers[i],themes[i],img[i])
            print('added page in db!')
    else:
        print('error in parsing!')
