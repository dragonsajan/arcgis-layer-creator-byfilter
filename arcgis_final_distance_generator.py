import arcpy
import os
from datetime import datetime
import time


###########################################################################
###########################################################################
################# Modify here #############################################

mxd_path = "D:/Ward 9 Trial/Ward 9 Trial.mxd" #"D:/new-9-brt1.mxd"

### Point
point_layer_name = "Final_HN_data_with_UID"
point_field_name = "NEAR_FID"
#

### Route
route_layer_name = "FINAL final road"
route_field_name = "FID"
route_coordinatePriority="UPPER_LEFT"
route_route_id_field = "UID"
#

###############################################################################
##############################################################################



















now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
print(dt_string)


#
base_directory = os.path.dirname(mxd_path)
point_new_folder_name = "Points_" + point_layer_name + "_" + dt_string
point_new_folder_path = os.path.join(base_directory, point_new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(point_new_folder_path):
    os.makedirs(point_new_folder_path)


mxd = arcpy.mapping.MapDocument(mxd_path)
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
# layer_name
point_layer = arcpy.mapping.ListLayers(data_frame, point_layer_name)[0]
print(point_layer)

# query = "NEAR_FID = 70"
# arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

arcpy.SelectLayerByAttribute_management(point_layer, "CLEAR_SELECTION")


# Get unique values from the "NEAR_FID" field
unique_values = set()  # Using a set to ensure uniqueness
with arcpy.da.SearchCursor(point_layer, [point_field_name]) as cursor:
    for row in cursor:
        unique_values.add(row[0])

print("Point Unique values in 'NEAR_FID':", unique_values)



for value in unique_values:
    # Construct the query to select rows with the current unique value
    point_query = "{} = {}".format(point_field_name, value)

    # Create a unique layer name
    point_new_layer_name = "Point_" + dt_string + "_" + str(value)

    # Create a new temporary layer for each unique value
    point_temp_layer_name = "tempLayer_" + str(value)
    arcpy.MakeFeatureLayer_management(point_layer, point_temp_layer_name, point_query)

    # Create a new feature class from the selected features
    arcpy.FeatureClassToFeatureClass_conversion(
        point_temp_layer_name,
        point_new_folder_path,
        point_new_layer_name,
    )

    # Path to the new layer
    point_new_layer_path = os.path.join(point_new_folder_path, point_new_layer_name + ".shp")

    # Add the new layer to the data frame
    poin_new_layer = arcpy.mapping.Layer(point_new_layer_path)
    arcpy.mapping.AddLayer(data_frame, poin_new_layer, "TOP")

    # Clear the temporary layer to avoid conflicts
    arcpy.Delete_management(point_temp_layer_name)

    print("Created and added new Point layer:", point_new_layer_name)


# mxd.save()
base_path, filename = os.path.split(mxd_path)

# Split the filename and extension
file_name_only, extension = os.path.splitext(filename)

# Insert the prefix before the extension
point_new_filename = "{}_1{}".format(file_name_only,extension)  # Inserted prefix

# Reconstruct the new path
point_new_mxd_path = os.path.join(base_path, point_new_filename)

print("Updated MXD path:", point_new_mxd_path)
mxd.saveACopy(point_new_mxd_path)
# data_frame.clear()
del mxd
print("##### - Point Layer completed")
print("Please Wait for next step.........")
time.sleep(1)

### End Point ############


### Start Route
##


route_new_folder_name = "Routes_" + route_layer_name + "_" + dt_string
route_new_folder_path = os.path.join(base_directory, route_new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(route_new_folder_path):
    os.makedirs(route_new_folder_path)

route_mxd = arcpy.mapping.MapDocument(point_new_mxd_path)
route_data_frame = arcpy.mapping.ListDataFrames(route_mxd)[0]

# layer_name
route_layer = arcpy.mapping.ListLayers(route_data_frame, route_layer_name)[0]

arcpy.SelectLayerByAttribute_management(route_layer, "CLEAR_SELECTION")

# Get unique values from the "NEAR_FID" field
unique_values = set()  # Using a set to ensure uniqueness
with arcpy.da.SearchCursor(route_layer, [route_field_name]) as cursor:
    for row in cursor:
        unique_values.add(row[0])
print("Route ids")
print(unique_values)

for value in unique_values:
    # Construct the query to select rows with the current unique value
    route_query = "{} = {}".format(route_field_name, value)

    # Create a unique layer name
    route_new_layer_name = "Route_" + dt_string + "_" + str(value)

    # Create a new temporary layer for each unique value
    route_temp_layer_name = "tempLayer_" + str(value)
    arcpy.MakeFeatureLayer_management(route_layer, route_temp_layer_name, route_query)

     # Path to the new layer
    route_new_layer_path = os.path.join(route_new_folder_path, route_new_layer_name + ".shp")

    arcpy.CreateRoutes_lr(
        in_line_features=route_temp_layer_name,
        route_id_field=route_route_id_field,
        out_feature_class=route_new_layer_path,
        measure_source="LENGTH",
        measure_offset=0,  # Example offset in measure units
        measure_factor=1,  # Example factor to scale measures
        coordinate_priority=route_coordinatePriority,
    )

   
    # Add the new layer to the data frame
    route_new_layer = arcpy.mapping.Layer(route_new_layer_path)
    arcpy.mapping.AddLayer(route_data_frame, route_new_layer, "TOP")

    # Clear the temporary layer to avoid conflicts
    arcpy.Delete_management(route_temp_layer_name)

    print("Created and added new Route layer:", route_new_layer_name)


base_path, filename = os.path.split(mxd_path)

# Split the filename and extension
file_name_only, extension = os.path.splitext(filename)

# Insert the prefix before the extension
route_new_filename = "{}_2{}".format(file_name_only,extension)  # Inserted prefix

# Reconstruct the new path
route_new_mxd_path = os.path.join(base_path, route_new_filename)

print("Updated MXD path:", route_new_mxd_path)
route_mxd.saveACopy(route_new_mxd_path)
# mxd.save()
del route_mxd
print("##### - Route Layer completed")
print("Please Wait for next step.........")
time.sleep(1)

### End Route ############



## Locator
##

locate_route_layer_name = "Route_{}_".format(dt_string)  # Adjust to the correct route layer name
locate_point_layer_name = "Point_{}_".format(dt_string)  # Adjust to the correct point layer name

locate_route_id_field = route_route_id_field #  "UID" # Unique column name
locate_route_field_name = route_field_name #"FID" # to get the id of route layers => should match with route_field_name


main_route_layer_name = route_layer_name # "FINAL final road" # layer name to get fid list


#
locate_new_folder_name = "Table_" + route_layer_name + point_layer_name + dt_string
locate_new_folder_path = os.path.join(base_directory, locate_new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(locate_new_folder_path):
    os.makedirs(locate_new_folder_path)


locate_mxd = arcpy.mapping.MapDocument(route_new_mxd_path)
locate_data_frame = arcpy.mapping.ListDataFrames(locate_mxd)[0]

# List all layers to ensure the desired ones are present
locate_available_layers = [lyr.name for lyr in arcpy.mapping.ListLayers(locate_data_frame)]
# print("Available layers:", available_layers)


# layer_name
locate_for_route_layer = arcpy.mapping.ListLayers(locate_data_frame, main_route_layer_name)[0] 
arcpy.SelectLayerByAttribute_management(locate_for_route_layer, "CLEAR_SELECTION")

# Get unique values from the "NEAR_FID" field
locate_unique_values = set()  # Using a set to ensure uniqueness
with arcpy.da.SearchCursor(locate_for_route_layer, [route_field_name]) as cursor:
    for row in cursor:
        locate_unique_values.add(row[0])

print(locate_unique_values)


for value in locate_unique_values:
    locate_temp_route_layer_name = locate_route_layer_name + str(value)
    locate_temp_point_layer_name = locate_point_layer_name + str(value)
    # Check if the layers exist
    if locate_temp_route_layer_name not in locate_available_layers:
        raise ValueError("Route layer '{}' does not exist in the data frame".format(locate_temp_route_layer_name))

    if locate_temp_point_layer_name not in locate_available_layers:
        # raise ValueError("Point layer '{}' does not exist in the data frame".format(point_layer_name))
        print("Point layer '{}' does not exist in the data frame".format(locate_temp_point_layer_name))
        continue
    
    # Get the route and point layers
    locate_route_layer = arcpy.mapping.ListLayers(locate_data_frame, locate_temp_route_layer_name)[0]
    locate_point_layer = arcpy.mapping.ListLayers(locate_data_frame, locate_temp_point_layer_name)[0]


    # Define the output event table
    # output_event_table =  "C:/Path/To/Your/Event/Table.dbf"  # Adjust to a valid path
    locate_output_event_table = os.path.join(locate_new_folder_path, "Table_{}_{}.dbf".format(locate_temp_route_layer_name, locate_temp_point_layer_name))

    # Set the search radius in meters
    locate_search_radius_in_meters = "1000 Meters"  # Example: 10 meters


    # Use "Locate Features Along Routes" with specified radius and measure field
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features=locate_point_layer,
        in_routes=locate_route_layer,
        route_id_field=locate_route_id_field,  # Specify the measure field
        radius_or_tolerance=locate_search_radius_in_meters,
        out_table=locate_output_event_table,
    )

    # Create a new table layer from the event table
    event_table_layer = arcpy.mapping.TableView(locate_output_event_table)

    # Add the event table to the data frame
    arcpy.mapping.AddTableView(locate_data_frame, event_table_layer)

    print("Features located along the route and saved to:", locate_output_event_table)


base_path, filename = os.path.split(mxd_path)

# Split the filename and extension
file_name_only, extension = os.path.splitext(filename)

# Insert the prefix before the extension
locate_new_filename = "{}_3{}".format(file_name_only,extension)  # Inserted prefix

# Reconstruct the new path
locate_new_mxd_path = os.path.join(base_path, locate_new_filename)

print("Updated MXD path:", locate_new_mxd_path)
locate_mxd.saveACopy(locate_new_mxd_path)
# mxd.save()
del locate_mxd
