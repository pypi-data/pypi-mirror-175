import pandas as pd
from os.path import join
from brainvistools import constants


def fs_mapper(index_as_key=True):
    """_summary_

    :param index_as_key: _description_, defaults to True
    :type index_as_key: bool, optional
    :return: _description_
    :rtype: _type_
    """
    filename = join(constants.DATA_DIR, "FreeSurferColorLUT.txt")
    lut = pd.read_csv(
        filename, comment="#", sep="\s+", names=["id", "name", "r", "g", "b", "a"]
    )

    lut = pd.DataFrame(lut)
    lut.name = lut.name.str.lower()

    # FS index-name mapper
    mapper = dict()

    # Create index-name pairs.
    for i, r in lut.iterrows():
        if index_as_key:
            mapper[r.id] = r["name"]
        else:
            mapper[r["name"]] = r.id

    return mapper
