import arcpy
import os
import re

def extract_number_from_filename(filename):
    # Extract numbers from the filename using regular expression
    match = re.search(r'(\d+)_dissolved', filename)
    if match:
        return int(match.group(1))
    else:
        return None

def add_field_and_update_value(shapefile_path, field_name, value):
    try:
        # Check if the field already exists
        fields = arcpy.ListFields(shapefile_path)
        field_names = [field.name for field in fields]
        if field_name not in field_names:
            # Add the field
            arcpy.AddField_management(shapefile_path, field_name, "TEXT")
            print("Field '{}' added to {}.".format(field_name, shapefile_path))
        
        # Update the field with the specified value
        with arcpy.da.UpdateCursor(shapefile_path, [field_name]) as cursor:
            for row in cursor:
                row[0] = value
                cursor.updateRow(row)
        
        print("Field '{}' in {} updated with value '{}'.".format(field_name, shapefile_path, value))
    
    except Exception as e:
        print("Error: {}".format(str(e)))

def process_shapefiles_in_directory(directory, field_name):
    try:
        # Iterate over each shapefile in the directory
        for filename in os.listdir(directory):
            if filename.endswith("_dissolved.shp"):
                shapefile_path = os.path.join(directory, filename)
                
                # Extract the numerical part from the filename
                num_part = extract_number_from_filename(filename)
                
                if num_part is not None:
                    gu_value = "GU_{:03}".format(num_part)
                    
                    # Add and update the field in the shapefile
                    add_field_and_update_value(shapefile_path, field_name, gu_value)
                else:
                    print("Could not extract number from filename '{}'. Skipping this file.".format(filename))
        
        print("Process completed for all shapefiles in the directory.")
    
    except Exception as e:
        print("Error: {}".format(str(e)))

# Input parameters
shapefile_directory = r"D:\ex\diss"  # Path to the directory containing shapefiles
field_name = "keterangan"  # Name of the new field

# Ensure the directory exists
if os.path.exists(shapefile_directory):
    # Call the function to process all shapefiles in the directory
    process_shapefiles_in_directory(shapefile_directory, field_name)
else:
    print("Directory {} does not exist.".format(shapefile_directory))
