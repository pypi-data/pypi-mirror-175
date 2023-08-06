import os
from os.path import join

import hcp_utils as hcp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from mayavi import mlab
from nibabel.freesurfer.io import read_annot
from surfer import Brain
from tvtk.api import tvtk
from tvtk.common import configure_input_data

from brainvistools import constants

mlab.options.offscreen = True

fsaverage_label_path = (
    "/Users/leonmartin_bih/work_data/pythontools/brainvistools/fsaverage/label"
)


annot_path_mmp1_lh = os.path.join(constants.DATA_DIR, "lh.HCP-MMP1.annot")
annot_path_mmp1_rh = os.path.join(constants.DATA_DIR, "rh.HCP-MMP1.annot")

annot_path_aparc_lh = join(fsaverage_label_path, "lh.aparc.annot")
annot_path_aparc_rh = join(fsaverage_label_path, "rh.aparc.annot")


def parc2fsaverage(parc_data, hemi="lh", annot_path=None):
    """Upsample parcellated data to fsaverage mesh.

    :param parc_data: key-value pairs of area-labels and data.
    :type parc_data: pandas.Series, dict
    :param hemi: 'hemisphere'
    :type hemi: str
    :param annot_path: path to annot-file
    :type annot_path: str
    :return: vertex data
    :rtype: numpy.ndarray
    """

    if isinstance(annot_path, type(None)):
        annot_path = annot_path_aparc_lh

    annot, _, names = read_annot(annot_path)

    if "MMP1" in annot_path:
        names = [n.decode("utf-8").replace("_ROI", "").lower() for n in names]
    else:
        names = ["ctx-" + hemi + "-" + n.decode("utf-8") for n in names]

    df_annot = (
        pd.DataFrame(names, columns=["area_name"])
        .reset_index()
        .rename({"index": "area_index"}, axis=1)
    )
    df_annot.loc[0, "area_index"] = -1

    vtx_data = np.zeros(annot.shape)

    for k, v in parc_data.items():
        if k in df_annot.area_name.to_list():
            l = df_annot.loc[df_annot.area_name == k]
            df_annot.at[l.index.item(), "value"] = v
            vtx_data = np.where(annot == l.area_index.item(), v, vtx_data)

    return vtx_data


def plot_fsaverage(vtx_data, views=["lat"], hemi="lh", surf="inflated", cmap="seismic"):
    mlab.options.offscreen = True

    subject_id = "fsaverage"

    brain = Brain(subject_id, hemi, surf, background="white", views=views)
    brain.add_data(vtx_data, colormap=cmap)
    brain.hide_colorbar()

    imgmap = brain.screenshot("rgba")
    brain.close()

    fig, axes = plt.subplots()
    axes.imshow(imgmap)
    axes.axis("off")
    plt.close()

    return fig


## %


