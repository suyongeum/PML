# All tables are created by eumdict_content_seed
# difficulty level is stored in core_word
# table: core_word
import os
import pymysql.cursors
from os import listdir
from os.path import isfile, join
import re
import settings

# windows
word_files_path = os.path.join(os.path.dirname(os.getcwd()), 'utils\\word_data')

def empty_table(con):
    with con.cursor() as cursor:
        # Create a new record
        sql = 'TRUNCATE TABLE `pml_word`'
        cursor.execute(sql)


def add_word(con, word, difficulty):
    with con.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `pml_word` (`word`, `difficulty`) VALUES (%s, %s)"
        cursor.execute(sql, (word, difficulty))


def read_word_file(path):
    words = []
    encodings = ['utf-16', 'utf-8', 'ascii']
    for e in encodings:
        try:
            with open(path) as f:
                lines = f.readlines()
            for line in lines:
                line_words = line.split()
                words.extend(line_words)
        except UnicodeError:
            print('Error in reading ' + path)
            print('got unicode error with %s , trying different encoding' % e)
        else:
            print('opening the file with encoding:  %s ' % e)
            break
    return words

# Connect to the database
connection = pymysql.connect(host           =   settings.DB_HOST,
                             user           =   settings.DB_USER,
                             password       =   settings.DB_PASS,
                             db             =   settings.DB_NAME,
                             charset        =   settings.DB_CHAR,
                             cursorclass    =   pymysql.cursors.DictCursor)

try:
    empty_table(connection)

    dir_list = listdir(word_files_path)
    #print (dir_list)
    for name in dir_list:
        path = join(word_files_path, name)
        if not isfile(path):
            continue
        match = re.match(r'^mod_done_lv(\d{2})\.txt$', name, re.M | re.I)
        if not match:
            continue
        difficulty_str = match.group(1)
        difficulty = int(difficulty_str)

        print(name)
        words = read_word_file(path)
        for word in words:
            #print(connection, word, difficulty)
            add_word(connection, word, difficulty)

    connection.commit()
    print('finished!')

except:
    raise

finally:
    connection.close()



