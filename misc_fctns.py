# -*- coding: utf-8 -*-
'''Misc fctns used for analysis of data from FERMI DiProI endstation
    Some fctns are used by script 'autofill_excel.py'
    11-2020: Adapted by M Keller from script used by E Jal's group
'''
import numpy as np  
import matplotlib.pyplot as plt
import os
import glob as g
from scipy.optimize import curve_fit


#==================================================================================================
#==================================================================================================
class t: 
# t : text
# Colors class:reset all colors with colors.reset; two  
# sub classes fg for foreground  
# and bg for background; use as colors.subclass.colorname. 
# i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,  
# underline, reverse, strike through, 
# and invisible work with the main class i.e. colors.bold'''
    reset='\033[0m'
    bold='\033[1m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
#==================================================================================================
#==================================================================================================


#==================================================================================================
#==================================================================================================
def attention(sentence1 = False, sentence2 = False, sentence3 = False):
    if isinstance(sentence1, str)==False and\
       isinstance(sentence2, str)==False and\
       isinstance(sentence2, str)==False:
        st='   /\   \n  /  \  \n /____\ '
    elif isinstance(sentence1, str)==True and\
         isinstance(sentence2, str)==False and\
         isinstance(sentence2, str)==False:
        st='   /\   \n  /  \  {0}\n /____\ '.format(sentence1)
    elif isinstance(sentence1, str)==True and\
         isinstance(sentence2, str)==True and\
         isinstance(sentence3, str)==False:
        st='   /\   \n  /  \  {0}\n /____\ {1}'.format(sentence1, sentence2)
    elif isinstance(sentence1, str)==True and\
         isinstance(sentence2, str)==True and\
         isinstance(sentence3, str)==True:
        st='   /\   {0}\n  /  \  {1}\n /____\ {2}'.format(sentence1, sentence2, sentence3)
    print(t.bold + t.fg.red + st + t.reset)
#==================================================================================================
#==================================================================================================



#==================================================================================================
def ls(path = "pwd", st = False, option = "al", show = True, ret = False):
    '''Get list of files in a directory
    Options:
        Sort list alphabetically
        Sort list by modification time
        Print list
        Return list to caller (full paths or just basenames)
        '''
    # "al": alphabetic order
    # "t" : time order
    if path == "pwd":   # Caller didn't specify dir, so use CWD
        path = os.getcwd()
    if isinstance(st, str):   # Pattern to match must contain the string
        pathname = "{0}/*{1}*".format(path, st)
    else:
        pathname = "{0}/*".format(path)

    li = g.glob(pathname)   # Get list of items matching pathname

    if option == "al":   # Sort list alphabetically
        li.sort()
    elif option == "t":   # Sort list by modification time
        li.sort(key=os.path.getmtime)

    if show == True:   # Print the list
        print()
        for i in range(0, len(li)):
            print( os.path.basename(li[i]) )
        print()

    if ret == "name":   # Return list of basenames
        li_extract = []
        for item in li:
            li_extract.append(os.path.basename(item))
        return li_extract
    elif ret == "path" or ret == True :   # Return list of full paths
        return li
#====================================================================================================
#====================================================================================================



#==================================================================================================
#==================================================================================================
def lists_to_txt(*argv, name_file, ini_path=os.getcwd(), legend = [], overwrite=True, message = False, way="vertical"):
    """
     This function allows to write in a file, several lists.
     === Example ===
     a = [1, 2, 3, 4, 5]
     b = [11, 12, 13, 14, 15]
     c = [21, 22, 23, 24, 25]
     p = lists_to_txt(a, b, c, name_file = "test", way="vertical")
     in the file test.txt :
     1 11 21
     2 12 22
     3 13 23
     4 14 24
     5 15 25
    
     p = lists_to_txt(a, b, c, name_file = "test", way="horizontal")
     in the file test.txt :
      1  2  3  4  5
     11 12 13 14 15
     21 22 23 24 25
    
     The number of list as input is illimited
    ======================================================
    """

    # To test if all list input in *argv has all the same length
    lists = []
    for arg in argv:
        lists.append(arg) #it adds a new line in the variable lists
    
    for i in range(1, len(lists)):
        if len(lists[0]) != len(lists[i]):
            attention("lists_to_txt function",\
                      "The list {0} has not the same size than the first one".format(i),\
                      "len(li[0]) = {0}  |  len(li[{1}]) = {2}".format( len(lists[0]), i, len(lists[i]) ))
            return
    
    if len(legend) != 0 and len(legend) != len(lists):
        attention("the legend has not the same size than the number of input list",\
                  "len(legend) = {0}  |  nb_list = {1}".format(len(legend), len(lists)) )
        return
        
    
    
    # Allow to transfor a list of list into an array
    # Thus we can use the column
    lists = np.array(lists)
    nb_row, nb_col = lists.shape
    
    # Creation and filling of the file
    path_file = '{0}/{1}.txt'.format(ini_path, name_file)
    
    # If you don't want to overwrite in a existing file, try to read it
    if overwrite == False:
        try:
            open(path_file, "r")
            attention("{0}.txt already exists".format(name_file), "So it is not overwritten")
        except IOError:
            return
    
    text_file = open(path_file, "w")
    if len(legend) != 0:
        text_file.writelines("\t".join(legend))
        text_file.write("\n")
    
    if way == "vertical":
        for j in range(0, nb_col):
            s = [str(v) for v in lists[:, j]]
            text_file.writelines("\t".join(s))
            text_file.write("\n")
    
    if way == "horizontal":
        for j in range(0, nb_row):
            s = [str(v) for v in lists[j, :]]
            text_file.writelines("\t".join(s))
            text_file.write("\n")
    
    text_file.close()
    return path_file
