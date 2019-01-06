from czml import czml
with open('Ground.czml','r',encoding='utf-8') as f:
    m=czml.CZML()
    m.loads(f.read())
print(m.packets())