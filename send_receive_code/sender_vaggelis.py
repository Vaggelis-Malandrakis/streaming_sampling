import time
from azure.eventhub import EventHubProducerClient, EventData
import numpy as np

CONNECTION_STR = "Endpoint=sb://eventhubns2.servicebus.windows.net/;SharedAccessKeyName=mypolicy;SharedAccessKey=glXJLCzo0cbqDhxkJKBPh8JPvZi3qaTI5Vtj+iyeqc4="
EVENTHUB_NAME = "working_eventhub"

def send_event_data_batch(producer):
    idx = 0
    idx_list = []
    res_list = []
    # copy_res_list = []

    for _ in range(5*1000):
        res_list.append(np.sin(idx))
        # rdm = np.random.randint(1, 100)
        # res_list.append(rdm)
        # copy_res_list.append(rdm)
        idx_list.append(round(idx, 1))
        idx += 0.1

    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    for k in range(1):
        event_data_batch = producer.create_batch()
        for i in range(1000):
            info = str(idx_list.pop(0)) + "," + str(res_list.pop(0))
            print('Sending: ' + info)
            event_data_batch.add(EventData(info))
        producer.send_batch(event_data_batch)


def send_event_data_batch_with_properties(producer):
    event_data_batch = producer.create_batch()
    event_data = EventData('Message with properties')
    event_data.properties = {'prop_key': 'prop_value'}
    event_data_batch.add(event_data)
    producer.send_batch(event_data_batch)


producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

start_time = time.time()
with producer:
    send_event_data_batch(producer)
    # send_event_data_batch_with_properties(producer)

print("Send messages in {} seconds.".format(time.time() - start_time))
