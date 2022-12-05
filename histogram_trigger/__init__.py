import  logging
import azure.functions as  func
import numpy as np
import math

def  main(event: func.EventHubEvent, outputBlob: func.Out[str]):

    def merge(bucket_list, maxSize):
        # find the 2 bars with the least amount of elements -> blocked
        # check if you can merge them with satisfying the criteria of maxSize

        bucket_sizes = []
        
        for bucket in bucket_list:
            bucket_sizes.append(len(bucket[0]))
            
        min_index = -1
        min_value = float('inf')
        
        j = 0
        while j < len(bucket_sizes) - 1:
            combined_size = bucket_sizes[j] + bucket_sizes[j+1]
            if combined_size <= maxSize:
                if combined_size < min_value:
                    min_index = j
        
        if min_index != -1:
            left_bucket = bucket_list.pop[min_index]
            right_bucket = bucket_list.pop[min_index + 1]
            list_of_elements = left_bucket[0] + right_bucket[0]
            min_bound = left_bucket[1][0]
            max_bound = right_bucket[1][1]
            merged_bucket = [list_of_elements, [min_bound, max_bound]]
            bucket_list.insert(min_index, merged_bucket)
        
        return bucket_list

    def split(bucket_list, index_bucket_to_split):
    
        bucket_to_split = bucket_list[index_bucket_to_split]
        elements_of_bucket = bucket_to_split[0]
        bucket_bounds = bucket_to_split[1]
        bucket_size = len(elements_of_bucket)
        
        # before split check that number of bars < Sm
        if len(bucket_list) + 1 > Sm:
            # we need to merge first
            bucket_list = merge(bucket_list)
        else:
            # sort elements:
            sorted_elements = sorted(elements_of_bucket, key = lambda x: x[1])
            
            # create 2 buckets
            left_bucket = [[],[bucket_bounds[0],sorted_elements[int(bucket_size / 2)][1]]]
            right_bucket = [[],[sorted_elements[int(bucket_size / 2)][1],bucket_bounds[1]]]
            
            # add elements in the buckets
            k = 0
            for k in range(len(sorted_elements)):
                if k < bucket_size / 2:
                    left_bucket[0].append(sorted_elements[k])
                else:
                    right_bucket[0].append(sorted_elements[k])
            
            # remove the initial bucket
            bucket_list.pop(index_bucket_to_split)
            
            # return the updated bucket_list
            bucket_list.insert(index_bucket_to_split, left_bucket)
            bucket_list.insert(index_bucket_to_split + 1, right_bucket)
        
        return bucket_list

    # number of items in the current window
    W = len(event)

    # B is the number of buckets in the histogram under construction
    B = 5

    # p < 10
    p = 2

    maxCoef = 1.7

    # Sm = B × p partitions (Bars)
    # the number of bars should not exceed Sm
    Sm = B * p

    # bucket_list:
    # [[[el1, el2, ...], [min, max)], [bucket1], [bucket2], ...]

    first_iter = True
    bucket_list = []
    elements_in_all_buckets = 0

    for ev in event:
        ev_str = ev.get_body().decode()

        idx, el = ev_str.split(",")

        idx = float(idx)
        el = float(el)
        
        temp_tuple = (idx, el)
        added_element = False
        
        if first_iter:
            first_iter = False
            temp_bucket = [[temp_tuple], [el, el]]
            bucket_list.append(temp_bucket)
            elements_in_all_buckets += 1        
        else:
            for bucket in bucket_list:
                bounds = bucket[1]
                min_bound = bounds[0]
                max_bound = bounds[1]
                if el < min_bound or el > max_bound:
                    continue
                else:
                    bucket[0].append(temp_tuple)
                    added_element = True
                    elements_in_all_buckets += 1
                    
            if added_element:
                #check if maxSize is violated
                # maxSize: max number of elements in a bar
                maxSize = math.ceil(maxCoef * W / Sm)
                i = 0
                while i < len(bucket_list):
                    current_bucket = bucket_list[i]
                    elements_in_bucket = current_bucket[0]
                    if len(elements_in_bucket) > maxSize:
                        bucket_list = split(bucket_list, i)
                    i += 1
            
            if not(added_element):
                # check whether the element must go in front or at the end of the buckets
                first_bucket = bucket_list[0] 
                last_bucket = bucket_list[-1]
                min_bound_first_bucket = first_bucket[1][0]
                max_bound_last_bucket = last_bucket[1][1]

                if el < min_bound_first_bucket:
                    # extend the first bucket             
                    bucket_list[0][1][0] = el
                    bucket_list[0][0].append(temp_tuple)
                    elements_in_all_buckets += 1
                elif el > max_bound_last_bucket:
                    # extend the last bucket
                    bucket_list[0][1][1] = el
                    bucket_list[0][0].append(temp_tuple)
                    elements_in_all_buckets += 1

    for bucket in bucket_list:
        logging.info(f'Bounds: {bucket[1]} Len: {len(bucket[0])}')
        outputBlob.set(f'Bounds: {bucket[1]} Len: {len(bucket[0])}')