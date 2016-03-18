def checker(dict_element, dict_filter):
    global counter
    counter = 0

    def fullfill_filter(key, value):
        if key in dict_filter:
            if value in dict_filter[key]:
                return True

    def extract_dict(dict_element):
        global counter

        for key, value in dict_element.items():
            if isinstance(value, str):
                if fullfill_filter(key, value):
                    counter += 1
            elif isinstance(value, dict): 
                extract_dict(value)
            elif isinstance(value, list):
                extract_list(key, value)

    def extract_list(key, list_element):
        global counter

        for el in list_element:
            if isinstance(el, dict):
                extract_dict(el)
            if isinstance(el, list):
                extract_list(el)
            if isinstance(el, str):
                if fullfill_filter(key, el):
                    counter += 1

    extract_dict(dict_element)
    
    if counter == len(dict_filter.keys()):
        return True
    return False
