import crawl_module.goo as goo_test
import database_service.goo_init_database as gid

base_url = 'https://dictionary.goo.ne.jp/jn'

if __name__ == '__main__':

    #crawl start
    goo_test.crawl_start(base_url)
