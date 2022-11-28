import  logging
import azure.functions as  func
import numpy as np

def  main(event: func.EventHubEvent, outputBlob: func.Out[str]):
    N = len(event)
    a = 1.1 # We increase T by 10%
    max_size = N / 10

    # 1/T = selection probability
    T = 1

    #// S = Concise Sample
    S = {}
    S_help = {}
    len_S = 0

    for ev in event:
        ev_str = ev.get_body().decode()

        idx, val = ev_str.split(",")

        t_idx = float(idx)
        t_val = float(val)

        if np.random.random() < 1/T:
            if t_val in S:
                S[t_val] += 1
                S_help[t_val].append(t_idx)
            else:
                S_help[t_val] = [t_idx]
                S[t_val] = 1
            len_S += 1

    
        # Deletion step, Adjust sample when it gets too large
        
        if len_S> max_size:
            T_prime = a * T
            
            for s in S:
                for _ in range(S[s]):
                    if np.random.random() < 1 - T/T_prime:
                        S[s] -= 1
                        len_S -=1
                        if len(S_help[s]) == 1:
                            S_help[s].pop(0)
                        else:
                            S_help[s].pop(np.random.randint(0,len(S_help[s])-1))
            
            T = T_prime

    idx_list = []
    res_list = []

    for s in S:
        if S[s] > 0:
            for i in range(S[s]):
                idx_list.append(S_help[s][i])
                res_list.append(s)

    rep_avg = np.average(res_list)
    rep_min = min(res_list)
    rep_max = max(res_list)

    logging.info(f'N: {N}, Average: {rep_avg}, Minimum: {rep_min}, Maximum: {rep_max}')
    outputBlob.set(f'N: {N}, Average: {rep_avg}, Minimum: {rep_min}, Maximum: {rep_max}')