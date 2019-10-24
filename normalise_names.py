#Used to Normalise variations in Names

#Just run the function two_word_name(input_list)

#Input: 
#input_list = ['matin a', 'mat amit', 'ma a', 'matin r', 'matin amit', 'amit matin',  'amit matin', 'a matin'] 

#Output: 
#{'a ma': [2], 'amit matin': [0, 4, 5, 6, 7], 'mat amit': [1], 'r matin': [3]}
#(Key - Normalised Name, Value - List of Indices to be normalised)

#The code currently handles two-word names. 

def exactsame(input_list):
    same = dict()
    for i,name in enumerate(input_list):
        try:
            same[name].append(i) 
        except:
            same[name] = [i]
    return same

def getformat(dict_type, dict_index):
    for name in dict_type:
        if (len(dict_type[name]) > 1) and (len(name.split()[0]) == 1):
            
            for name_ in dict_type[name]:
                a = set(name_.split())
                b = set(name.split())
                
                if (len(a - b) == 1):
                    final_name = list(a-b)[0] +' '+ name.split()[1] 
                    dict_type[final_name] = dict_type.pop(name)
                    dict_index[final_name] = dict_index.pop(name)
    
    return dict_type, dict_index


def two_word_name(input_list):
    uniq_dict = exactsame(input_list)
    uniq_list = uniq_dict.keys()

    word_switch_type_track = {}
    word_switch_index_track = {}

    for name in uniq_list:        
        list_keys = word_switch_type_track.keys()
        keys_set_list = [set(i.split()) for i in list_keys]
        
        if set(name.split()) in keys_set_list:
            idx = keys_set_list.index(set(name.split()))
            element_name = list_keys[idx]

            word_switch_index_track[element_name] += uniq_dict[name]
            word_switch_type_track[element_name].append(name)

        else:
            word_switch_type_track[name] = [name]
            word_switch_index_track[name] = uniq_dict[name]
    
    update_type = {}
    update_index = {}
    
    for name in word_switch_type_track:
        if len(name.split()[1]) == 1:
            update_type['%s %s'%(name.split()[1], name.split()[0])] = word_switch_type_track[name]
            update_index['%s %s'%(name.split()[1], name.split()[0])] = word_switch_index_track[name]
        else:
            update_type[name] = word_switch_type_track[name]
            update_index[name] = word_switch_index_track[name]
    
    
    new_update_type = {}
    new_update_index = {}
    
    for name in update_index:        
        list_keys = new_update_type.keys()
        keys_set_list = [set(i.split()) for i in list_keys]
        name_set = set(name.split())
        
        flg = 0
        for key in keys_set_list:
            if flg == 1:
                break
                
            result = key.intersection(name_set)
            
            if len(result) == 1:
                a = list(name_set - result)[0]
                b = list(key - result)[0]
                
                if len(a) == 1 or len(b) == 1:
                    a = a[0]
                    b = b[0]

                    if a == b:
                        idx = keys_set_list.index(key)
                        element_name = list_keys[idx]

                        new_update_index[element_name] += update_index[name]
                        new_update_type[element_name].append(name)
                        
                    else:
                        new_update_index[name] = update_index[name]
                        new_update_type[name] = [name]
                else:
                    new_update_index[name] = update_index[name]
                    new_update_type[name] = [name]
                
                flg = 1

        if flg == 0:
            new_update_index[name] = update_index[name]
            new_update_type[name] = [name]
    
    new_update_type, new_update_index = getformat(new_update_type, new_update_index)
    
    return new_update_index