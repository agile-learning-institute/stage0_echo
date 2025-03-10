import logging
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from echo.agent import Agent
from services.bot_services import BotServices

logger = logging.getLogger(__name__)

def create_bot_agent(agent_name):
    """ Registers event handlers and commands for the Fran home channel. """
    agent = Agent(agent_name, description="The bot agent provides information about a specific Echo Bot, including the set of active channels")
    
    def get_bot(arguments):
        """Get the bot record based on the bot_id passed as arguments"""
        try:
            token = create_token()
            bot = BotServices.get_bot(bot_id=arguments, token=token)
            return bot
        except Exception as e:
            logger.warning(f"A get_bot Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_bot", 
        function=get_bot,
        description="Get all bot information for the specified bot", 
        arguments_schema={
            "description": "Bot Unique Identifier",
            "type": "identifier"
        },
        output_schema={
            "title": "Bots",
            "description": "Stage0 Bots",
            "type": "object",
            "properties": {
                "_id": {
                    "description": "The unique identifier for a Bot Description",
                    "type": "identifier"
                },
                "status": {
                    "description": "The status of the Bot",
                    "type": "enum",
                    "enums": "default_status"
                },
                "name": {
                    "description": "Bot Short Name",
                    "type": "word"
                },
                "description": {
                    "description": "Short description of bot",
                    "type": "sentence"
                },
                "channels": {
                    "description": "List of Discord Channel ID values",
                    "type": "array",
                    "items": {
                        "type": "word"
                    }
                },
                "last_saved": {
                    "description": "Last Saved breadcrumb",
                    "type": "breadcrumb"
                }
            }
        })

    def get_channels(arguments):
        """Get a list of active channels for the specified bot"""
        try:
            token = create_token()
            channels = BotServices.get_channels(bot_id=arguments, token=token)
            return channels
        except Exception as e:
            logger.warning(f"A get_channels Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name= "get_channels", 
        function = get_channels,
        description = "Get a list of active channels", 
        arguments_schema = {
            "description": "Bot Unique Identifier",
            "type": "identifier"
        },
        output_schema = {
            "description": "Array (set) of channel ID's",
            "type": "array",
            "items": {
                "type": "identifier"
            }
        })
    
    def add_channel(arguments):
        """Add the specified channel_id 
        to the set of active channels for bot_id"""
        try:
            logger.debug(f"Agent Add Channel({arguments})")
            token = create_token()
            logger.debug(f"Token: {token}")
            breadcrumb = create_breadcrumb(token)
            logger.debug(f"Breadcrumb: {breadcrumb}")
            channels = BotServices.add_channel(
                channel_id=arguments["channel_id"], 
                bot_id=arguments["bot_id"], 
                token=token, breadcrumb=breadcrumb)
            logger.info(f"Channels: {channels}")
            return channels
        except Exception as e:
            logger.warning(f"A add_channel Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name= "add_channel", 
        function = add_channel,
        description = "Add a channel to the set of active channels", 
        arguments_schema = {
            "description": "Bot and Channel identifier",
            "type": "object",
            "properties": {
                "bot_id": {
                    "description": "The bot unique identifier",
                    "type": "identifier"
                },
                "channel_id": {
                    "description": "The channel identifier",
                    "type": "identifier"
                }
            }
        },
        output_schema = {
            "description": "Array (set) of channel ID's",
            "type": "array",
            "items": {
                "type": "identifier"
            }
        })
    
    def remove_channel(arguments):
        """Remove the specified channel_id 
        from the set of active channels for bot_id"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            channels = BotServices.remove_channel(
                bot_id=arguments["bot_id"], 
                channel_id=arguments["channel_id"], 
                token=token, breadcrumb=breadcrumb)
            return channels
        except Exception as e:
            logger.warning(f"A remove_channel Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name= "remove_channel", 
        function = remove_channel,
        description = "Remove a channel from the active channels list", 
        arguments_schema = {
            "description": "Bot and Channel identifier",
            "type": "object",
            "properties": {
                "bot_id": {
                    "description": "The bot unique identifier",
                    "type": "identifier"
                },
                "channel_id": {
                    "description": "The channel identifier",
                    "type": "identifier"
                }
            }
        },
        output_schema = {
            "description": "Array (set) of channel ID's",
            "type": "array",
            "items": {
                "type": "identifier"
            }
        })

    logger.info("Registered bot agent action handlers.")
    return agent