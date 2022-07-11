import os
from sqlite3 import TimeFromTicks
from osgeo import gdal
from osgeo import _osr
import matplotlib.pyplot as plt
import numpy as np
import math

#Moving to directory where tif files are stored:
base_dir=r'E:\SSSSSSS\YASH\Desktop_15-09-2021\ANGT\Python_codes\IIRS ISRO Geoprocessing\Overview-of-Geoprocessing-using-Python-IIRS-ISRO\Indore_pics\Indore_picture'
os.chdir(base_dir)
file_name='BAND2.tif'
#Use command 'gdalinfo -nomd BAND2.tif' to get the transformation information about the tif file without metadata.
#Now by using Python code we extract this data:
ds=gdal.Open(file_name)
print(ds)                                      #output : <osgeo.gdal.Dataset; proxy of <Swig Object of type 'GDALDatasetShadow *' at 0x000002A7CDF53540> >
print("File List: ",ds.GetFileList()) 
print("Width: ",ds.RasterXSize) 
print("Height: ",ds.RasterYSize) 
print("Coordinate System: ",ds.GetProjection())

gt=ds.GetGeoTransform()
print("Geo-Transformation Information: ",gt)
print("Origin: ",(gt[0],gt[3]))
print("Pixel Size: ",(gt[1],gt[5]))