import diffllib   # Fuzzy string matching lib
import ogr
from difflib import get_close_matches
from logging import logger
  


def fix_class_id_from_name(shape_path, id_field, name_field, name_to_id_dict):
    """DANGER: IN-PLACE FUNCTION. DO NOT USE WITHOUT BACKING UP SHAPEFILE.
    Walks through every feature in shapefile at shape_path, comparing name_field to
    an internal lookup table and replacing id_field appropriately."""
    shapefile = ogr.Open(shape_path, 1)
    layer = shapefile.GetLayer()
    for feature in layer:
        # If the name of a feature is within match_threshold of a key in name_to_id_dict, update id_field
        name = feature.GetField(name_field)
        match = get_close_matches(name, name_to_id_dict.keys(), n = 1).first()
        try:
            print("Setting {} to id value {}".format(name, name_to_id_dict[match]))
            feature.SetFieldInteger64(name_to_id_dict[match])
        except KeyError:
            print("No match for {} found in name_to_id_dict".format(name))
            
if __name__ == "__main__":
    
    name_to_id_dict = {
        "Stable Forest": 1,
        "Forest To Other Veg": 2,
        "Forest To None Veg": 3,
        "Stable Veg": 4,
        "Other Veg To None Veg": 5,
        "Other Veg To Forest": 6,
        "Stable Non Veg": 7,
        "Non Veg To Other Veg": 8,
        "Non Veg To Forest": 9,
        "Water": 10
        }
    
    shape_path = "/path/to/shapefile/WITH/BACKUP!"
    id_field = "Id"
    name_field = "Class"
    
    fix_class_id_from_name(shape_path, id_field, name_field, name_to_id_dict)