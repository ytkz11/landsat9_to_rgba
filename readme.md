# Landsat 9 

Download Landsat9 images from USGS. Landsat9 images differ from domestic images in the following ways:

1. The Landsat9 image has been geometrically corrected without rpc file.

  2.Landsat9 images are in the form of a single band, with each band saved as a separate file.



# True color RGBA for Landsat9

The second band of Landsat9 is known as Blue, Blue, or B

The third band of Landsat9 is Green, or G for short

The fourth band of Landsat9 is Red, or R for short





Next, write a function that does this:

Enter the folder decompressed by Landsat9 to obtain the file names of bands 2, 3, and 4 of Landsat9



The effect of this function is to facilitate automation, each image name is unique, if you have to manually specify the Landsat9 band 2, 3, 4 file name each time is time-consuming and laborious.

Analyze the tif name format of Landsat9 to extract the common naming rules.

![image-20231013172543805](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202310131725238.png)

LC09_L2SR_018113_20230209_20230310_02_T2_SR_B1.TIF has the following features

B1 stands for band 1, the first band.

The file suffix is TIF.

Based on these two points, the names of bands 2, 3 and 4 are automatically obtained.

Take a closer look at the following code:



```python
class landsat9_to_webp:
    def __init__(self, path):
       self.path = path
    def get_tif_file(self, file_dir, type = '.TIF'):
    
        """
        Search for files whose type extension does not include subdirectories
        """
        L = []
        if type(type) == str:
                if len([type]) == 1:
                    filelist = os.listdir(file_dir)
                    for file in filelist:
                        if os.path.splitext(file)[1] == type:
                            L.append(os.path.join(file_dir, file))
        if type(type) != str:
                if len(type) > 1:
                    for i in range(len(type)):
                        filelist = os.listdir(file_dir)
                        for file in filelist:
                            if os.path.splitext(file)[1] == type[i]:
                                L.append(os.path.join(file_dir, file))
        return L
```



Let's start by writing a class called landsat9_to_webp, which we often refer to as self. The input to the landsat9_to_webp class is the lansat9 folder path, so one of the properties of this class is the input path.



This class has a class method called get_tif_file, which is also a landsat9_to_webp attribute. The get_tif_file method searches for the file whose suffix is TIF in the specified folder. If the file exists, the get_tif_file method returns the list of qualified file names.

Here is an example

```python
path = r'X:\LC09_L2SP_121038_20220616_20230411_02_T1'
filelist = landsat9_to_webp(path).get_tif_file()
```

Let's print out the filelist loop and see what it looks like.

```python
import os
for file in filelist:
    print(os.path.basename(file))
```

Console print a message:

```
LC09_L2SP_121038_20220616_20230411_02_T1_QA_PIXEL.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_QA_RADSAT.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B1.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B2.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B3.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B4.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B5.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B6.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B7.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_QA_AEROSOL.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_ATRAN.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_B10.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_CDIST.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_DRAD.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_EMIS.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_EMSD.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_QA.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_TRAD.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_ST_URAD.TIF

```



Obviously, the filelist is a list of length 19, as shown in the screenshot below in pycharm

