from skimage.segmentation import find_boundaries
from DataSet.PascalVoCDataset import PascalVOCDataset
from scipy.ndimage import find_objects
import numpy as np
from SelectiveSearch.Graphbasedinitpy import GraphBasedinit
import cv2
import os
import random
import matplotlib.pyplot as plt

from SelectiveSearch.Region_Val import Regions_values
from SelectiveSearch.SimilScorRegion import Region_Similarity_score
from SelectiveSearch.merge_Region import Merge_Region
from SelectiveSearch.Updat_Similarity import update_regions_sim


class SelectiveSearch:
    def __init__(self, segmented_image, image):
        self.segmented_image = segmented_image
        self.labels = np.unique(self.segmented_image).tolist()  # list of the labels
        self.image = image
        self.region = {}

    def Find_max_sim(self, pair_region):
        max_similarity_pair = max(pair_region, key=pair_region.get)
        ij = list(max_similarity_pair)
        return ij[0], ij[1]

    def update_segmented_image(self, i, j):
        new_label = max(self.labels)
        for old_label in [i, j]:
            self.segmented_image[self.segmented_image == old_label] = new_label
        return segmented_image

    def method(self):
        regions = Regions_values(self)
        pair_region = Region_Similarity_score(self)
        # Initialize a set to store the merged regions
        for i in range(50):
            i, j = self.Find_max_sim(pair_region)
            merged_region = Merge_Region(self, i, j)
            self.update_segmented_image(i, j)
            pair_region = update_regions_sim(self, i, j, pair_region, regions)

        return merged_region


if __name__ == "__main__":
    # Now you can use the generated regions as potential object proposals
    dataset_dir = "C:/Users/farideh/Desktop/object detection/datasets/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/"
    image_list_path = "C:/Users/farideh/Desktop/object detection/datasets/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Layout/val.txt"

    dataset = PascalVOCDataset(dataset_dir, image_list_path)
    images, labels = dataset.get_data()
    # Choose a random image index
    random_image_idx = random.randint(0, len(images) - 1)

    # Get the random image and its associated labels
    random_image = images[random_image_idx]
    random_labels = labels[random_image_idx]

    # Load the original image without preprocessing
    image_filename = dataset.image_filenames[random_image_idx] + '.jpg'
    original_image_path = os.path.join(dataset.image_dir, image_filename)
    original_image = cv2.imread(original_image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # Original image
    plt.subplot(1, 4, 1)
    plt.imshow(original_image)
    plt.title('Original Image')
    plt.axis('off')

    graph_segmenter = GraphBasedinit(image=original_image, scale=100, sigma=0.5, min_size=600)
    segmented_image = graph_segmenter.Segment()
    plt.subplot(1, 4, 2)
    plt.imshow(segmented_image)
    plt.title('Segmented Image before')
    plt.axis('off')

    selective_searh = SelectiveSearch(segmented_image=segmented_image, image=original_image)
    merged_region = selective_searh.method()

    # Segmented image
    # Create a copy of the original image to avoid modifying it
    image_with_boxes = original_image.copy()

    plt.subplot(1, 4, 3)
    plt.imshow(segmented_image)  # You can choose a suitable colormap
    plt.title('Segmented Image')
    plt.axis('off')
    print(segmented_image)

    # Draw rectangles on the image based on the merged_region dictionary
    for label, info in merged_region.items():
        box = info['box']
        color = (0, 255, 0)  # Green color (BGR format)
        thickness = 2
        image_with_boxes = cv2.rectangle(image_with_boxes, (box[0], box[1]), (box[2], box[3]), color, thickness)

    plt.subplot(1, 4, 4)
    plt.imshow(image_with_boxes)
    plt.title('Segmented Image with Boxes')
    plt.axis('off')

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()
