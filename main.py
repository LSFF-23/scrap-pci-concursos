from FetchPCI import FetchPCI

import logging
import os
import sqlite3
import time

DB_FILE = "news.db"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s [%(levelname)s] %(message)s] ",
    encoding="utf-8",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)

if not os.path.isfile(DB_FILE):
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

fp = FetchPCI("https://www.pciconcursos.com.br/concursos/nordeste/", {"id": "MA"}, {"id": "PB"}, DB_FILE)
while True:
    try:
        logging.info(fp.fetch_data())
    except Exception as e:
        logging.info(repr(e))
    time.sleep(60)