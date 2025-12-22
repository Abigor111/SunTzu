from .test import Person
from. test2 import Info, Relationships
p = Person("Igor", Info(30, "Lisboa"), Relationships([]))

p.birthday()           # método de Info
p.add_friend("Rui")    # método de Relationships
