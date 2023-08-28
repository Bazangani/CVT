import skimage.segmentation as seg
from DataSet.PascalVoCDataset import PascalVOCDataset
import random
import cv2
import os
import matplotlib.pyplot as plt

class GraphBasedinit:
    """
        A class for performing graph-based initialization using the Felzenszwalb segmentation algorithm.

        Parameters:
        - image: The input image to be segmented.
        - scale: The scale parameter for Felzenszwalb segmentation. Higher means larger clusters.
        - sigma: The sigma parameter for Felzenszwalb segmentation. Width (standard deviation) of Gaussian kernel used in preprocessing.
        - min_size: The minimum component size for Felzenszwalb segmentation. Minimum component size. Enforced using postprocessing.
        output : Integer mask indicating segment labels.
        """

    def __init__(self, image, scale, sigma, min_size):
        self.image = image
        self.scale = scale
        self.sigma = sigma
        self.min_size = min_size

    def Segment(self):
        segmented_img = seg.felzenszwalb(self.image, scale=self.scale, sigma=self.sigma, min_size=self.min_size)
        return segmented_img



if __name__ == "__main__":
    # Now you can use the generated regions as potential object proposals
    dataset_dir = "C:/Users/farideh/Desktop/object detection/datasets/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/"
    image_list_path = "C:/Users/farideh/Desktop/object detection/datasets/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Layout/val.txt"

    dataset = PascalVOCDataset(dataset_dir, image_list_path)
    images, labels = dataset.get_data()
    print("Number of images:", len(images))
    print("Number of labels:", len(labels))
    # Choose a random image index
    random_image_idx = random.randint(0, len(images) - 1)

    # Get the random image and its associated labels
    random_image = images[random_image_idx]
    random_labels = labels[random_image_idx]

    # Load the original image without preprocessing
    image_filename = dataset.image_filenames[random_image_idx] + '.jpg'
    original_image_path = os.path.join(dataset.image_dir, image_filename)
    original_image = cv2.imread(original_image_path)
    graph_segmenter = GraphBasedinit(image=original_image, scale=50, sigma=0.5, min_size=300)
    segmented_image = graph_segmenter.Segment()
    print(original_image.shape)
    print(segmented_image.shape)

    # Original image
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title('Original Image')
    plt.axis('off')

    # Segmented image
    plt.subplot(1, 2, 2)
    plt.imshow(segmented_image)  # You can choose a suitable colormap
    plt.title('Segmented Image')
    plt.axis('off')

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()


