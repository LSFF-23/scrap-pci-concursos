import sqlite3

# create/connect database
conn = sqlite3.connect("news.db")
cursor = conn.cursor()

# create table
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