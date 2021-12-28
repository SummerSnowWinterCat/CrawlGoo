from database_service.database_pool import search_data, add_data

if __name__ == '__main__':
    _CREATE_IT = '''
          CREATE TABLE IF NOT EXISTS {}(
            ID INT PRIMARY KEY AUTO_INCREMENT,
            INITIALS VARCHAR(25) NOT NULL,
            WORD VARCHAR(200) NOT NULL,
            MORPHEME VARCHAR (200),
            URL VARCHAR (800),
            MEANING VARCHAR (5000) NOT NULL,
            UPDATETIME DATETIME NOT NULL,
            EXTEND VARCHAR(5000)
            )CHARSET utf8mb4;
          '''.format('DICTIONARY_IT')
    add_data(_CREATE_IT)
