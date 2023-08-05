from dataclasses import dataclass


          
class stilix_list:
          def add_styles(self,reciever_list: list,sender_list: list):
                    for item in sender_list:
                              reciever_list.append(item)
                              
          def remove_styles(self,remove_list: list,items_to_remove: list):
                    for item in items_to_remove:
                              if item in remove_list:
                                        remove_list.remove(item) 
                                        
          def display_all(self,list_to_display_all: list):
                    for item in list_to_display_all:
                              print(item)
          
          def display_all_horizontal(self,list_to_display_all: list):
                    for item in list_to_display_all:
                              print(item,end="")

'''
The STILIX_LIST object can be used to perform simple operations on lists.The add_styles method can be used to add the desired items in the sender list to the reciever list.This is a way of adding stuff to lists with the
STILIX_LIST object.The remove_styles method can be used to remove the desired styles from the list.STILIX_LIST can also handle
when it comes to list output.The display all method can be used to display all the stuff from the list.The display_all_horizontol method can be used to display all of the items in the list in a horizontal way.

a = ["circle","square"]
STILIX_LIST.add_styles(a,["rectangle","oval"])
a then becomes ["circle","square","rectangle","oval"]
STILIX_LIST.remove_styles(a,["rectangle","oval"])
a then becomes ["circle","square"]
STILIX_LIST.display_all(a)
then comes the output
circle
square
a = ["circle ","square "]
STILIX_LIST.display_all_horizontal(a)
then comes the output
circle square
'''
@dataclass
class stilix_list_count:
          value: int
          def list_length(self,list_: list):
                    for item in list_:
                              self.value += 1
                    return self.value
          
          def list_count(self,list_: list,desired_counts: list):
                    for item in list_:
                              if item in desired_counts:
                                        self.value += 1
                    return self.value
          
          def reveal_item_indices(self,list_containing_item: list,items: list):
                    for item in items:
                              return list_containing_item.index(item)
          
'''
When it comes to list info the STILIX_LIST_COUNT object can handle that.Printing the list_length of the list can return the lists length.Printing the list_count of the desired items
in the list can return the amount of the desired items in the list.Printing the reveal_item_indices of the desired items in the list can return the indices of the desired items
in the list.
a = [5,6,6,7]
print(STILIX_LIST_COUNT.list_length(a))
4
print(STILIX_LIST_COUNT.list_count(a,[6]))
2
print(STILIX_LIST_COUNT.reveal_item_indices(a,[5,7]))
[0,3]
'''
          
STILIX_LIST = stilix_list()    

STILIX_LIST_COUNT = stilix_list_count(0)

@dataclass
class stilix:
          style: str = " * "
          def split_(self,storage: list,storage_to: list):
                    STILIX_LIST.add_styles(storage_to,storage)
                    
          def insert_style(self,storage: list):
                    value = 1
                    while value < STILIX_LIST_COUNT.list_length(storage):
                              storage.insert(value,self.style)
                              value += 2
                               
          def change_style(self,desired_style: str):
                    self.style = f" {desired_style} "

STILIX = stilix([])

'''
The STILIX object can be used for further list output.The insert_style method can be used to insert the * symbol between the stuff in the list.Now all you can do is use one
of the list output methods to generate a nice list output.However inserting the * symbol into the list can cause problems with the indices of the other stuff in the list.
You can use the split_ method to have two same lists.One list can be used to process the stuff , another list can be used for inserting the * symbol into it and to be the output.
Dont like the default * symbol, you can use the change_style method to switch the * symbol to your desired symbol.

a = ["circle","rectangle"]
STILIX.insert_style(a)
STILIX_LIST.display_all_horizontal(a)

circle * square

a = ["circle","square"]
STILIX.change_style("//")
STILIX.insert_style(a)
STILIX_LIST.display_all_horizontal(a)

circle // square

a , b= ["m","e"] , []
STILIX.split_(a,b)
STILIX.insert_style(a)
STILIX_LIST.display_all_horizontal(a)
print(f"{b[0]}{b[1]})

m * e
me

'''