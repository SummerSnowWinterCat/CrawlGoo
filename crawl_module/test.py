import crawl_module.goo as goo
import database_service.goo_init_database as g_i_d
import pymysql
from tqdm import tqdm

if __name__ == '__main__':
    print(goo.get_word_pages('https://dictionary.goo.ne.jp/jn/index/%E3%82%92/'))
