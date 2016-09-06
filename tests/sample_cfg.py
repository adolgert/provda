import provda

param = provda.get_parameters("provda.tests.sample", {
  "cod_in": provda.path_template("workdir/cod{acause}_{date}_{sex_id}.csv", "r"),
  "risks_in": provda.path_template("workdir/risks{acause}_{date}_{sex_id}.hdf5", "r"),
  "cod_out": provda.path_template("workdir/results{acause}_{date}_{sex_id}.hdf5", "w"),
  "acause" : provda.cause("heart attack"),
  "risk" : provda.risk("smoking"),
  "sex_id" : provda.sex(2),
  "date" : provda.string("2016_03_07"),
  "untracked" : {
    "loglevel": provda.string("DEBUG"),
    "memlimit": provda.int(20)
    }
  })

