
from typing import AbstractSet, Any
from abc import ABC , abstractmethod

class d_display:
          def store_(self,should_store_: bool,item_to_store: Any):
                    store_dict = {
                              True:item_to_store
                    }
                    return store_dict.get(should_store_)

class my_class(ABC):
          @abstractmethod
          def save(self):
                    pass
          
          @abstractmethod
          def process(self):
                    pass
          
          @abstractmethod
          def display(self):
                    pass
          
d_management_display = d_display()

'''
The d_management_display object displays an item depending on the boolean entered.
The my_class abstract class can be used to make custom classes based on the methods save_ , process and display.
my_class indicates that it is your class that you coded.

def do_(my_class):
          def save(self,something):
                    #some code
                    
          def process(self,something):
                    #some code
          
          def display(self,something):
                    #some code

value = 1
t = False

if value == 1:
          t = True
          d_management_display.store_(t,value)

'''