import logging
from flask import Flask

logger = logging.getLogger("provda.server")


app = Flask(__name__)
@app.route("/")
def object():
    logger.debug("object enter")
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run()
