from bs4 import BeautifulSoup

def init_bs(source):
    soup = BeautifulSoup(source,'html.parser')
    return soup

def find_id(soup):
    id_span = soup.find_all('span', class_='canselect')
    ids_on_page = list()
    for span in id_span:
        ids_on_page.append(span)
    return ids_on_page

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
    themes = soup.find_all('td',class_='param-row')
    themes_on_page = list()
    for theme in themes:
        themes_on_page.append(theme)
    return themes_on_page
def find_type_answer(soup):
    tanswer = soup.find_all

def parse_response_types(soup):
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