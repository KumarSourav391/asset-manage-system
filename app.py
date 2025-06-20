
from entrypoint import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_flask():
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run_flask()
