import cv2
from scipy.ndimage import find_objects
from SelectiveSearch.Histo import Hist_color

def Regions_values(self):
    for label in self.labels:
        size = (self.segmented_image == label).sum()
        bbox = find_objects(self.segmented_image == label)[0]
        box = tuple([bbox[i].start for i in (1, 0)] +  # (x, y) -> (y_start, x_start, y_stop, x_stop)
                    [bbox[i].stop for i in (1, 0)]
                    )
        mask = self.segmented_image == label
        Lab_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        color_hist = Hist_color(mask, self.image)
        texture_hist = Hist_color(mask, Lab_img)

        self.region[label] = {
            'size': size,
            "box": box,
            "color_hist": color_hist,
            "texture_hist": texture_hist
        }

    return self.region
