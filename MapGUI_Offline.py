from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App

class SelectLocation(App):
    def build(self):
        mapview = MapView(zoom=11, lat=50.6394, lon=3.057)

        # Function to add a marker on map click
        def add_marker_event(instance, location, *args):
            marker = MapMarker(lat=location[0], lon=location[1])
            mapview.add_marker(marker)

        # Bind the map click event to add_marker_event function
        mapview.bind(on_map_click=add_marker_event)

        print(type(mapview.export_to_png("map.png")))

        return mapview


if __name__ == '__main__':
    SelectLocation().run()
