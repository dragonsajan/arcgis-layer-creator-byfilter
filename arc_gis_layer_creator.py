import arcpy
import os
from datetime import datetime

mxd_path = "C:/Users/Admin/Desktop/new 9 brt.mxd"
layer_name = "Final_House_Data_after_routing_and_code"
field_name = "NEAR_FID"


now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
print(dt_string)

#
base_directory = os.path.dirname(mxd_path)
new_folder_name = "layers_" + layer_name + dt_string
new_folder_path = os.path.join(base_directory, new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)


mxd = arcpy.mapping.MapDocument(mxd_path)
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
# layer_name
layer = arcpy.mapping.ListLayers(data_frame, layer_name)[0]
print(layer)

arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")


# Get unique values from the "NEAR_FID" field
unique_values = set()  # Using a set to ensure uniqueness
with arcpy.da.SearchCursor(layer, [field_name]) as cursor:
    for row in cursor:
        unique_values.add(row[0])

print("Unique values in 'NEAR_FID':", unique_values)


for value in unique_values:
    # Construct the query to select rows with the current unique value
    query = "{} = {}".format(field_name, value)

    # Create a unique layer name
    new_layer_name = "fLayer_" + dt_string + "_" + str(value)

    # Create a new temporary layer for each unique value
    temp_layer_name = "tempLayer_" + str(value)
    arcpy.MakeFeatureLayer_management(layer, temp_layer_name, query)

    # Create a new feature class from the selected features
    arcpy.FeatureClassToFeatureClass_conversion(
        temp_layer_name,
        new_folder_path,
        new_layer_name,
    )

    # Path to the new layer
    new_layer_path = os.path.join(new_folder_path, new_layer_name + ".shp")

    # Add the new layer to the data frame
    new_layer = arcpy.mapping.Layer(new_layer_path)
    arcpy.mapping.AddLayer(data_frame, new_layer, "TOP")

    # Clear the temporary layer to avoid conflicts
    arcpy.Delete_management(temp_layer_name)

    print("Created and added new layer:", new_layer_name)


mxd.save()
