#Connection to Google Drive
from google.colab import drive
drive.mount('/content/drive')

#Read & Display the generic geojson file
!pip install geopandas
import geopandas as gpd
file_path = '/content/drive/MyDrive/xView_train.geojson'
gdf = gpd.read_file(file_path)
print(gdf)

#Filter annotations by NRMM type_id, save in new GeoJSON, and display filtered file
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