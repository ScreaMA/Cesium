from czml import czml
doc = czml.CZML()
packet1 = czml.CZMLPacket(id='document',version='1.0')
doc.packets.append(packet1)

# Create and append a billboard packet
def create(obj_id,longitude,latitude,height):
    packet2 = czml.CZMLPacket(id = obj_id)
    packet2.name = "BEIDOU1"
    lb = czml.Label(text="北斗卫星",show=True)
    lb.scale=0.5
    lb.pixelOffset = {'cartesian2':[50,-30]}
    packet2.label=lb
    packet2.position ={"cartographicDegrees" : [longitude,latitude,height]}
    md = czml.Model()
    md.gltf = "../../Models/a2100.gltf"
    md.maximumScale = 20000
    md.minimumPixelSize = 64
    packet2.model = md
    doc.packets.append(packet2)

create("Satellite2",105.2,39.2,20000)
# Write the CZML document to a file
filename = "test.czml"
doc.write(filename)