import sys
import re

if len(sys.argv) == 2:
    growthfactor = 1.0
elif len(sys.argv) == 3:
    growthfactor = float(sys.argv[2])
else:
    print('usage: python obj2mc.py myobject.obj [growthfactor]')
    sys.exit(1)

obj = open(sys.argv[1])
json = open(sys.argv[1] + '.json', 'w')

#start with dummy coordinates because obj is one-indexed
coordinates = ['0.0,0.0,0.0']
slashremover = r'([0-9\.\-]*)/[0-9\.\-]*/[0-9\.\-]*'
firstline = True #used to make sure the final face has no comma at the end
offset = 0.5 #makes the center of the block the origin, not the corner

json.write('''{
\t"name": "steak_styles",
\t"faces": [
''')

for line in obj:
    splitline = line.strip().split()
    if splitline and splitline[0] == 'v':
        coords = [float(splitline[1]), float(splitline[2]),
                  float(splitline[3])]
        for i in range(3):
            coords[i] = (coords[i] * growthfactor) + offset
            coords[i] = round(coords[i], 10)
        coord_string = ','.join(str(coord) for coord in coords)
        coordinates.append(coord_string)
    if splitline and splitline[0] == 'f':
        for i in range(1, 4):
            #change "f 1/2/3 4/5/6 7/8/9" to "f 1 4 7"
            splitline[i] = re.sub(slashremover, r'\1', splitline[i])
        coord_ids = (int(splitline[1]), int(splitline[2]),
                     int(splitline[3]))
        
        if firstline:
            firstline = False
        else:
            json.write(',\n')
        json.write('{"vertices":[')
        
        json.write('{"position":[')
        json.write(coordinates[coord_ids[0]])
        json.write('],"texcoord":[0,0]},')
        
        json.write('{"position":[')
        json.write(coordinates[coord_ids[1]])
        json.write('],"texcoord":[0,16]},')
        
        json.write('{"position":[')
        json.write(coordinates[coord_ids[2]])
        json.write('],"texcoord":[16,0]},')

        #duplicate third triangle corner because MC requires quadrilaterals
        json.write('{"position":[')
        json.write(coordinates[coord_ids[2]])
        json.write('],"texcoord":[16,16]}') #omit the comma here or MC crashes

        json.write(']}')
        
json.write('''
\t]
}''')

obj.close()
json.close()