def norm(x):
    """Normalise array betweeen 0-1

    :param x: _description_
    :type x: _type_
    :return: _description_
    :rtype: _type_
    """
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def _render_surf(
    dscalars,
    hemi="lh",
    surface="inflated",
    cmap=None,
    view="lateral",
    figsize=(1024, 1024),
    alpha=0.9,
    alpha_sulc=1,
    bgcolor=(1, 1, 1),
):
    """Renders HCP template surface mesh.

    :param data: _description_
    :type data: _type_
    :param hemi: _description_, defaults to 'lh'
    :type hemi: str, optional
    :param surface: _description_, defaults to 'inflated'
    :type surface: str, optional
    :param cmap: _description_, defaults to None
    :type cmap: _type_, optional
    :param view: _description_, defaults to 'lateral'
    :type view: str, optional
    :param title: _description_, defaults to 'Random data'
    :type title: str, optional
    :param alpha: _description_, defaults to 0.9
    :type alpha: float, optional
    :param alpha_sulc: _description_, defaults to 1
    :type alpha_sulc: int, optional
    :param bgcolor: _description_, defaults to (1,1,1)
    :type bgcolor: tuple, optional
    :return: _description_
    :rtype: _type_
    """
    mlab.clf()

    azimuth = 0

    if hemi in ["lh", "left"]:
        surf = hcp.mesh[surface + "_left"]
        dscalars_sulc = hcp.mesh["sulc_left"]
        dscalars_ctx = hcp.left_cortex_data(dscalars)

        if view == "lateral":
            azimuth += 180

    elif hemi in ["rh", "right"]:
        surf = hcp.mesh[surface + "_right"]
        dscalars_sulc = hcp.mesh["sulc_right"]
        dscalars_ctx = hcp.right_cortex_data(dscalars)

        if view == "medial":
            azimuth += 180

    else:
        surf = hcp.mesh[surface]
        dscalars_sulc = hcp.mesh["sulc"]
        dscalars_ctx = hcp.cortex_data(dscalars)

    fig = mlab.figure(size=figsize, bgcolor=bgcolor)

    # Get coordinates and vertices.
    x = surf[0][:, 0]
    y = surf[0][:, 1]
    z = surf[0][:, 2]
    tris = surf[1]

    # generate an rgba matrix, of shape n_vertices x 4
    if not cmap:
        cmap = cm.get_cmap("hot_r")
    elif isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)

    hue = norm(dscalars_ctx)
    colors = cmap(hue)[:, :3]
    alpha = np.full(z.shape, alpha)
    alpha = np.where(dscalars_ctx == 0, 0, alpha)
    rgba_vals = np.concatenate((colors, alpha[:, None]), axis=1)

    cmap_sulc = plt.get_cmap("Greys")
    hue_sulc = norm(dscalars_sulc)
    colors_sulc = cmap_sulc(hue_sulc)[:, :3]
    alpha_sulc = np.full(z.shape, alpha_sulc)

    # Mix with sulcal depth image by means of alpha compositing
    srcRGB = colors
    dstRGB = colors_sulc

    srcA = alpha
    dstA = alpha_sulc

    # Work out resultant alpha channel
    outA = srcA + dstA * (1 - srcA)

    # Work out resultant RGB
    outRGB = (
        srcRGB * srcA[..., np.newaxis]
        + dstRGB * dstA[..., np.newaxis] * (1 - srcA[..., np.newaxis])
    ) / outA[..., np.newaxis]
    rgba_vals = np.concatenate((outRGB, outA[:, None]), axis=1)

    mesh = mlab.pipeline.triangular_mesh_source(x, y, z, tris, figure=fig)

    mesh.data.point_data.scalars.number_of_components = 4  # r, g, b, a
    mesh.data.point_data.scalars = (rgba_vals * 255).astype("ubyte")

    # tvtk for vis
    mapper = tvtk.PolyDataMapper()
    configure_input_data(mapper, mesh.data)
    actor = tvtk.Actor()
    actor.mapper = mapper
    fig.scene.add_actor(actor)

    cam, foc = mlab.move()
    # Define View
    if view.lower() in ["lateral"]:
        elevation = 90

    elif view.lower() in ["medial"]:
        elevation = 90

    elif view.lower() in ["dorsal", "superior"]:
        elevation = 0

    elif view.lower() in ["ventral", "iferior"]:
        elevation = 180

    mlab.view(
        azimuth=azimuth,
        elevation=elevation,
        distance=None,
        focalpoint="auto",
        roll=None,
        reset_roll=True,
    )

    return fig


def render_surf_mpl(data, **kwargs):
    """_summary_

    :param data: _description_
    :type data: _type_
    :return: _description_
    :rtype: _type_
    """
    if len(data) == 379:
        dscalars = hcp.unparcellate(data, hcp.mmp)
    else:
        dscalars = data

    mlab_fig = _render_surf(dscalars, **kwargs)
    imgmap = mlab.screenshot(figure=mlab_fig, mode="rgba", antialiased=True)
    mlab.close(mlab_fig)
    return imgmap


def add_cbar(data, fig, ax, cmap="viridis", unit="", font_kwargs={}):
    vmin = data.min()
    vmax = data.max()

    cbar = fig.colorbar(
        cm.ScalarMappable(norm=plt.Normalize(vmin, vmax), cmap=cmap),
        ax=ax,
        ticks=[vmin, vmax],
        fraction=0.025,
    )
    cbar.outline.set_visible(False)
    cbar.ax.set_yticklabels([np.round(vmin, 2), np.round(vmax, 2)], **font_kwargs)
    cbar.set_label(unit, rotation=0)


