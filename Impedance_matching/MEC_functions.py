import numpy as np
import matplotlib.pyplot as plt
import scipy
import pandas as pd 
from shapely.geometry import  LineString

# function to flip across interface velocity
def reflected_hugo(x, interface_velocity):
    """This function flips the hugoniot

    Args:
        x (array): particle velocity
        interface_velocity (float): mirror point (interface velocity in this case)

    Returns:
        mirror x array: flipped x
    """
    results = 2*interface_velocity-x
    return results 

def impedance_match(data_1 = str, data_2 = str, interface_velocity = float):
    """impedance matching

    Args:
        data_1 (string, excel with Up and P): Path to the excel with the standard window to which we are impedance matching. Defaults to str.
        data_2 (string, excel with U and P): Path to the excel with the sample hugoniot which will be flipped. Defaults to str.
        interface_velocity (float): The interface velocity which you find from VISAR across which we will flip.  Defaults to float.

    Returns:
        y + x and y floats  : The window pressure and the sample Up and Sample P
    """
    LiF_Hugoniot = pd.read_excel(data_1, header=0)
    SLG_Hugoniot = pd.read_excel(data_2, header=0)
    
    # Interpolating data

    num_interp_points = 50000

    x_LIF = np.linspace(min(LiF_Hugoniot['Up']), max(LiF_Hugoniot['Up']), num_interp_points)

    y_LiF_interp = np.interp(x_LIF, LiF_Hugoniot["Up"], LiF_Hugoniot['P'])

    x_SLG = np.linspace(min(SLG_Hugoniot['Up']), max(SLG_Hugoniot['Up']), num_interp_points)

    y_SLG_interp = np.interp(x_SLG, SLG_Hugoniot["Up"], SLG_Hugoniot['P'])
    
    # Creating a vertical line at interface velocity for intersection
    x_vertical =np.zeros(50000)+ interface_velocity
    y_vertical = np.linspace(0,400, 50000)

    line_1 = LineString(np.column_stack((x_vertical, y_vertical)))
    line_2 = LineString(np.column_stack((x_LIF, y_LiF_interp)))
    intersection = line_1.intersection(line_2)

    x_1, y_1 = intersection.xy
    
    # Creating a horizontal line
    x_horizontal = np.linspace(-10,10,50000)
    y_horizontal = np.zeros(50000)+y_1

    line_1 = LineString(np.column_stack((x_horizontal, y_horizontal)))
    line_2 = LineString(np.column_stack((x_SLG, y_SLG_interp)))
    intersection = line_1.intersection(line_2)

    x_2, y_2 = intersection.xy
    
    # shifting SLG on top of the LiF at the interface velocity

    shift_value = x_2[0] - interface_velocity
    x_shift_SLG = x_SLG - shift_value 

    # flipped SLG
    x_flip_SLG = reflected_hugo(x_shift_SLG, interface_velocity)
    
    line_1 = LineString(np.column_stack((x_flip_SLG, y_SLG_interp)))
    line_2 = LineString(np.column_stack((x_SLG, y_SLG_interp)))
    intersection = line_1.intersection(line_2)

    x_3, y_3 = intersection.xy
    return y_1[0], x_3[0], y_3[0] 

# Window_P, Sample_Up, Sample_P = impedance_match("/Users/meera94/Desktop/LCLS MEC LX99/MEC2022_code/Impedance_matching/LiF hugoniot.xlsx", "/Users/meera94/Desktop/LCLS MEC LX99/MEC2022_code/Impedance_matching/RenganathanSLG.xlsx", 3)

# print(Window_P, Sample_Up, Sample_P)
