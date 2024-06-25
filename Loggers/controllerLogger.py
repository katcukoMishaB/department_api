import logging
controllerLogger = logging.getLogger("ControllerLogger")
controllerLogger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s — %(funcName)s:%(lineno)d — %(message)s")
handler = logging.FileHandler(f"ControllerLogger.log", mode='a', encoding='utf-8')
handler.setFormatter(formatter)
controllerLogger.addHandler(handler)