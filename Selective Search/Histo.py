import numpy as np


def Hist_color(mask, image):
    """
          Calculate the color histogram of a given region within an image.
          Parameters:
              mask (numpy.ndarray): Binary mask indicating the region of interest.
              image (numpy.ndarray): Color image (with one or more channels).
          Returns:
              numpy.ndarray: Color histogram of the specified region.
          """
    if len(image.shape) == 2:
        image = image.reshape(image.shape[0], image.shape[1], 1)
    num_channel = image.shape[2]
    histo = np.array([])
    for ch in range(num_channel):
        layer = image[:, :, ch][mask]
        histo = np.concatenate([histo] + [np.histogram(layer, 20)[0]])
    histo = histo / np.sum(histo)
    return histo
