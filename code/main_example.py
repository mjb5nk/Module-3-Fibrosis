import cv2
from termcolor import colored
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 1. Configuration
filenames = [
    r"images/MASK_Sk658 Llobe ch010017.jpg",
    r"images/MASK_Sk658 Llobe ch010071.jpg",
    r"images/MASK_Sk658 Llobe ch010039.jpg",
    r"images/MASK_Sk658 Slobe ch010110.jpg",
    r"images/MASK_Sk658 Slobe ch010126.jpg",
    r"images/MASK_Sk658 Slobe ch010159.jpg",
]

depths = [45, 810, 15, 5300, 6800, 860]

# 2. Processing (Consolidated into one loop)
white_percents = []
results_log = []

print(colored("Counts of pixel by color in each image", "yellow"))

# Use zip to iterate through filenames and depths simultaneously
for i, (fname, depth) in enumerate(zip(filenames, depths)):
    # Read image in grayscale
    img = cv2.imread(fname, 0)
    
    if img is None:
        print(colored(f"Error: Could not load {fname}", "red"))
        continue

    # Threshold and count pixels
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    white = np.sum(binary == 255)
    black = np.sum(binary == 0)
    
    # Calculate percentage
    percent = 100 * (white / (white + black))
    white_percents.append(percent)

    # Print first set of requirements (Pixel Counts)
    print(colored(f"White pixels in image {i}: {white}", "white"))
    print(colored(f"Black pixels in image {i}: {black}", "black"))
    print()
    
    # Store data for the second print loop to maintain your specific output order
    results_log.append((fname, percent, depth))

# 3. Print Summary (Percentage and Depth)
print(colored("Percent white px:", "yellow"))
for fname, percent, depth in results_log:
    print(colored(f'{fname}:', "red"))
    print(f'{percent}% White | Depth: {depth} microns\n')

# 4. Write to CSV
df = pd.DataFrame({
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})

df.to_csv('Percent_White_Pixels.csv', index=False)
print("The .csv file 'Percent_White_Pixels.csv' has been created.")


##############
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

# interpolate_depth = float(input(colored(
#     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# x = depths
# y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# i = interp1d(x, y, kind='linear')
# interpolate_point = i(interpolate_depth)
# print(colored(
#     f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# depths_i = depths[:]
# depths_i.append(interpolate_depth)
# white_percents_i = white_percents[:]
# white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# fig, axs = plt.subplots(2, 1)

# axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
# axs[0].set_title('Plot of depth of image vs percentage white pixels')
# axs[0].set_xlabel('depth of image (in microns)')
# axs[0].set_ylabel('white pixels as a percentage of total pixels')
# axs[0].grid(True)


# axs[1].scatter(depths_i, white_percents_i, marker='o',
#                linestyle='-', color='blue')
# axs[1].set_title(
#     'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
# axs[1].set_xlabel('depth of image (in microns)')
# axs[1].set_ylabel('white pixels as a percentage of total pixels')
# axs[1].grid(True)
# axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
#                color='red', s=100, label='Highlighted point')


# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
