import arcpy
import os
from datetime import datetime

# mxd_path = "C:/Users/Admin/Desktop/new 9 brt.mxd"
mxd_path = "C:/Users/Admin/Desktop/new-9-brt1.mxd"
layer_name = "Final_House_Data_after_routing_and_code"
field_name = "NEAR_FID"


now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
print(dt_string)

#
base_directory = os.path.dirname(mxd_path)
new_folder_name = "Points_" + layer_name + "_" + dt_string
new_folder_path = os.path.join(base_directory, new_folder_name)

## Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)


mxd = arcpy.mapping.MapDocument(mxd_path)
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
# layer_name
layer = arcpy.mapping.ListLayers(data_frame, layer_name)[0]
print(layer)

# query = "NEAR_FID = 70"
# arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")


# Get unique values from the "NEAR_FID" field
unique_values = set()  # Using a set to ensure uniqueness
with arcpy.da.SearchCursor(layer, [field_name]) as cursor:
    for row in cursor:
        unique_values.add(row[0])

print("Unique values in 'NEAR_FID':", unique_values)


# for value in unique_values:

   

#     # Define a new layer name based on the unique value
#     new_layer_name = "fLayer_" + dt_string + "_" + str(value)

#     # Define the query to select rows with the current unique value
#     query = "{} = {}".format(field_name, value)

#     temp_layer_name = "tempLayer_" + str(value)

#     print(query)
#     # Create the new layer based on the query
    
#     # arcpy.MakeFeatureLayer_management(layer, temp_layer_name, query)
#     # arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
#     # time.sleep(1)
#     arcpy.SelectLayerByAttribute_management( arcpy.mapping.ListLayers(data_frame, layer_name)[0], "NEW_SELECTION", query)

#     arcpy.FeatureClassToFeatureClass_conversion(
#         temp_layer_name,
#         new_folder_path,
#         new_layer_name,
#         where_clause=query,
#     )

#     new_layer_path = os.path.join(new_folder_path, new_layer_name + ".shp")
#     try:
#         layer = arcpy.mapping.Layer(new_layer_path)
#         print("Layer is valid and created successfully - {}".format(new_layer_name))
#     except Exception as e:
#         print("Error creating layer:", e)
    
#     new_layer = arcpy.mapping.Layer(new_layer_path)
#     arcpy.mapping.AddLayer(data_frame, new_layer, "TOP")
#     new_layer.name = new_layer_name


for value in unique_values:
    # Construct the query to select rows with the current unique value
    query = "{} = {}".format(field_name, value)

    # Create a unique layer name
    new_layer_name = "Point_" + dt_string + "_" + str(value)

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
