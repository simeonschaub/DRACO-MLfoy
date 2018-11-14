# global imports
import numpy as np
import os
import sys


# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

import DRACO_Frameworks.DNN_Aachen.DNN_Aachen as DNN_Aachen
import DRACO_Frameworks.DNN_Aachen.variable_info as variable_info

categories_dic = {
    "(N_Jets == 4 and N_BTagsM >= 3)": [variable_info.variables_4j_3b, "4j_ge3t"],
    "(N_Jets == 5 and N_BTagsM >= 3)": [variable_info.variables_5j_3b, "5j_ge3t"],
    "(N_Jets == 6 and N_BTagsM >= 3)": [variable_info.variables_6j_3b, "5j_ge3t"]}

prenet_targets = [
    #"GenAdd_BB_inacceptance",
    "GenAdd_B_inacceptance",
    "GenHiggs_BB_inacceptance",
    #"GenHiggs_B_inacceptance",
    #"GenTopHad_B_inacceptance",
    "GenTopHad_QQ_inacceptance",
    "GenTopHad_Q_inacceptance",
    #"GenTopLep_B_inacceptance"
    ]

event_classes = ["ttHbb", "ttbb", "tt2b", "ttb", "ttcc", "ttlf"]

inPath = "/storage/c/vanderlinden/DRACO-MLfoy/workdir/aachen_data/"

for key in categories_dic:
    outpath = "/storage/c/vanderlinden/DRACO-MLfoy/workdir/aachen_eval_"+str(categories_dic[key][1])+"/"


    dnn_aachen = DNN_Aachen.DNN(
        in_path             = inPath, 
        save_path           = outpath,		
        event_classes       = event_classes, 
        event_category      = key,
        train_variables     = categories_dic[key][0], 
        prenet_targets      = prenet_targets,
        train_epochs        = 500,
        early_stopping      = 50,
        eval_metrics        = ["acc", "mean_squared_error"])


    dnn_aachen.build_model()
    dnn_aachen.train_models()
    dnn_aachen.eval_model()
    dnn_aachen.plot_metrics()
    dnn_aachen.plot_prenet_nodes()
    dnn_aachen.plot_classification_nodes()
