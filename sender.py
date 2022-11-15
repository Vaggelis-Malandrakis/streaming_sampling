import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from math import cos

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str="Endpoint=sb://eventhubns2.servicebus.windows.net/;SharedAccessKeyName=mypolicy;SharedAccessKey=glXJLCzo0cbqDhxkJKBPh8JPvZi3qaTI5Vtj+iyeqc4=",
        eventhub_name="eh2")
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        x = 0
        for _ in range(1):
            for _ in range(100):
                y = cos(x)
                tuple_str = str(x) + ", " + str(y)
                event_data_batch.add(EventData(tuple_str))
                x += 0.1
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
