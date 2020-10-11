import crawl_module.goo as goo
import database_service.goo_init_database as gid
import pymysql

base_url = 'https://dictionary.goo.ne.jp/jn'

if __name__ == '__main__':
    print('DOWNLOAD MODE 1:Create and Download')
    print('DOWNLOAD MODE 2:Download Only')
    if int(input("DOWNLOAD MODE (1 or 2):")) == 1:
        goo.crawl_start(base_url)
    else:
        goo.download_continue()
