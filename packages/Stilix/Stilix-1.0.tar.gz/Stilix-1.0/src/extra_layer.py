from Stilix import STILIX_LIST
from dataclasses import dataclass

@dataclass
class extra_layer:
          extra_layer_storage: list[list]
          def add_layers(self,layers_amount: int):
                    while layers_amount > 0:
                              STILIX_LIST.add_styles(self.extra_layer_storage,[[]])
                              layers_amount -= 1
          
          def remove_layers(self,layers_to_remove_amount: int):
                    while layers_to_remove_amount > 0:
                              STILIX_LIST.remove_styles(self.extra_layer_storage,[[]])
                              layers_to_remove_amount -= 1
                              
          def display_layers(self):
                    STILIX_LIST.display_all(self.extra_layer_storage)
          
          def display_layers_horizontal(self):
                    STILIX_LIST.display_all_horizontal(self.extra_layer_storage)
                    
EXTRA_LAYER = extra_layer([])

'''
The EXTRA_LAYER object can be used to make multiple empty lists.Each empty list can be assigned to manage one task.The add_layers method can be used to add a desired amount of empty lists to EXTRA_LAYER.extra_layer_storage.
The remove layers method can be used to remove a desired amount of empty lists from EXTRA_LAYER.extra_layer_storage.The display_layers method can be used to display the empty lists vertically.The display_layers_horizontal
method can be used to display the empty lists horizontally.

EXTRA_LAYER.add_layers(3)

print(EXTRA_LAYER.extra_layer_storage)

[[],[],[]]

EXTRA_LAYER.remove_layers(1)

print(EXTRA_LAYER.extra_layer_storage)

[[],[]]

EXTRA_LAYER.display_layers()

[]
[]

EXTRA_LAYER.display_layers_horizontal()

[][]

'''