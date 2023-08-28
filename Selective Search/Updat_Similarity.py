import numpy as np
from skimage.segmentation import find_boundaries


def update_regions_sim(self, i, j, pair_region, regions):
    pair_to_find = (i, j)
    # print(pair_to_find)
    keys_to_delete = [key for key in pair_region.keys() if any(x in key for x in pair_to_find)]
    # print(keys_to_delete)

    for key in keys_to_delete:
        del pair_region[key]

    self.labels.remove(i)
    self.labels.remove(j)

    # print("The labels exist after deleting:", i in self.labels or j in self.labels)

    new_label = max(self.labels)  # we added the label before
    boundries = find_boundaries(self.segmented_image == new_label)
    neighbours_new_label = np.unique(self.segmented_image[boundries]).tolist()
    neighbours_new_label.remove(new_label)

    for i in neighbours_new_label:
        sim = 0
        size_sim = sum([min(a, b) for a, b in zip(regions[i]["color_hist"], regions[j]["color_hist"])])
        texture_sim = sum([min(a, b) for a, b in zip(regions[i]["texture_hist"], regions[j]["texture_hist"])])
        color_sim = sum([min(a, b) for a, b in zip(regions[i]["color_hist"], regions[j]["color_hist"])])

        # calculate the similarity
        sim = color_sim + texture_sim + size_sim
        pair_region[(new_label, i)] = sim

    return pair_region
