import arcpy
import os
from datetime import datetime

mxd_path = "C:/Users/Admin/Desktop/new-9-brt1.mxd"

# Names of the layers to work with
route_layer_name = "Route_28042024090951_63"  # Adjust to the correct route layer name
point_layer_name = "Point_28042024090904_63"  # Adjust to the correct point layer name
route_id_field = "UID"


now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
print(dt_string)

#
base_directory = os.path.dirname(mxd_path)
new_folder_name = "Table_" + route_layer_name + point_layer_name + dt_string
new_folder_path = os.path.join(base_directory, new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

mxd = arcpy.mapping.MapDocument(mxd_path)
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

# List all layers to ensure the desired ones are present
available_layers = [lyr.name for lyr in arcpy.mapping.ListLayers(data_frame)]
# print("Available layers:", available_layers)



# Check if the layers exist
if route_layer_name not in available_layers:
    raise ValueError("Route layer '{}' does not exist in the data frame".format(route_layer_name))

if point_layer_name not in available_layers:
    raise ValueError("Point layer '{}' does not exist in the data frame".format(point_layer_name))


# Get the route and point layers
route_layer = arcpy.mapping.ListLayers(data_frame, route_layer_name)[0]
point_layer = arcpy.mapping.ListLayers(data_frame, point_layer_name)[0]

# Define the output event table
# output_event_table =  "C:/Path/To/Your/Event/Table.dbf"  # Adjust to a valid path
output_event_table = os.path.join(new_folder_path, "Table_{}{}.dbf".format(route_layer_name,point_layer_name))

# Set the search radius in meters
search_radius_in_meters = "1000 Meters"  # Example: 10 meters


# Use "Locate Features Along Routes" with specified radius and measure field
arcpy.LocateFeaturesAlongRoutes_lr(
    in_features=point_layer,
    in_routes=route_layer,
    route_id_field=route_id_field,  # Specify the measure field
    radius_or_tolerance=search_radius_in_meters,
    out_table=output_event_table,
)


# Create a new table layer from the event table
event_table_layer = arcpy.mapping.TableView(output_event_table)

# Add the event table to the data frame
arcpy.mapping.AddTableView(data_frame, event_table_layer)

print("Features located along the route and saved to:", output_event_table)

mxd.save()