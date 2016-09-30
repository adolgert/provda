import provda

param = provda.get_parameters("minipackage.down.examplemod", {
    "down_cause_in": provda.path_template(
        "workdir/cod{acause}_{date}_{sex_id}.csv", "r"),
    })

def params():
    return [str(param["down_cause_in"]), param["demog"], param["filetypes"]]
