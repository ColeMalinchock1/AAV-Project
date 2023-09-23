import tkinter
import tkintermapview

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
map_widget.set_position(35.948987,-79.102532, marker=False)  # Chapel Hill, NC
# map_widget.set_zoom(17)

# set current position with address
map_widget.set_address("Starting Location", marker=True)

# Adding markers
def add_marker_event(coords):
    global waypoints
    new_marker = map_widget.set_marker(coords[0], coords[1])
    waypoints.append([coords[0] , coords[1]])
    path_maker()
    
# Left click
map_widget.add_left_click_map_command(add_marker_event)

# set a path
def path_maker():
    global waypoints
    if len(waypoints) > 1:
        path = map_widget.set_path(waypoints)

root_tk.mainloop()