def plot_fsLR(
    vtx_data,
    title="",
    unit="1",
    cmap="inferno",
    figsize=None,
    font_kwargs={"fontname": "Arial", "fontsize": 12},
    **kwargs
):
    imgmap = render_surf_mpl(vtx_data, view="lateral", cmap=cmap, **kwargs)
    imgmap_med = render_surf_mpl(vtx_data, view="medial", cmap=cmap, **kwargs)

    fig, axes = plt.subplots(
        ncols=2, figsize=figsize, gridspec_kw={"width_ratios": (1, 1)}
    )
    axes[0].imshow(imgmap)
    axes[1].imshow(imgmap_med)

    for ax in fig.axes:
        ax.axis("off")

    vmin = vtx_data.min()
    vmax = vtx_data.max()

    cbar = fig.colorbar(
        cm.ScalarMappable(norm=plt.Normalize(vmin, vmax), cmap=cmap),
        ax=axes[1],
        ticks=[vmin, vmax],
        fraction=0.025,
    )
    cbar.outline.set_visible(False)
    cbar.ax.set_yticklabels([np.round(vmin, 2), np.round(vmax, 2)], **font_kwargs)
    cbar.set_label(unit, rotation=0)
    fig.tight_layout()

    box = axes[1].get_position()
    box.x0 = box.x0 - 0.01
    box.x1 = box.x1 - 0.01
    axes[1].set_position(box)

    # box = cbar.get_position()
    # box.x0 = box.x0 - 0.01
    # box.x1 = box.x1 - 0.01
    # cbar.set_position(box)

    fig.suptitle(title, y=0.85, **font_kwargs)
    plt.close()

    return fig


def plot_hcp(
    data, title="TVBase map", view="lateral", unit="R", cbar=True, cmap=None, **kwargs
):
    """Surface Plot on HCP template.

    :param data: _description_
    :type data: _type_
    :param title: _description_, defaults to 'TVBase map'
    :type title: str, optional
    :param view: _description_, defaults to 'lateral'
    :type view: str, optional
    :param unit: _description_, defaults to 'R'
    :type unit: str, optional
    :param cbar: _description_, defaults to True
    :type cbar: bool, optional
    :param cmap: _description_, defaults to None
    :type cmap: _type_, optional
    :return: _description_
    :rtype: _type_
    """
    mlab.close(all=True)
    mlab.clf()

    if len(data) == 379:
        dscalars = hcp.unparcellate(data, hcp.mmp)
    else:
        dscalars = data

    if view in ["lateralmedial", "both"]:
        fig = _render_surf(dscalars, view="lateral", cmap=cmap, **kwargs)
        imgmap = mlab.screenshot(figure=fig, mode="rgba", antialiased=True)

        fig_med = _render_surf(dscalars, view="medial", cmap=cmap, **kwargs)
        imgmap_med = mlab.screenshot(figure=fig_med, mode="rgba", antialiased=True)

        grid = 121
        txt_height = 0.7
        fig_width = 8
    else:
        fig = _render_surf(dscalars, view=view, cmap=cmap, **kwargs)
        imgmap = mlab.screenshot(figure=fig, mode="rgba", antialiased=True)

        grid = 111
        txt_height = 0.9
        fig_width = 4
    # fig = _render_surf(data, view='lateral', **kwargs)

    # Create Matplotlib render

    fig2 = plt.figure(figsize=(fig_width, 3), facecolor="white")
    plt.rcParams.update({"font.size": 12})

    ax = fig2.add_subplot(grid)
    ax.imshow(imgmap, zorder=4)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.axis("off")
    # Title inside Frame

    if view in ["lateralmedial", "both"]:
        ax_med = fig2.add_subplot(grid + 1)
        ax_med.imshow(imgmap_med, zorder=4)
        ax_med.axes.get_xaxis().set_visible(False)
        ax_med.axes.get_yaxis().set_visible(False)
        ax_med.axis("off")

    fig2.tight_layout()
    if cbar:
        # divider = make_axes_locatable(ax)
        # cax = divider.append_axes("bottom", size="4%", pad=-0.1)

        # formatted_colorbar(data, ax=cax, cmap=cmap, orientation='horizontal')

        #
        # cax.set_title('R')

        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        cax = inset_axes(
            fig2.axes[len(fig2.axes) - 1],
            width="30%",  # width = 30% of parent_bbox
            height="5%",  # height : 1 inch
            loc=4,
        )
        fig.colorbar(
            cm.ScalarMappable(norm=plt.Normalize(data.min(), data.max()), cmap=cmap),
            ax=cax,
            ticks=[data.min(), data.max()],
            fraction=0.025,
        )

        # plot.formatted_colorbar(data, ax=cax, cmap=cmap, orientation="horizontal")
        cax.set_title(unit, size=12)

    # fig2.suptitle('test', size=15);

    fig2.subplots_adjust(
        left=None, bottom=None, right=None, top=None, wspace=-0.5, hspace=-1
    )

    fig2.text(
        0.5,
        0.9,
        title,
        bbox={"facecolor": "white", "alpha": 1, "edgecolor": "none"},
        ha="center",
        va="center",
        size=13,
    )

    plt.close()
    return fig2
