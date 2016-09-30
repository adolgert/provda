import provda

param = provda.get_parameters("minipackage.sub.examplemod", {
    "sub_out": provda.path_template(
        "workdir/cod{acause}_{date}_{sex_id}.csv", "r"),
    })

def params():
    return [str(param["sub_out"]), param["demog"]]
