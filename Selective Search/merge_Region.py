
def Merge_Region(self,i, j):
    new_label = max(self.labels) + 1

    self.labels.append(new_label)

    region_i, region_j = self.region[i], self.region[j]

    new_size = region_i["size"] + region_j["size"]
    new_box = (min(region_i["box"][0], region_j["box"][0]),
               min(region_i["box"][1], region_j["box"][1]),
               min(region_i["box"][2], region_j["box"][2]),
               min(region_i["box"][3], region_j["box"][3])
               )
    value = {
        'size': new_size,
        "box": new_box,
        "color_hist": (region_i["color_hist"] * region_i["size"] + region_j["color_hist"] * region_j[
            "size"]) / new_size,
        "texture_hist": (region_i["texture_hist"] * region_i["size"] + region_j["texture_hist"] * region_j[
            "size"]) / new_size
    }
    self.region[new_label] = value

    return self.region
