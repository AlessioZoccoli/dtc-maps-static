from common.persistence.db import Database
from pprint import pprint

if __name__ == '__main__':
    my_db = Database()
    ten_docs = my_db.get_n_documents(10)

    for post in ten_docs:
        pprint(post)
    # pprint(my_db.get_n_documents(4))