![image-20231013180036859](https://cdn.jsdelivr.net/gh/ytkz11/picture/imgs202310131800037.png)

By this time, we were halfway there.



The next step is to perform a data cleaning on this list, with the aim of stably finding the bands we need.

Basic friends will notice that the fourth element, fifth element, and sixth element of filelist are the B2, B3, and B4 bands that we need. Why do we still do data cleaning? The reasons are as follows:

It is not certain that the fourth element, the fifth element, and the sixth element of the filelist obtained each time are the bands of B2, B3, and B4 that we need.



For example, if I use sentinel-2 as an example, there are file structure differences between sentinel-2 L1C data and sentinel-2 L2A data, so there is no guarantee that every time a filelist[3], filelist[4], filelist[5] is the file name we want.



Here we write a few more lines of code to make sure that the next read is the file, which is Landsat9 bands 2, 3, and 4.

The stupid method is to loop the filelist list and add an if statement, if the current element exists B2.TIF, then the element is the name of the second band.

Let's write another class method,

Again, integrate the code as follows:

```python
class landsat9_to_webp:
    def __init__(self, path):
       self.path = path
    def get_tif_file(self, filetype = '.TIF'):
        # 
        """
      
        """
        L = []
        if type(filetype) == str:
                if len([filetype]) == 1:
                    filelist = os.listdir(self.path)
                    for file in filelist:
                        if os.path.splitext(file)[1] == filetype:
                            L.append(os.path.join(self.path, file))
        if type(filetype) != str:
                if len(filetype) > 1:
                    for i in range(len(filetype)):
                        filelist = os.listdir(self.path)
                        for file in filelist:
                            if os.path.splitext(file)[1] == type[i]:
                                L.append(os.path.join(self.path, file))
        return L
    
    
    def finded_2_3_4_band(self):
        filelist = self.get_tif_file()
        for file in filelist:
            if 'B2.TIF' in file:
                B2file = file
            elif  'B3.TIF' in file:
                B3file = file
            elif  'B4.TIF' in file:
                B4file = file
        return [B2file, B3file, B4file]
```



ok, call this class, this class has two methods finded_2_3_4_band, get_tif_file

Let's parse the running logic of this class so far.



First, instantiate the class.

Next, the finded_2_3_4_band method is called.

The finded_2_3_4_band method then calls the get_tif_file method.

Finally, a list is returned, which contains the elements B2file, B3file, and B4file.

```python
path = r'X:\LC09_L2SP_121038_20220616_20230411_02_T1'
filelist = landsat9_to_webp(path).finded_2_3_4_band()
      
```



Let's print out the filelist loop and see what it looks like.

```python
import os
for file in filelist:
    print(os.path.basename(file))
```

Console print a message:

```
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B2.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B3.TIF
LC09_L2SP_121038_20220616_20230411_02_T1_SR_B4.TIF
```

Complete a feature to get the file name of the second, third, and fourth bands of Landsat9 images through the folder



# GDAL reads tif

Once we have the corresponding file name, we read tif into memory via gdal.

Use numpy to create a matrix for [X,Y,4]. Return the matrix.



# Data stretching

Why do data stretching, I once wrote a public account to explain.

Because Landsat9's data type is 16bit, and the computer screen display range is 8bit, the process of 16bit to 8bit is called data stretching.



Linear stretching, also equal proportion stretching, the specific code is as follows:

```python
def linear_stretch(data, num=1):
    '''

@param data: Matrix to be stretched
@param num: Tensile coefficient, usually 1-5
@return: The stretched matrix
    '''
    x, y = np.shape(data)
    data_8bit = data
    data_8bit[data_8bit == -9999] = 0

    # Convert nan in the data to a specific value, for example
    # data_8bit[np.isnan(data_8bit)] = 0
    d2 = np.percentile(data_8bit, num)
    u98 = np.percentile(data_8bit, 100 - num)

    maxout = 255
    minout = 0
    data_8bit_new = minout + ((data_8bit - d2) / (u98 - d2)) * (maxout - minout)
    data_8bit_new[data_8bit_new < minout] = minout
    data_8bit_new[data_8bit_new > maxout] = maxout
    data_8bit_new = data_8bit_new.astype(np.int32)
    return data_8bit_new
```



# Clean up the code

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2023/10/13 18:35 
# @File : landsat9_to_webp.py

import numpy as np
import cv2
from osgeo import gdal
import os
"""
Read landsat9 images and generate thumbnails in rgba format
"""

class landsat9_to_webp:
    def __init__(self, path):
        self.path = path
        file_list = self.finded_2_3_4_band()
        self.bluefile = file_list[0]
        self.greenfile = file_list[1]
        self.redfile = file_list[2]
        self.outfile = os.path.splitext(self.redfile)[0][:-2] + '.png'
    def get_tif_file(self, filetype = '.TIF'):

        """
       Search for files whose filetype extension does not include subdirectories
        """
        L = []
        if type(filetype) == str:
            if len([filetype]) == 1:
                filelist = os.listdir(self.path)
                for file in filelist:
                    if os.path.splitext(file)[1] == filetype:
                        L.append(os.path.join(self.path, file))
        if type(filetype) != str:
            if len(filetype) > 1:
                for i in range(len(filetype)):
                    filelist = os.listdir(self.path)
                    for file in filelist:
                        if os.path.splitext(file)[1] == type[i]:
                            L.append(os.path.join(self.path, file))
        return L
    def finded_2_3_4_band(self):
        filelist = self.get_tif_file()
        for file in filelist:
            if 'B2.TIF' in file:
                B2file = file
            elif  'B3.TIF' in file:
                B3file = file
            elif  'B4.TIF' in file:
                B4file = file
        return [B2file, B3file, B4file]

    def read_tif(self):

        ds1 = gdal.Open(self.bluefile)
        blue = ds1.ReadAsArray()

        ds2 = gdal.Open(self.greenfile)
        green = ds2.ReadAsArray()

        ds3 = gdal.Open(self.redfile)
        red = ds3.ReadAsArray()

        x, y = blue.shape
        new_arr = np.zeros(shape=[x, y, 4])
        new_arr[:, :, 0] = linear_stretch(blue)
        new_arr[:, :, 1] = linear_stretch(green)
        new_arr[:, :, 2] = linear_stretch(red)

        new_arr[:, :, 3][blue != 0] = 255  # transparency.
        return new_arr
    def save_webp_by_opencv(self, new_arr, minification=6):
        '''

        @param new_arr: The array to be saved
        @param size: Scaling factor
        @return:
        '''
        # The size of the output picture
        new_x = int(new_arr.shape[0] / minification)
        new_y = int(new_arr.shape[1] / minification)

        # Zoom out
        gray_im = cv2.resize(new_arr, (new_x, new_y), interpolation=cv2.INTER_AREA)

        # Save as png image
        os.chdir(self.path)
        cv2.imwrite(os.path.basename(self.outfile), gray_im)

    def to_picture(self, minification=6):
        data = self.read_tif()
        self.save_webp_by_opencv(data, minification)

def linear_stretch(data, num=1):
    '''

    @param data: The matrix to be stretched
    @param num: Tensile coefficient, generally 1-5
    @return: The stretched matrix
    '''
    x, y = np.shape(data)
    data_8bit = data
    data_8bit[data_8bit == -9999] = 0

    # Convert nan in the data to a specific value, for example
    d2 = np.percentile(data_8bit, num)
    u98 = np.percentile(data_8bit, 100 - num)

    maxout = 255
    minout = 0
    data_8bit_new = minout + ((data_8bit - d2) / (u98 - d2)) * (maxout - minout)
    data_8bit_new[data_8bit_new < minout] = minout
    data_8bit_new[data_8bit_new > maxout] = maxout
    data_8bit_new = data_8bit_new.astype(np.int32)
    return data_8bit_new

if __name__ == '__main__':
    path = r'D:\xxxx'
    filelist = landsat9_to_webp(path).to_picture()


```



If it helps, likes are my biggest creative motivator.

![LC09_L2SP_044034_20220417_20220419_02_T1_SR_](D:\LC09_L2SP_044034_20220417_20220419_02_T1_SR_.png)
