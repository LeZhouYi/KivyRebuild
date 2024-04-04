from core.logging import logger
from core.app.main import MainApp

if __name__ == "__main__":
    logger.debug("app start")
    MainApp().run()
