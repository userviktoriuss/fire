import pyautocad
from pyautocad import APoint

acad = pyautocad.Autocad()

print(acad.doc.Name)

sel = acad.get_selection(text='Select circles:')
print(sel.Name)
print(sel.Count)
selected = []
for e in acad.iter_objects():
    print(e.ObjectID) # затея: перебрать все объекты и сравнить айди с выбранными, но хочется лучше.