from .core import app
from . import settings as s

topic = app.topic(s.TOPIC_NAME)


@app.agent(topic)
async def listener(messages):
    if s.BATCH_NUMBER > 1:
        print("batch")
        async for list_msg in messages.take(s.BATCH_NUMBER, within=s.BATCH_FRAME):
            app.process(list_msg)
    else:
        print("single")
        async for m in messages:
            app.process(m)
