from dataclasses import dataclass
from d_tool import d_management_display
from Stilix_data_change import empty_list
@dataclass
class ladder_:
          ladder_design_storage: list[str]
          def set_amount(self,amount: int,list_: list):
                    list_.append(amount)
          
LADDER_ = ladder_(["-"])

class ladder_hewn_:
                    
          def design_ladder(self,amount: int):
                    while amount > 0:
                              print(LADDER_.ladder_design_storage[0])
                              amount -= 1

          def ladder_amount(self,amount_of_ladder: list[int]):
                    d_management_display.store_(True,amount_of_ladder[0])
          
          def change_ladder_style(self,desired_style: any):
                    LADDER_.ladder_design_storage[0] = desired_style

LADDER_HEWN_ = ladder_hewn_()

'''
The LADDER_HEWN_ object manages further output.Ladder hewn inserts design between two text.

text 1
-
-
-
text 2

The LADDER_ object contains the default - symbol which is used to print a desired amount of it between two pieces of text.The design_ladder method of LADDER_HEWN_can be used to print a desired amount of - symbols.
The ladder_amount method of the LADDER_HEWN_ object displays the amount of -s printed but the list containing the amount should be put in the brackets when your calling the method.LADDER_HEWN_.ladder_amount(list containing amount).
The amount can be stored by the LADDER_.set_amount method in your desired list.Dont want to use -s , you can use the LADDER_HEWN_.change_ladder_style method to change to your desired style

a = []
LADDER_.set_amount(1,a)
LADDER_HEWN_.change_ladder_style("w")
LADDER_HEWN_.design_ladder(a[0])
LADDER_HEWN_.ladder_amount(a)

w
1
'''

