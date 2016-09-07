import provda

param = provda.get_parameters("provda.tests.sample", {
    "cod_in": provda.path_template(
        "workdir/cod{acause}_{date}_{sex_id}.csv", "r"),
    "risks_in": provda.path_template(
        "workdir/risks{acause}_{risk}_{date}_{sex_id}.hdf5", "r"),
    "cod_out": provda.path_template(
        "workdir/results{acause}_{date}_{sex_id}.hdf5", "w"),
    "use_x" : provda.bool(True),
    "acause" : provda.cause(None),
    "sex_id" : provda.sex(None),
    "date" : provda.string(None),
    "loglevel": provda.string("DEBUG", tracked=False),
    "memlimit": provda.int(20, tracked=False),
    "list_of_stuff" : ["one", "two", "three"]
    })

