from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from brainvistools import cbar as bvcbar
from brainvistools import cmap as bvcm
from nilearn import plotting


def formatted_glass_brain(
    img,
    title=None,
    unit=r"$R_{KL}$",
    colorbar=True,
    display_mode="ortho",
    contours=None,
    alpha=0,
    cmap=None,
    fig=None,
    ax=None,
    figsize=(12, 4),
    # cbar_kwargs={},
    **kwargs,
):
    """Plots formatted version of the :func:`nilearn.plotting.plot_glass_brain

    :param img: Brain image in NIfTI format.
    :type img: nibabel.nifti1.Nifti1Image
    :param title: Plot title
    :type title: str
    :param unit: Unit for the colorbar, defaults to r"{KL}$"
    :type unit: regexp, str, optional
    :param colorbar: Adds colorbar to plot with :func:`~tvbase.plot.add_colorbar`, defaults to True
    :type colorbar: bool, optional
    :param display_mode: display_mode from :func:`nilearn.plotting.plot_glass_brain`, defaults to "ortho"
    :type display_mode: str, optional
    :param add_contours: Adds contours of the parcellation, defaults to False
    :type add_contours: bool, optional
    :param alpha: Alpha value (transparency) of the color map, defaults to 0
    :type alpha: int, optional
    :param cmap: color map: accepts string input for matplotlib cmap names, defaults to None
    :type cmap: str, optional
    :return: _description_
    :rtype: _type_
    """
    data = img.get_fdata()
    # TODO: Check new cmap handling in nilearn!
    # if isinstance(cmap, type(None)):
    #    cmap = tvbase_cmap(data)

    if isinstance(cmap, str):
        cmap_cbar = cmap
        cmap = bvcm.double_cmap(cmap)
    else:
        cmap_cbar = cmap

    if isinstance(ax, type(None)) or isinstance(fig, type(None)):
        fig, ax = plt.subplots(figsize=figsize)
    # ax = fig.add_subplot(111)
    # ax.patch.set_alpha(alpha)

    display = plotting.plot_glass_brain(
        img,
        plot_abs=False,
        axes=ax,
        display_mode=display_mode,
        cmap=cmap,
        **kwargs,
    )

    if colorbar is True:
        bvcbar.add_colorbar(
            np.unique(data), fig, unit=unit, cmap=cmap_cbar, borderpad=-2
        )

    fig.patch.set_alpha(alpha)

    if not isinstance(title, type(None)):
        fig.suptitle(title, ha="center", y=1.1)

    if not isinstance(contours, type(None)):
        display.add_contours(contours, colors="#4dbbd5")
    plt.close(fig)
    return fig


def formatted_stat_map(
    img, title, unit="R", cmap=None, title_pad=1.1, colorbar=True, **kwargs
):
    """Plots formatted version of the :func:`nilearn.plotting.plot_stat_map`

    :param img: _description_
    :type img: _type_
    :param title: _description_
    :type title: _type_
    :param unit: _description_, defaults to 'R'
    :type unit: str, optional
    :param cmap: _description_, defaults to None
    :type cmap: _type_, optional
    :param title_pad: _description_, defaults to 1.1
    :type title_pad: float, optional
    :return: _description_
    :rtype: _type_
    """
    data = img.get_fdata()

    if isinstance(cmap, type(None)):
        cmap = "hot_r"

    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(111)
    plt.axis("off")

    display = plotting.plot_stat_map(
        img,
        # bg_img=constants.mask_mni152,
        black_bg=False,
        figure=fig,
        cmap=cmap,
        colorbar=False,
        draw_cross=False,
        **kwargs,
    )

    if colorbar is True:
        bvcbar.add_colorbar(
            data, fig, unit=unit, cmap=cmap, orientation="vertical", borderpad=-2
        )

    if title:
        fig.suptitle(title, ha="center", va="top", y=title_pad)

    fig.patch.set_alpha(0)  # Transparent background.

    return display
