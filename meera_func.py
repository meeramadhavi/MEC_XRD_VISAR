
from PIL import Image
import fabio
import os


def import_tiff(filename):
    """opens and returns the TIFF file

    Args:
        filename (string): give the filename and path as a string

    Returns:
        _type_: an image matrix
    """
    # Open the TIFF image
    image = fabio.open(filename).data

    # Display the image
    #image.show()
    return image



def get_files(directory, extension):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                all_files.append((file, file_path))
    return all_files



def line_mask(x, m = 4.8, c = 345):
    """_summary_

    Args:
        x (_type_): _description_
        m (float, optional): _description_. Defaults to 4.8.
        c (int, optional): _description_. Defaults to 345.

    Returns:
        _type_: _description_
    """
    y = m*x+c
    return y

def get_fit_guess(df, run_no = int, num_peaks = int):
    
    temp_run_fit_params=df.loc[df['Run No']==run_no]

    if num_peaks == 2:
        p0 = temp_run_fit_params[['B_Guess', 'I0_Guess', 'P0_Guess', 'G0_Guess', 'I1_Guess', 'P1_Guess', 'G1_Guess']].values[0]
        B_low = temp_run_fit_params[['B_Low', 'I0_Low', 'P0_Low', 'G0_Low', 'I1_Low', 'P1_Low', 'G1_Low']].values[0]
        B_high = temp_run_fit_params[['B_High', 'I0_High', 'P0_High', 'G0_High', 'I1_High', 'P1_High', 'G1_High']].values[0] #.values to change from pandas data frame to np array values. this is a nested list so taking the [0] so that you get the actual list. if confused change and check

    elif num_peaks == 3:
        p0 = temp_run_fit_params[['B_Guess', 'I0_Guess', 'P0_Guess', 'G0_Guess', 'I1_Guess', 'P1_Guess', 'G1_Guess', 'I2_Guess', 'P2_Guess', 'G2_Guess']].values[0]
        B_low = temp_run_fit_params[['B_Low', 'I0_Low', 'P0_Low', 'G0_Low', 'I1_Low', 'P1_Low', 'G1_Low', 'I2_Low', 'P2_Low', 'G2_Low']].values[0]
        B_high = temp_run_fit_params[['B_High', 'I0_High', 'P0_High', 'G0_High', 'I1_High', 'P1_High', 'G1_High', 'I2_High', 'P2_High', 'G2_High']].values[0] #.values to change from pandas data frame to np array values. this is a nested list so taking the [0] so that you get the actual list. if confused change and check
        
    elif num_peaks == 4:
        p0 = temp_run_fit_params[['m_Guess','B_Guess', 'I0_Guess', 'P0_Guess', 'G0_Guess', 'I1_Guess', 'P1_Guess', 'G1_Guess', 'I2_Guess', 'P2_Guess', 'G2_Guess','I3_Guess', 'P3_Guess', 'G3_Guess']].values[0]
        B_low = temp_run_fit_params[['m_Low', 'B_Low', 'I0_Low', 'P0_Low', 'G0_Low', 'I1_Low', 'P1_Low', 'G1_Low', 'I2_Low', 'P2_Low', 'G2_Low',  'I3_Low', 'P3_Low', 'G3_Low']].values[0]
        B_high = temp_run_fit_params[['m_High', 'B_High', 'I0_High', 'P0_High', 'G0_High', 'I1_High', 'P1_High', 'G1_High', 'I2_High', 'P2_High', 'G2_High','I3_High', 'P3_High', 'G3_High']].values[0] #.values to change from pandas data frame to np array values. this is a nested list so taking the [0] so that you get the actual list. if confused change and check
    
    
    return p0, (B_low, B_high)