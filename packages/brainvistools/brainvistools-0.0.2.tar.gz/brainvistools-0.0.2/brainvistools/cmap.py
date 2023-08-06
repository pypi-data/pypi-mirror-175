import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors


def hex_to_rgb(value):
    """Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values

    :param value: hexcode
    :type value: str
    :return: rgba value
    :rtype: tuple
    """
    value = value.strip("#")  # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    """Converts rgb to decimal colours (i.e. divides each value by 256)

    :param value: rgb values
    :type value: tuple
    :return: decimal rgb values
    :rtype: tuple
    """
    return [v / 256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    """creates and returns a color map that can be used in heat map figures.
    If float_list is not provided, colour map graduates linearly between each color in hex_list.
    If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

    :param hex_list: list of hex code strings
    :type hex_list: list
    :param float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and
    end with 1., defaults to None
    :type float_list: list, optional
    :return: color map
    :rtype: matplotlib.colors.LinearSegmentedColormap
    """
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(["red", "green", "blue"]):
        col_list = [
            [float_list[i], rgb_list[i][num], rgb_list[i][num]]
            for i in range(len(float_list))
        ]
        cdict[col] = col_list
    cmp = mpl.colors.LinearSegmentedColormap("my_cmp", segmentdata=cdict, N=256)
    return cmp


def double_cmap(cmap, reverse=True):
    """Double colormap. Extend colors with reversed version (mirroring).

    :param cmap: Matplotlib colormap or string indicating one.
    :type cmap: matplotlib.colors.ListedColormap, str
    :param reverse: _description_, defaults to True
    :type reverse: bool, optional
    :return: _description_
    :rtype: _type_
    """
    if isinstance(cmap, str):
        clrs = plt.get_cmap(cmap)(np.linspace(0.0, 1, 128))
        clrs2 = plt.get_cmap(cmap)(np.linspace(0.0, 1, 128))
    else:
        clrs = cmap(np.linspace(0.0, 1, 128))
        clrs2 = cmap(np.linspace(0.0, 1, 128))

    if reverse:
        clrs = np.vstack(((np.flip(clrs2, axis=0), clrs)))
    else:
        clrs = np.vstack((clrs, np.flip(clrs2, axis=0)))

    mymap = colors.LinearSegmentedColormap.from_list("my_colormap", clrs)
    return mymap
