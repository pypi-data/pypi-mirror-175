import os

import numpy as np
from brainvistools import constants, surface
from mayavi import mlab
from surfer import Brain

mlab.options.offscreen = True


def normalize_ts(ts):
    ts_norm = (ts - ts.mean()) / ts.std()
    return ts_norm


annot_path_lh = os.path.join(constants.DATA_DIR, "lh.HCP-MMP1.annot")
annot_path_rh = os.path.join(constants.DATA_DIR, "rh.HCP-MMP1.annot")


def anmiate_fsaverage_ts(df, annot_path=None, hemi="lh", tstart=0, tend=20, tdil=0.5):

    times = list()
    vtx_ts = np.ndarray((163842, len(df)))
    ind = 0

    for t, r in df.iterrows():
        times.append(float(t * 16))

        vtx_data = surface.parc2fsaverage(r, annot_path=annot_path, hemi=hemi)

        vtx_ts[:, ind] = vtx_data
        ind += 1

    absmax = np.nanmax(
        [abs(np.nanmin(vtx_ts[:, :tend])), abs(np.nanmax(vtx_ts[:, :tend]))]
    )

    # %%

    brain = Brain("fsaverage", "lh", "pial", background="white")

    # %%
    brain.add_data(
        vtx_ts[:, tstart:tend],
        colormap="seismic",
        hemi="lh",
        min=-absmax,
        max=absmax,
        smoothing_steps=10,
        time=times[:tend],
        time_label=lambda t: "%s ms" % int(round(t * 1e3)),
    )

    if not fout.endswith(".mov"):
        fout = fout + ".mov"

    # brain.hide_colorbar(row=1)
    brain.save_movie(fout, time_dilation=tdil)
    brain.close()

    mlab.close(all=True)
