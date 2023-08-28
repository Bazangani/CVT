import numpy as np
import cv2
from skimage.segmentation import find_boundaries
from SelectiveSearch.Histo import Hist_color

def Region_Similarity_score(self):
    pair_region = {}

    for i in self.labels:
        boundries = find_boundaries(self.segmented_image == i, mode='outer')
        neighbours_labels = np.unique(self.segmented_image[boundries]).tolist()  # the neighbouring label of label i
        LAB_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        for j in neighbours_labels:
            color_hist_j = Hist_color(self.segmented_image == j, self.image)
            texture_hist_j = Hist_color(self.segmented_image == j, LAB_img)
            size_j = (self.segmented_image == j).sum()

            if i < j:
                sim = 0
                # color histogram
                color_hist_i = Hist_color(self.segmented_image == i, self.image)
                color_sim = sum([min(a, b) for a, b in zip(color_hist_i, color_hist_j)])

                # texture histogram
                texture_hist_i = Hist_color(self.segmented_image == i, LAB_img)
                texture_sim = sum([min(a, b) for a, b in zip(texture_hist_i, texture_hist_j)])

                # size histogram
                size_i = (self.segmented_image == i).sum()
                size_sim = 1.0 - (size_i + size_j) / self.image.size

                # calculate the similarity
                sim = color_sim + texture_sim + size_sim
                pair_region[(i, j)] = sim

    return pair_region

