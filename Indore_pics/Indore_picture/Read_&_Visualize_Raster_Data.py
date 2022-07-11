import os
from sqlite3 import TimeFromTicks
from osgeo import gdal
from osgeo import _osr
import matplotlib.pyplot as plt
import numpy as np
import math
import pprint

#Moving to directory where tif files are stored:
base_dir=r'E:\SSSSSSS\YASH\Desktop_15-09-2021\ANGT\Python_codes\IIRS ISRO Geoprocessing\Overview-of-Geoprocessing-using-Python-IIRS-ISRO\Indore_pics\Indore_picture'
os.chdir(base_dir)
file_name='BAND5.tif'
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

print("Upper Left Corner: ",gdal.ApplyGeoTransform(gt,0,0))
print("Upper Right Corner: ",gdal.ApplyGeoTransform(gt,ds.RasterXSize,0))
print("Lower Left Corner: ",gdal.ApplyGeoTransform(gt,0,ds.RasterYSize))
print("Lower Left Corner: ",gdal.ApplyGeoTransform(gt,ds.RasterXSize,ds.RasterYSize))
print("Centre: ",gdal.ApplyGeoTransform(gt,ds.RasterXSize/2,ds.RasterYSize/2))

print("Meta-Data: ",ds.GetMetadata())
pprint.pprint(ds.GetMetadata())         #Information is printed in a readable way using pprint

print('Image Structure: ',ds.GetMetadata('IMAGE_STRUCTURE'))
print('Number of bands: ',ds.RasterCount)

#Get Information of each band:
for i in range(1,ds.RasterCount+1):                                #starting index from 1 since bands are numbered from 1
    band=ds.GetRasterBand(i)
    interp=band.GetColorInterpretation()
    interp_name=gdal.GetColorInterpretationName(interp)
    (width,height)=band.GetBlockSize()
    print('Band {0:d}, block size {1:d} {2:d},color interp {3:s}'.format(i,width,height,interp_name))

    ovr_count=band.GetOverviewCount()
    for j in range(ovr_count):                                    #starting index from 0 as overview bands startts from 0
        ovr_band=band.GetOverview(j)
        print('Overview %d: %dx%d'%(j,ovr_band.XSize,ovr_band.YSize))

#for deleting dataset ds use ds.del
#Get statistics of image using command: "gdalinfo -stats -nomd BAND2.tif" after getting into image location.
#Using python to get statistics of all bands:

for i in range(1,ds.RasterCount+1):
    band=ds.GetRasterBand(i)
    (Minimum,Maximum,Mean,Stddevi)=band.ComputeStatistics(False)       #Passing argument as false calculate statistics for image and passing true calculate it for overview band
    print('Band{:d}, Minimum: {:.3f}, Maximum: {:.3f},Mean: {:.3f}, Stddevi: {:.3f}'.format(i,Minimum,Maximum,Mean,Stddevi))

band=ds.GetRasterBand(1)
data=band.ReadAsArray()                                  #stores a band as numpy array data
print(data)
plt.figure(figsize=(10,10))
plt.imshow(data,cmap='gray')
plt.colorbar()
plt.show()


#Plotting all band image: 
plt.figure(figsize=(30,30))
for i in range(1,ds.RasterCount+1):                      #Each band show image for different electromagnetic wavelength
    band=ds.GetRasterBand(i)
    data=band.ReadAsArray()
    plt.subplot(1,3,i)
    plt.imshow(data,cmap='gray')
    plt.colorbar()
    plt.show()

#----------------------------------------Visualise MultiBand Raster--------------------------------------------------------
    
#multi_data=ds.ReadAsArray()                                                     #use this if your image have multiple bands
#multi_data.shape
#reshape_data=np.stack((multi_data[0],multi_data[1],multi_data[2]),axis=-1)
#plt.figure(figsize=(10,10))
#plt.imshow(reshape_data)
#plt.show()

#----------------------------------------Reading Partial Image-------------------------------------------------------------

band=ds.GetRasterBand(1)
data=band.ReadAsArray(xoff=511,yoff=338,win_xsize=512,win_ysize=512)
data.shape
plt.imshow(data,cmap='jet')
plt.show()

#---------------------------------------Reading Raster Blockwise-----------------------------------------------------------

band=ds.GetRasterBand(1)
x_size=ds.RasterXSize
y_size=ds.RasterYSize
block_size_x,block_size_y=band.GetBlockSize()
print(block_size_x,block_size_y)

for x in range(0,x_size,block_size_x):               #Reading columns
    if x+block_size_x < x_size:
        columns=block_size_x
    else:
        columns=x_size - x

    for y in range(0,y_size,block_size_y):               #Reading rows
        if y+block_size_y < y_size:
            rows=block_size_y
        else:
            rows=y_size - y

    data=band.ReadAsArray(x,y,columns,rows)
    print(data)

print("Outside loop: ",data)
print(data.shape)
