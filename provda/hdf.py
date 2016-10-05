import logging
import h5py


logger = logging.getLogger("provda.hdf")


def add_keys(filename, keys):
    f = h5py.File(filename)
    g = f.create_group("/created")
    for k, v in keys.items():
        g.attrs[k] = str(v)