#==================================================================================================
#==================================================================================================


#===== Some mask fctns, may or may not be useful ======
#======================================================
def rectangular_mask2(img, xc, yc, lx, ly):
  """
  Function to calculate radial mean on an image with a given
  circle center and radius.
 
  Arguments:
  - xc, yc - center of a circle
  - radius - radius on which the radial mean must be calculated (can be float with
             the fraction of the pixel size)
  - image  - image array
  """
 
  # get image size
  yN, xN = np.shape(img)
 
  # fcreate the meshgrid with the same size as the image and the circle center at
  # the [0,0] coordinates
  y,x = np.ogrid[-yc:yN-yc,-xc:xN-xc]
 
  # get two circular masks, the first one with the provided limit radius and the
  # second one with the radius incremented by size
  # all points on the circle with the r <= radius are True, and outside radius are False
  mask_x = x*x  <= lx*lx/4
  mask_y = y*y  <= ly*ly/4
  

  mask = (mask_x*mask_y).astype(float)
 
 
  # return mean value
  # return np.nanmean(result), result
  return mask

def radial_mask(img, xc, yc, radius, sizeradius):
  """
  Function to calculate radial mean on an image with a given
  circle center and radius.
 
  Arguments:
  - xc, yc - center of a circle
  - radius - radius on which the radial mean must be calculated (can be float with
             the fraction of the pixel size)
  - image  - image array
  """
 
  # get image size
  yN, xN = np.shape(img)
 
  # fcreate the meshgrid with the same size as the image and the circle center at
  # the [0,0] coordinates
  y,x = np.ogrid[-yc:yN-yc,-xc:xN-xc]
 
  # get two circular masks, the first one with the provided limit radius and the
  # second one with the radius incremented by size
  # all points on the circle with the r <= radius are True, and outside radius are False
  mask1 = x*x + y*y <= radius*radius
  mask2 = x*x + y*y <= (radius+sizeradius)*(radius+sizeradius)
  # from the two above masks get ring mask
  mask = np.logical_xor(mask1, mask2)
  # convert logical (False, True) values to 0 and 1
  mask = mask.astype(float)
 
  # replace all pixels outside the ring with NaN
  # mask[np.where(mask==0)] = np.nan
  # multiply mask and image
  #result = mask
 
  # return mean value
  # return np.nanmean(result), result
  return mask

def radial_mask2(img, xc, yc, radius):
  """
  Function to calculate radial mean on an image with a given
  circle center and radius.
 
  Arguments:
  - xc, yc - center of a circle
  - radius - radius on which the radial mean must be calculated (can be float with
             the fraction of the pixel size)
  - image  - image array
  """
 
  # get image size
  yN, xN = np.shape(img)
 
  # fcreate the meshgrid with the same size as the image and the circle center at
  # the [0,0] coordinates
  y,x = np.ogrid[-yc:yN-yc,-xc:xN-xc]
 
  # get two circular masks, the first one with the provided limit radius and the
  # second one with the radius incremented by size
  # all points on the circle with the r <= radius are True, and outside radius are False
  mask1 = x*x + y*y <= radius*radius
  

  mask = mask1.astype(float)
 
 
  # return mean value
  # return np.nanmean(result), result
  return mask


#==================================================================================================
#==================================================================================================
