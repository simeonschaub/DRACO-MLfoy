# global imports
import numpy as np
import os
import sys
import socket
import matplotlib.pyplot as plt
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

import DRACO_Frameworks.DNN_Aachen.DNN_Aachen as DNN_Aachen
import DRACO_Frameworks.DNN_Aachen.variable_info as variable_info
import DRACO_Frameworks.DNN_Aachen.data_frame as data_frame

category_vars = {
    "4j_ge3t": variable_info.variables_4j_3b,
    "4j_4t": variable_info.variables_4j_3b,
    "5j_ge3t": variable_info.variables_5j_3b,
    "ge6j_ge3t": variable_info.variables_6j_3b}            
categories = {
    "4j_ge3t":   "(N_Jets == 4 and N_BTagsM >= 3)",
    "4j_4t":   "(N_Jets == 4 and N_BTagsM == 4)",
    "5j_ge3t":   "(N_Jets == 5 and N_BTagsM >= 3)",
    "ge6j_ge3t": "(N_Jets >= 6 and N_BTagsM >= 3)",
    }
prenet_targets = [
    #"GenAdd_BB_inacceptance",
    #"GenAdd_B_inacceptance",
    "GenHiggs_BB_inacceptance",
    "GenHiggs_B_inacceptance",
    "GenTopHad_B_inacceptance",
    "GenTopHad_QQ_inacceptance",
    "GenTopHad_Q_inacceptance",
    "GenTopLep_B_inacceptance"
    ]

event_classes = ["ttHbb", "ttbb", "tt2b", "ttb", "ttcc", "ttlf"]

if "naf" in socket.gethostname():
    workpath = "/nfs/dust/cms/user/vdlinden/DRACO-MLfoy/workdir/"
else:
    workpath = "/ceph/vanderlinden/DRACO-MLfoy/workdir/"


inPath = workpath+"/AachenDNN_files"

key = sys.argv[1]

workpath = "/ceph/vanderlinden/DRACO-MLfoy/train_scripts/Aachen_DNN_checkpoints/"
outpath = workpath+"/"+str(key)+"/"
checkpoint_path = outpath + "/checkpoints/trained_main_net.h5py"

dnn_aachen = DNN_Aachen.DNN(
    in_path             = inPath,
    save_path           = outpath,
    event_classes       = event_classes,
    event_category      = categories[key],
    train_variables     = category_vars[key],
    prenet_targets      = prenet_targets,
    train_epochs        = 500,
    early_stopping      = 20,
    eval_metrics        = ["acc"],
    additional_cut      = None)

dnn_aachen.load_trained_model()

data = dnn_aachen.data.get_test_data(as_matrix=False)

prediction_before = dnn_aachen.main_net.predict(data.values)

# apply some uncertainties to data
def func(x):
    return x + np.random.normal(0,0.01)

data_new = data.applymap(func)

prediction_after = dnn_aachen.main_net.predict(data_new.values)
#print( data.head() )
#print(data_new.head())
absolute_differences = []
other_pred = 0
for i in range(len(prediction_before)):
    diff = 0
    for j in range(len(prediction_before[i])):
        diff += np.abs( prediction_before[i][j]-prediction_after[i][j] )
    absolute_differences.append(diff)
    if not np.argmax( prediction_before[i] ) == np.argmax( prediction_after[i] ):
        print("predictions not the same:")
        print(prediction_before[i])
        print(prediction_after[i])
        print("="*40)
        other_pred += 1

print(other_pred)
print(len(prediction_before))
plt.hist(absolute_differences)
plt.show()


