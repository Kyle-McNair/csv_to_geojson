#########################################
#### csv_to_geojson.py               ####
#### Author: Kyle McNair             ####
#### Last Updated: November 29, 2020 ####
#########################################

# pandas and json needed
import pandas as pd
import json

# geojson function converts pandas data frame data to geojson format
def geojson(df, x, y, outputfile):
    fc = {"type":"FeatureCollection"}
    col = []
    for c in df.columns:
        col.append(c)
    col.remove(x)
    col.remove(y)
    features = []
    properties = {}
    for index, row in df.iterrows():
        X = row[x]
        Y = row[y]
        coordinates = [X,Y]
        for c in col:
            properties.update({c:row[c]})
        data_dict = {"type":"Feature","geometry":{"type":"Point","coordinates":coordinates},"properties":properties}
        features.append(data_dict)
    fc.update({"features":features})
    geojson = json.dumps(fc)
    with open(outputfile + '.json','w') as geojson_file:
        geojson_file.write(geojson)
    geojson_file.close()

# columnCheck checks the data frame if the input fields are there or not
def columnCheck(df, field):
    if field == "X":
        while True:
            Xcolumn = input("\nEnter the X (Longitude) Field: ")
            try:
                for c in df.columns:
                    if c == Xcolumn:
                        return Xcolumn
                if Xcolumn not in df.columns:
                        raise Exception
            except:
                print ("Column not found, please try again...")
            
    elif field == "Y":
        while True:
            Ycolumn = input("\nEnter the Y (Latitude) Field: ")
            try:
                for c in df.columns:
                    if c == Ycolumn:
                        return Ycolumn
                if Ycolumn not in df.columns:
                    raise Exception
            except:
                print ("Column not found, please try again...")
        
            
csv = input("Enter the csv file path: ")

df = pd.read_csv(csv)
df = pd.DataFrame(df)

x_field = columnCheck(df,"X")
y_field = columnCheck(df,"Y")

output = input("\nEnter the name of the output geojson file: ")
    
geojson(df, x_field, y_field, output)

print ("\ncsv file converted to geojson!")
