import cv2
import pyzbar.pyzbar as pyzbar
import requests
from bs4 import BeautifulSoup as BS

# Код категорий с сайта soliq.uz
categories = {'001': ['ПРОЧЕЕ'], '002': ['ПРОДУКТЫ'], '003': ['ПРОЧЕЕ'], '004': ['ПРОДУКТЫ'], '005': ['ПРОДУКТЫ'],
              '006': ['ПРОЧЕЕ'], '007': ['ОВОЩИ'], '008': ['ФРУКТЫ И ОРЕХИ'], '009': ['КОФЕ, САХАР, ЧАЙ И СПЕЦИИ'],
              '010': ['ПРОЧЕЕ'], '011': ['ПРОДУКТЫ'], '012': ['ПРОЧЕЕ'], '013': ['ПРОЧЕЕ'], '014': ['ПРОЧЕЕ'],
              '015': ['ПРОДУКТЫ'], '016': ['ПРОДУКТЫ'], '017': ['КОФЕ, САХАР, ЧАЙ И СПЕЦИИ'], '018': ['ПРОДУКТЫ'],
              '019': ['ПРОДУКТЫ'], '020': ['ПРОДУКТЫ'], '021': ['ПРОДУКТЫ'], '022': ['НАПИТКИ'], '023': ['ПРОЧЕЕ'],
              '024': ['ПРОЧЕЕ'], '025': ['ПРОЧЕЕ'], '026': ['ПРОЧЕЕ'], '027': ['ПРОЧЕЕ'], '028': ['ПРОЧЕЕ'],
              '029': ['ПРОЧЕЕ'], '030': ['ФАРМАЦЕВТИЧЕСКАЯ ПРОДУКЦИЯ'], '031': ['ПРОЧЕЕ'], '032': ['ПРОЧЕЕ'],
              '033': ['ПРОЧЕЕ'], '034': ['ПРОЧЕЕ'], '035': ['ПРОЧЕЕ'], '036': ['ПРОЧЕЕ'], '037': ['ПРОЧЕЕ'],
              '038': ['ПРОЧЕЕ'], '039': ['ПРОЧЕЕ'], '040': ['ПРОЧЕЕ'], '041': ['ПРОЧЕЕ'], '042': ['ПРОЧЕЕ'],
              '043': ['ПРОЧЕЕ'], '044': ['ПРОЧЕЕ'], '045': ['ПРОЧЕЕ'], '047': ['ПРОЧЕЕ'], '048': ['ПРОЧЕЕ'],
              '049': ['ПРОЧЕЕ'], '050': ['ПРОЧЕЕ'], '051': ['ПРОЧЕЕ'], '052': ['ПРОЧЕЕ'], '053': ['ПРОЧЕЕ'],
              '054': ['ПРОЧЕЕ'], '055': ['ПРОЧЕЕ'], '056': ['ПРОЧЕЕ'], '057': ['ПРОЧЕЕ'], '058': ['ПРОЧЕЕ'],
              '059': ['ПРОЧЕЕ'], '060': ['ПРОЧЕЕ'], '061': ['ОДЕЖДА'], '062': ['ОДЕЖДА'], '063': ['ПРОЧЕЕ'],
              '064': ['ОБУВЬ'], '065': ['ПРОЧЕЕ'], '066': ['ПРОЧЕЕ'], '067': ['ПРОЧЕЕ'], '068': ['ПРОЧЕЕ'],
              '069': ['ПРОЧЕЕ'], '070': ['ПРОЧЕЕ'], '071': ['ЮВЕЛИРНЫЕ УКРАШЕНИЯ'], '072': ['ПРОЧЕЕ'],
              '073': ['ПРОЧЕЕ'], '074': ['ПРОЧЕЕ'], '075': ['ПРОЧЕЕ'], '076': ['ПРОЧЕЕ'], '078': ['ПРОЧЕЕ'],
              '079': ['ПРОЧЕЕ'], '080': ['ПРОЧЕЕ'], '081': ['ПРОЧЕЕ'], '082': ['ПРОЧЕЕ'], '083': ['ПРОЧЕЕ'],
              '084': ['ПРОЧЕЕ'], '085': ['ПРОЧЕЕ'], '086': ['ПРОЧЕЕ'], '087': ['ПРОЧЕЕ'], '088': ['ПРОЧЕЕ'],
              '089': ['ПРОЧЕЕ'], '090': ['ПРОЧЕЕ'], '091': ['ПРОЧЕЕ'], '092': ['ПРОЧЕЕ'], '093': ['ПРОЧЕЕ'],
              '094': ['ПРОЧЕЕ'], '095': ['ИГРУШКИ И СПОРТИВНЫЙ ИНВЕНТАРЬ'], '096': ['ПРОЧЕЕ'], '097': ['ПРОЧЕЕ'],
              '098': ['ПРОЧЕЕ'], '099': ['КОММУНАЛЬНЫЕ УСЛУГИ'], '100': ['ПРОЧЕЕ'], '101': ['ПРОЧЕЕ'],
              '102': ['ПРОЧЕЕ'], '103': ['ПРОЧЕЕ'], '104': ['ПРОЧЕЕ'], '105': ['ПРОЧЕЕ'], '106': ['ПРОЧЕЕ'],
              '107': ['ПРОЧЕЕ'], '108': ['ОБРАЗОВАТЕЛЬНЫЕ УСЛУГИ'], '109': ['МЕДИЦИНСКИЕ УСЛУГИ'], '110': ['ПРОЧЕЕ'],
              '111': ['ПРОЧЕЕ'], '112': ['ПРОЧЕЕ'], '113': ['ПРОЧЕЕ'], '114': ['ПРОЧЕЕ'], '115': ['ПРОЧЕЕ'],
              '116': ['ПРОЧЕЕ'], '117': ['БЫТОВЫЕ УСЛУГИ'], '118': ['ПРОЧЕЕ']}

