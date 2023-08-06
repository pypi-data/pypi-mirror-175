import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm, colors


def formatted_colorbar(
    data,
    ax=None,
    unit=r"$R_{KL}$",
    orientation="vertical",
    title_pos="right",
    cmap=None,
    **kwargs,
):
    """Plot formatted colorbar into matplotlib.pyplot.figure or stand-alone

    :param data: TVBase data array
    :type data: numpy.array
    :param ax: axis of a matplotlib.pyplot.subplot, defaults to None
    :type ax: matplotlib.pyplot.axis, optional
    :param unit: Unit of the data, defaults to 'R'
    :type unit: str, optional
    :param fontsize: Fontsize, defaults to 12
    :type fontsize: int, optional
    :return: Plotted colorbar
    :rtype: matplotlib.pyplot.figure
    """
    fontsize = 12

    mpl.rcParams["font.sans-serif"] = "Arial"
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.size"] = fontsize

    # data = np.round(data, 3)
    if "vmin" not in kwargs.keys():
        vmin = np.nanmin(data)
    else:
        vmin = kwargs["vmin"]

    if "vmax" not in kwargs.keys():
        vmax = np.nanmax(data)
    else:
        vmax = kwargs["vmax"]

    abs_extrema = np.max([abs(vmin), abs(vmax)])

    # Set cbar tick labels.
    if vmin < 0:
        if vmax > 0:
            ticks = [-abs_extrema, 0, abs_extrema]
            norm = colors.TwoSlopeNorm(vmin=-abs_extrema, vcenter=0.0, vmax=abs_extrema)
        if vmax < 0:
            ticks = [vmin, 0]
            norm = mpl.colors.Normalize(vmin=vmin, vmax=0)
    else:
        ticks = [0, vmax]
        norm = mpl.colors.Normalize(vmin=0, vmax=vmax)

    # Check if inserted in figure or create new one.
    if not ax:
        fig_exist = False
        fig, ax = plt.subplots(figsize=(0.25, 2))
    else:
        fig_exist = True

    # Get colorbar from matplotlib if cbar input is string.
    if isinstance(cmap, type(None)):
        # TODO: Change back when tvbase_cmap is adapted to new nilearn style.
        # cmap = tvbase_cmap(data)
        cmap = "hot_r"

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    # cb = mpl.colorbar.ColorbarBase(
    #     ax, orientation=orientation, cmap=cmap, norm=norm, ticks=ticks  # vmax and vmin
    # )
    cb = mpl.colorbar.ColorbarBase(
        ax,
        orientation=orientation,
        ticks=ticks,  # [0, 0.5, 1],
        cmap=cmap,
        norm=norm,
    )

    cb.set_ticklabels(np.round(ticks, 3))
    cb.outline.set_visible(False)
    if title_pos in ["up", "top"]:
        cb.ax.set_title(unit, size=fontsize)

    elif title_pos == "right":
        cb.ax.set_ylabel(
            unit, fontsize=fontsize, labelpad=-0.5, **{"rotation": "horizontal"}
        )
    else:
        cb.ax.set_title("")
        cb.ax.set_ylabel("")

    for t in cb.ax.get_yticklabels():
        t.set_fontsize(fontsize)

    ax.patch.set_alpha(0)
    if not fig_exist:
        plt.close(fig)
        return fig


def add_colorbar(
    fig, ax, vmin=0, vmax=1, cmap="viridis", unit="", font_kwargs={}, pad=0.05
):
    cbar = fig.colorbar(
        cm.ScalarMappable(norm=plt.Normalize(vmin, vmax), cmap=cmap),
        ax=ax,
        ticks=[vmin, vmax],
        fraction=0.025,
        use_gridspec=True,
        pad=pad,
    )
    cbar.outline.set_visible(False)
    cbar.ax.set_yticklabels([np.round(vmin, 2), np.round(vmax, 2)], **font_kwargs)
    cbar.set_label(unit, rotation=0)
    fig.tight_layout()

    return cbar
