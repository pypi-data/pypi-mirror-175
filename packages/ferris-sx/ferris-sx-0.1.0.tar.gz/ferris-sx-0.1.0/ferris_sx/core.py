import logging

import faust
# from ferris_cli.ferris_cli import FerrisKafkaLoggingHandler
# from logstash_formatter import LogstashFormatterV1
from ferris_sx import settings as s

app = faust.App(s.APP_NAME,
                broker=[f'kafka://{url}' for url in s.KAFKA_NODES],
                topic_disable_leader=True,
                autodiscover=True,
                origin='ferris_sx')

app.logger = logging.getLogger(s.APP_NAME)
logger = logging.getLogger(s.APP_NAME)
# kh = FerrisKafkaLoggingHandler()
# kh.setLevel(s.LOG_TO_KAFKA_LEVEL)
# formatter = LogstashFormatterV1()
# kh.setFormatter(formatter)
# logger.addHandler(kh)
