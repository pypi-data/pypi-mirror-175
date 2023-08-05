from dataclasses import dataclass
from Stilix import STILIX_LIST , STILIX_LIST_COUNT
@dataclass
class empty_space:
          list_: list
          def check_reset(self,list_to_check_reset: list):
                    dict_check = {
                              0:True
                    }
                    print(dict_check.get(STILIX_LIST_COUNT.list_length(list_to_check_reset)))
                    
empty_list=empty_space([])

'''
The empty_list object contains an empty list which can be used on anything.
The check_reset mehod of the empty list object checks if the desired list is empty.

empty_list.list_ = ["a"]

empty_list.check_reset(empty_list.list_)

False

w = []

empty_list.check_reset(w)

True
'''

class change_data:
          def normal_save(self,thing_to_save: list,save_on: list):
                    save_on.append(thing_to_save)
                    
          def tuple_save(self,thing_too_tup: list,save_tup_on_thing: list):
                    thing_too_tup=tuple(thing_too_tup)
                    save_tup_on_thing.append(thing_too_tup)
                    thing_too_tup=list(thing_too_tup)
                    
          def set_save(self,thing_to_list: list,save_list_on: list):
                    thing_to_list=set(thing_to_list)
                    save_list_on.append(thing_to_list)
                    thing_to_list=list(thing_to_list)

data_change=change_data()

'''
The data_change object saves a list as a different data structure like tuples or sets in a list.
The data_change.normal_save method can be used to just save a list in another list without changing it.
The data_change.tuple_save method can be used to save a list as a tuple in another list.
The data_change.set_save method can be used to save a list as a set in another list.

b = []
a = []
data_change.normal_save(a,b)
print(b)

[[]]

data_change.tuple_save(a,b)
print(b)

[()]

data_change.set_save(a,b)
print(b)

[{}]

'''