# Получение ссылки к чеку
def decode(src):
    image = cv2.imread(src)
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        response = requests.get(obj.data)
        page = BS(response.content,'html.parser')
        return page

# Получение списка с названиями покупки
def pr_name(page):
    product_info = [el.select('.products-row') for el in page.select('.products-tables')]
    list_name = [pr_name.find('td').get_text().strip() for pr_name in product_info[0]]
    return list_name

# Получение списка с количеством покупки
def pr_number(page):
    product_info = [el.select('.products-row') for el in page.select('.products-tables')]
    list_number = [float(pr_number.find('td', {'align': 'right'}).get_text().strip()) for pr_number in product_info[0]]
    return list_number

# Получение списка с суммой покупки
def pr_sum(page):
    product_info = [el.select('.products-row') for el in page.select('.products-tables')]
    list_sum = [float(pr_sum.find('td', {'class': 'price-sum'}).get_text().strip().replace(',','')) for pr_sum in product_info[0]]
    return list_sum

# Получение списка с категориями покупки
def category(page):
    global categories
    product_code = [i.select('.code-row') for i in page.select('.products-tables')]
    list_cat_code = [category.find('td', {'align': 'right', 'colspan': '2'}).get_text().strip() for category in product_code[0]]
    product_info = [el.select('.products-row') for el in page.select('.products-tables')]

    def func_chunks_generators(lst, n):
        for i in range(0, len(lst), int(len(lst) / n)):
            yield list_cat_code[i: i + int(len(lst) / n)]

    kodi = list(func_chunks_generators(list_cat_code, len(product_info[0])))
    list_cat = [i[2][:3] for i in kodi]
    cat_list = [categories[i][0] for i in list_cat]
    return cat_list

# Получение даты покупки
def get_date(page):
    d = page.select('i')
    data = d[1].text
    date = int(data[:2])
    return date

# Получение месяца покупки
def get_month(page):
    d = page.select('i')
    data = d[1].text
    month = int(data[3:5])
    return month

# Получение года покупки
def get_year(page):
    d = page.select('i')
    data = d[1].text
    year = int(data[6:10])
    return year




