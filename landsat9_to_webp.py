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

        new_arr[:, :, 3][blue != 0] = 255  # 透明度.
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

