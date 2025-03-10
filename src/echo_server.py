import sys
import signal
import threading
from werkzeug.serving import make_server

# Initialize Singletons
from config.config import Config
from mongo_utils.mongo_io import MongoIO
config = Config.get_instance()
mongo = MongoIO.get_instance()

# Initialize Logging
import logging
logging.basicConfig(level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)
logger.info(f"============= Starting Server Initialization, Logging at {config.LOGGING_LEVEL}===============")

# Initialize Echo Discord Bot
from echo.echo import Echo
from echo.ollama_llm_client import OllamaLLMClient
echo = Echo("Echo", bot_id=config.FRAN_BOT_ID, model=config.FRAN_MODEL_NAME, client=OllamaLLMClient())
# from echo.mock_llm_client import MockLLMClient
# echo = Echo("Fran", bot_id=config.FRAN_BOT_ID, model=config.FRAN_MODEL_NAME, client=MockLLMClient())

# Register Agents
from agents.config_agent import create_config_agent

echo.register_agent(create_config_agent(agent_name="config"))

# Initialize Flask App
from flask import Flask
from flask_utils.ejson_encoder import MongoJSONEncoder
from prometheus_flask_exporter import PrometheusMetrics
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.BUILT_AT)

# Register flask routes
from routes.bot_routes import create_bot_routes
from routes.conversation_routes import create_conversation_routes
from routes.echo_routes import create_echo_routes
from routes.config_routes import create_config_routes

app.register_blueprint(create_bot_routes(), url_prefix='/api/bot')
app.register_blueprint(create_conversation_routes(), url_prefix='/api/conversation')
app.register_blueprint(create_echo_routes(echo=echo), url_prefix='/api/echo')
app.register_blueprint(create_config_routes(), url_prefix='/api/config')

# Flask server management
server = make_server("0.0.0.0", config.FRAN_API_PORT, app)
flask_thread = threading.Thread(target=server.serve_forever)

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")

    # Shutdown Flask gracefully
    if flask_thread.is_alive():
        logger.info("Stopping Flask server...")
        server.shutdown()
        flask_thread.join()

    # Disconnect from MongoDB
    logger.info("Closing MongoDB connection.")
    mongo.disconnect()

    # Close the Discord bot
    logger.info("Closing Discord connection.")
    echo.close(timeout=0.1) # TODO Add DISCORD_TIMEOUT config value with this default value

    logger.info("Shutdown complete.")
    sys.exit(0)  

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Start the bot and expose the app object for Gunicorn
if __name__ == "__main__":
    flask_thread.start()
    logger.info("Flask server started.")

    # Run Discord bot in the main thread
    echo.run(token=config.DISCORD_FRAN_TOKEN)
    