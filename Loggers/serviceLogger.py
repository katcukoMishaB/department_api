import logging
serviceLogger = logging.getLogger("ServiceLogger")
serviceLogger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s — %(funcName)s:%(lineno)d — %(message)s")
handler = logging.FileHandler(f"ServiceLogger.log", mode='a', encoding='utf-8')
handler.setFormatter(formatter)
serviceLogger.addHandler(handler)