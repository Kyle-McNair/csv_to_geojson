# csv to geojson

This is a Python script that converts coordinates from a csv file into a point feature in geojson format. The following is required to run the script:
* Python version 3.X
* Pandas Python module
* csv that has XY coordinates. Please note, make sure the coordinates you have are in the desired projection. The script does not reproject anything.

Steps to run the script:
1. On command line, setup the file path where your csv is located. This is where your geojson file will be saved.
2. Run the script (Python csv_to_geojson.py)
3. The script will first ask the file path of the csv file that will need to be entered.
  * Example-- Enter the csv file path: C:\Users\person\xy_coordinates.csv
4. Script will then ask for the column name of X (Longitude) and Y (Latitude) in order to continue running.
5. Finally, the script will ask the desired output name of your geojson file.
6. You should be all set, convert away!
