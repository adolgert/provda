"""
These are rules about how to build IHME paths.

A path has:
1) A base disk location for all data. /ihme, or J:/ihme.
2) A team location, such as /forecasting.
3) A role for a dataset, such as sev_data, or sev_forecasts.
4) A date an description, as YYYMMDD_whatever.
5) Subdirectories for results.
"""
import os
import logging
import re


logger = logging.getLogger("provda.ihmepath")


def build_path(host_type, team, role, date, description,
               subdirectory=None, filename=None):
    directory_stack = list()
    if host_type == "cluster":
        directory_stack.append("ihme")
    elif host_type == "windows":
        directory_stack.append("J:")
    else:
        logger.exception("Expect a host type of cluster or windows.")

    directory_stack.append(team)
    directory_stack.append(role)
    normalized = "".join(re.findall("[a-zA-Z0-9\.\-\_]",
                                    description.replace(" ", "_")))
    directory_stack.append("{}_{}".format(date, normalized))
    if subdirectory is not None:
        directory_stack.append(subdirectory)
    if filename is not None:
        directory_stack.append(filename)
    return os.path.join(*directory_stack)
