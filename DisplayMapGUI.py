import tkinter
import tkintermapview
from geopy import distance
import math
import csv

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# Storing Markers
waypoints = []

# Setting the radius
radius = 12

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# set other tile server (standard is OpenStreetMap)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

# set current position and zoom
map_widget.set_position(35.770743,-78.674817, marker=False)  # Chapel Hill, NC
# map_widget.set_zoom(17)

# set current position with address
map_widget.set_address("Starting Location", marker=True)

# Adding markers
def add_marker_event(coords):
    
    global waypoints

    # Getting the latitude and longitude from the coordinates
    lat = float(coords[0])
    lon = float(coords[1])

    # Creating a new marker at that lat lon
    new_marker = map_widget.set_marker(lat, lon)

    waypoints.append([lat , lon])
    path_maker()
    
    
# set a path
def path_maker():
    global waypoints
    if len(waypoints) > 1:
        path = map_widget.set_path(waypoints)
        print( path )

coords = []

with open("gps_data_converted.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        add_marker_event(row)
root_tk.mainloop()
