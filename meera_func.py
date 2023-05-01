
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
