import arcpy
import os
from datetime import datetime

mxd_path = "C:/Users/Admin/Desktop/new-9-brt1.mxd"
layer_name = "FINAL final road"
#field_name = "NEAR_FID"
# query = "UID = '72SAR0'" 
query = "{} = {}".format("FID", 70)

route_id_field = "UID"


now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
print(dt_string)

#
base_directory = os.path.dirname(mxd_path)
new_folder_name = "Routes_" + layer_name + dt_string
new_folder_path = os.path.join(base_directory, new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

mxd = arcpy.mapping.MapDocument(mxd_path)
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

# layer_name
layer = arcpy.mapping.ListLayers(data_frame, layer_name)[0]

# Define the query to select `FID` 70

# Select features with the specified query
arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

# Validate the selection
selection_count = arcpy.GetCount_management(layer).getOutput(0)
print("Number of features selected:", selection_count)



print(layer)

# Define the output path for the route feature class
# output_route_path = new_folder_path #"C:/Path/To/Your/Output/Routes.gdb/Routes"
output_route_path = os.path.join(new_folder_path, "Route_{}.shp".format(dt_string))  # Ensure .shp extension for shapefiles

# Create routes from the target layer
# arcpy.CreateRoutes_lr(
#     in_line_features=layer,
#     route_id_field=route_id_field,  # Field to define unique routes
#     out_feature_class=output_route_path,
#     measure_source="LENGTH",
#       coordinate_priority="UPPER_LEFT",  # Using length as the measure source
# )

arcpy.CreateRoutes_lr(
    in_line_features=layer,
    route_id_field=route_id_field,
    out_feature_class=output_route_path,
    measure_source="LENGTH",
    measure_offset=0,  # Example offset in measure units
    measure_factor=1,  # Example factor to scale measures
    coordinate_priority="UPPER_LEFT",
)

print("Routes created and saved to:", output_route_path)


# Load the created routes
routes_layer = arcpy.mapping.Layer(output_route_path)




# Add the created route layer to the data frame
arcpy.mapping.AddLayer(data_frame, routes_layer, "TOP")





# new_layer_name = "fLayer_" + dt_string + "_70" 

# arcpy.FeatureClassToFeatureClass_conversion(
#     layer,
#     new_folder_path,
#     new_layer_name,
#     where_clause=query,
# )

# new_layer_path = os.path.join(new_folder_path, new_layer_name + ".shp")
# print(new_layer_path)


# try:
#     layer = arcpy.mapping.Layer(new_layer_path)
#     print("Layer is valid and created successfully")
# except Exception as e:
#     print("Error creating layer:", e)

# new_layer = arcpy.mapping.Layer(new_layer_path)
# arcpy.mapping.AddLayer(data_frame, new_layer, "TOP")
# new_layer.name = new_layer_name

mxd.save()
