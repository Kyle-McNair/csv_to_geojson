# csv to geojson

This is a Python script that converts coordinates from a csv file into a point feature in geojson format. The following is required to run the script:
* Python version 3.X
* Modules Needed:
  - Pandas
  - PyQt5
* csv that has XY coordinates. Please note, make sure the coordinates you have are in the desired projection. The script does not reproject anything.

Steps to run the script:
1. On command line, setup the file path where your csv is located. 
2. Run the script (Python csv_to_geojson.py)
3. The script will bring up a GUI to execute the conversion. 
![alt text](gui.png)
4. Browse through folder directory to find the csv file.
5. Once the csv is found, you can select which x/y field in the dropdown selection.
6. Browse to desired folder location and name the file name.
7. Click on the "Convert to geojson" to convert!

