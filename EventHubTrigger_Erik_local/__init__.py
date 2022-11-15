import  logging
import azure.functions as  func
import numpy as np

def  main(event: func.EventHubEvent):

    res = []
    res_size = 25

    stream_weight = 1
    i = 0

    for  ev  in  event:
        logging.info(f'Function triggered to process a message: {ev.get_body().decode()}')
        ev_str = ev.get_body().decode()
        stream_val = tuple(map(float, ev_str.split(', ')))
        if i < res_size:
            key = np.random.rand()**(1/stream_weight)
            res += [(key,stream_val)]
        else:
            res_keys = [k for k,v in res]
            thresh = min(res_keys)
            min_ind = res_keys.index(thresh)
            key = np.random.rand()**(1/stream_weight)
            if key > thresh:
                res[min_ind] = (key,stream_val)
        i += 1

    res_val = ["(" + str(v1) + ", " + str(v2) + ")" for k,(v1,v2) in res]
    samp_str =  ' '.join(res_val)
    logging.info(f'Final sampled values: {samp_str}')
    
    # logging.info(f' SequenceNumber = {ev.sequence_number}')
    # logging.info(f' Offset = {ev.offset}')