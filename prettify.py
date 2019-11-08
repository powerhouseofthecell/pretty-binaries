import matplotlib.pyplot as plt
import numpy as np
import math

import os

import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
    "infile",
    type=str,
    help="the filepath to the file you want to see as an image"
)

ap.add_argument(
    "-o",
    "--outfile",
    type=str,
    default="prettified",
    help="the base filepath for the output file (if saving)"
)

ap.add_argument(
    "-d",
    action="store_true",
    help="if passed, will NOT save the resulting image"
)

ap.add_argument(
    "--no-display",
    action="store_true",
    help="if passed, will NOT display the image while the script runs"
)

ap.add_argument(
    "--colormap",
    type=str,
    default="gray",
    help="the matplotlib colormap to use for the image"
)

ap.add_argument(
    "--scale",
    type=int,
    default=1,
    help="dictates how many bytes to include in one 'pixel' of the output image (big files should probably use larger values here)"
)

args = ap.parse_args()

if __name__ == '__main__':
    if not os.path.isfile(args.infile):
        print(f"Invalid filepath: {args.infile}")
        exit(1)
    
    if args.scale < 1:
        print("Scale should be an integer > 0")
        exit(2)

    with open(args.infile, 'rb') as binary_file:
        binary_data = binary_file.read()

    binary_data = [format(b, 'b') for b in binary_data]

    scale = args.scale
    array = np.array([int(''.join(binary_data[i:i + scale]), 2) for i in range(0, len(binary_data) - scale + 1, scale)])

    # scale the array's values down to [0, 1]
    max_el = max(array)
    array = np.array([el / max_el * 255.0 for el in array], dtype=np.float32)

    # squarify the array
    square_len = math.floor(math.sqrt(len(array)))
    array = array[:square_len ** 2]
    array = np.reshape(array, (square_len, square_len))

    # show the actual image
    fig = plt.imshow(array, cmap=args.colormap, vmin=0, vmax=255, aspect='equal')

    # turn off axes
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    # save the figure
    if not args.d:
        plt.savefig(args.outfile, bbox_inches='tight', pad_inches=0)

    # display the figure
    if not args.no_display:
        plt.show()