from FetchPCI import FetchPCI

import logging
import os
import sqlite3

db_file = "news.db"

if not os.path.isfile(db_file):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            news_id INTEGER PRIMARY KEY AUTOINCREMENT,
            public_body TEXT,
            pci_link TEXT,
            pb_icon TEXT,
            location TEXT,
            additional_info TEXT,
            enrolment_upto TEXT
        )
    """)
    conn.commit()
    conn.close()

fp = FetchPCI("https://www.pciconcursos.com.br/concursos/nordeste/", {"id": "MA"}, {"id": "PB"}, db_file)
try:
    logging.info(fp.fetch_data())
except Exception as e:
    logging.info(repr(e))