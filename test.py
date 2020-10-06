import crawl_module.goo as goo_test
import random
import time
from tqdm import tqdm

url_00 = 'https://dictionary.goo.ne.jp/jn'
url_01 = 'https://dictionary.goo.ne.jp/jn/index/%E3%81%82/'
url_02 = 'https://dictionary.goo.ne.jp/jn/index/%E3%81%82/248'
# goo_test.get_content_box_word(url)
# goo_test.get_word(url=url_02)
goo_test.crawl_start(url_00)
#print(goo_test.get_word_pages(url_01))
