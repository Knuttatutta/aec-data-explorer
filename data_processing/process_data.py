from copy import copy
from warnings import warn

SPECKLE_ATTRIBUTES_TO_PURGE = ['applicationId', 'totalChildrenCount', 'collectionType']

def process_speckle_data(data):

    def purge_speckle_data(data):
        def process_dict(d):
            keys_to_delete = []
            items_to_add = {}
            
            for key, value in d.items():
                if key == 'speckle_type':
                    d[key] = value.split('.')[-1]
                elif key in ['elements', 'demands', 'parameters'] and isinstance(value, list):
                    d[key] = process_elements(value)
                elif '@' in key:
                    new_key = key.replace('@', '')
                    items_to_add[new_key] = process_value(value)
                    keys_to_delete.append(key)
                elif key in SPECKLE_ATTRIBUTES_TO_PURGE:
                    keys_to_delete.append(key)
                else:
                    d[key] = process_value(value)
            
            for key in keys_to_delete:
                del d[key]
            d.update(items_to_add)
            
            return d
        
        def process_list(lst):
            return [process_value(item) for item in lst]
        
        def process_value(val):
            if isinstance(val, dict):
                return process_dict(val)
            elif isinstance(val, list):
                return process_list(val)
            else:
                return val
        
        def process_elements(elements):
            processed_elements = {}
            for i, item in enumerate(elements):
                if isinstance(item, dict):
                    processed_item = process_value(item)
                    if 'speckle_type' in processed_item:
                        key = processed_item['name']
                        # Ensure unique keys by appending a number if necessary
                        while key in processed_elements:
                            key = f"{key}_{i}"
                        processed_elements[key] = processed_item
                    else:
                        # If no speckle_type, use a default key
                        key = f"unknown_type_{i}"
                        processed_elements[key] = processed_item
                else:
                    # Handle case where item is not a dictionary
                    key = f"invalid_element_{i}"
                    processed_elements[key] = process_value(item)
            return processed_elements
        
        return process_value(data)

    data_to_process = copy(data)
    processed_data = purge_speckle_data(data_to_process)

    return processed_data