# Connection to Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Read & Display the generic geojson file
!pip install geopandas
import geopandas as gpd
file_path = '/content/drive/MyDrive/xView_train.geojson'
gdf = gpd.read_file(file_path)
print(gdf)

# Filter annotations by NRMM type_id, save in new GeoJSON, and display filtered file
!pip install geopandas
import geopandas as gpd
file_path = '/content/drive/MyDrive/xView_train.geojson'
gdf = gpd.read_file(file_path)
nrmm_type_ids = {60, 63, 64, 61, 55, 59, 54, 65, 53, 32, 66, 56, 62, 57}
nrmm_annotations = gdf[gdf['type_id'].isin(nrmm_type_ids)]
output_file = '/content/drive/MyDrive/nrmm_annotations.geojson'
nrmm_annotations.to_file(output_file, driver='GeoJSON')
print(f"NRMM annotations saved to {output_file}")
print("\nContenuto di nrmm_annotations.geojson:")
with open(output_file, 'r') as f:
    content = f.read()
print(content)

# Counts the number of bounding boxes in every NRMM image
import geopandas as gpd
file_path = '/content/drive/MyDrive/nrmm_train_annotations.geojson'
gdf = gpd.read_file(file_path)
bbox_count = {}
for index, row in gdf.iterrows():
    image_id = row['image_id']
    if image_id in bbox_count:
        bbox_count[image_id] += 1
    else:
        bbox_count[image_id] = 1
for image_id, count in bbox_count.items():
    print(f"Immagine {image_id}: {count} bounding box")
total_images_with_annotations = len(bbox_count)
print(f"\nNumero totale di immagini con annotazioni: {total_images_with_annotations}")

# Converts the bouning box coodinates (in every NRMM image) from an image format to a YOLO format (through the calculation of the train images dimensions)
# and creates a text file in the same directory as the trian image to save the YOLO coordinates and the subject type_ID (the type of NRMM machinary)
!pip install geopandas pillow
import geopandas as gpd
import os
from PIL import Image
from google.colab import drive
drive.mount('/content/drive')
file_path = '/content/drive/MyDrive/nrmm_train_annotations.geojson'
def convert_to_yolo_coordinates(bounds, img_width, img_height):
    x_min, y_min, x_max, y_max = [int(coord) for coord in bounds.split(',')]
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    width = x_max - x_min
    height = y_max - y_min
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height
    return x_center, y_center, width, height
if os.path.exists(file_path):
    gdf = gpd.read_file(file_path)
    images_dir = '/content/drive/MyDrive/train_images'
    for index, row in gdf.iterrows():
        image_id = row['image_id']
        bounds = row['bounds_imcoords']
        type_id = row['type_id']
        image_path = os.path.join(images_dir, image_id)
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                img_width, img_height = img.size
            yolo_coords = convert_to_yolo_coordinates(bounds, img_width, img_height)
            text_file_path = os.path.join(os.path.dirname(image_path), f"{os.path.splitext(image_id)[0]}.txt")
            with open(text_file_path, 'a') as f:
                f.write(f"{type_id} {' '.join(map(str, yolo_coords))}\n")
        else:
            print(f"Image not found: {image_path}")
else:
    print(f"File not found: {file_path}")

# Fixing a bug related to wrong name in txt files (.tif.txt bug)
import os
folder_path = '/content/drive/MyDrive/train_images'
files = os.listdir(folder_path)
for filename in files:
    if filename.endswith('.txt'):
        try:
            new_filename = os.path.join(folder_path, filename.replace('.tif.txt', '.txt'))
            os.rename(os.path.join(folder_path, filename), new_filename)
            print(f"File rinominato: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Errore durante la rinomina di {filename}: {e}")

# Deleting the non-NRMM images in train_images folder using the .txt files created 
import os
folder_path = '/content/drive/MyDrive/train_images'
txt_numbers = set()
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        txt_numbers.add(filename.replace('.txt', ''))
for filename in os.listdir(folder_path):
    if filename.endswith('.tif'):
        num = filename.replace('.tif', '')
        if num not in txt_numbers:
            try:
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"File eliminato: {file_path}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {file_path}: {e}")

import os

# Counting the number of NRMM tif (images) and txt files
images_dir = '/content/drive/MyDrive/train_images'
txt_count = 0
tif_count = 0
for filename in os.listdir(images_dir):
    if filename.endswith('.txt'):
        txt_count += 1
    elif filename.endswith('.tif'):
        tif_count += 1
print(f"Numero di file txt: {txt_count}")
print(f"Numero di file tif: {tif_count}")
