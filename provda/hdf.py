import logging
import h5py


logger = logging.getLogger("provda.hdf")


def add_keys(filename, keys, group=None):
    """
    This adds key-value pairs to an HDF file. It puts them all
    into attributes on a group called "/created".

    :param filename str: The filename as a string
    :param keys: A dictionary of key-value pairs to add to the file.
    :param group: If you want to name the group something else, name it here.
    :return:
    """
    f = h5py.File(filename)
    if group is not None:
        g = f.create_group(group)
    else:
        g = f.create_group("/created")
    for k, v in keys.items():
        g.attrs[k] = str(v)
