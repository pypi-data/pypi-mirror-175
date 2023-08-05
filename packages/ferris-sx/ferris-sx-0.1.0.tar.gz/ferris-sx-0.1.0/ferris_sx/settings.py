import os
import json

# from ferris_cli.ferris_cli import ApplicationConfigurator

APP_NAME = os.environ['APP_NAME']

# app_config = ApplicationConfigurator().get(APP_NAME)
# env = ApplicationConfigurator().get("ferris.env")

TOPIC_NAME = os.environ['TOPIC_NAME']

MODULE_NAME = os.environ['MODULE_NAME']
CLASS_NAME = os.environ['CLASS_NAME']

BATCH_NUMBER = int(os.environ['BATCH_NUMBER'])
BATCH_FRAME = int(os.environ['BATCH_FRAME'])

KAFKA_NODES = json.loads(os.environ['KAFKA_NODES'])
LOG_TO_KAFKA_LEVEL = os.environ['LOG_TO_KAFKA_LEVEL']

