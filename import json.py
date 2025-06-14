import geopandas as gpd

# Cargar el archivo GeoJSON
archivo_geojson = "poligonos-localidades.geojson"
localidades = gpd.read_file(archivo_geojson)

# Mostrar las primeras filas del archivo
print(localidades.head())

# Verificar la columna de geometría
print(localidades.geometry)
