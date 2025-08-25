from FetchPCI import FetchPCI

import time
import logging

sb = FetchPCI("https://www.pciconcursos.com.br/concursos/nordeste/", {"id": "MA"}, {"id": "PB"})
while True:
    try:
        sb.fetch_data()
    except Exception as e:
        logging.info(repr(e))
    time.sleep(60)