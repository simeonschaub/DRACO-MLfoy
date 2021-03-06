# global imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import tqdm

# option handler
import optionHandler
options = optionHandler.optionHandler(sys.argv)

# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

# import class for DNN training
import DRACO_Frameworks.DNN.DNN as DNN
import DRACO_Frameworks.DNN.BNN as BNN
import DRACO_Frameworks.DNN.data_frame as df

options.initArguments()

# load samples
input_samples = df.InputSamples(options.getInputDirectory(), options.getActivatedSamples(), options.getTestPercentage()) #+"_nominal"

# define all samples
input_samples.addSample(options.getDefaultName("ttH"), label = "ttH", normalization_weight = options.getNomWeight())
input_samples.addSample(options.getDefaultName("ttbb") , label = "ttbb" , normalization_weight = options.getNomWeight())
input_samples.addSample(options.getDefaultName("tt2b") , label = "tt2b" , normalization_weight = options.getNomWeight())
#input_samples.addSample(options.getDefaultName("ttb")  , label = "ttb"  , normalization_weight = options.getNomWeight())
input_samples.addSample(options.getDefaultName("ttcc") , label = "ttcc" , normalization_weight = options.getNomWeight())
input_samples.addSample(options.getDefaultName("ttlf") , label = "ttlf" , normalization_weight = options.getNomWeight())

# # load samples JES up
# input_samples_up = df.InputSamples(options.getInputDirectory()+"_JESup", options.getActivatedSamples(), options.getTestPercentage())

# # define all samples JES up
# input_samples_up.addSample(options.getDefaultName("ttH"), label = "ttH", normalization_weight = options.getNomWeight())
# input_samples_up.addSample(options.getDefaultName("ttbb") , label = "ttbb" , normalization_weight = options.getNomWeight())
# input_samples_up.addSample(options.getDefaultName("tt2b") , label = "tt2b" , normalization_weight = options.getNomWeight())
# #input_samples_up.addSample(options.getDefaultName("ttb")  , label = "ttb"  , normalization_weight = options.getNomWeight())
# input_samples_up.addSample(options.getDefaultName("ttcc") , label = "ttcc" , normalization_weight = options.getNomWeight())
# input_samples_up.addSample(options.getDefaultName("ttlf") , label = "ttlf" , normalization_weight = options.getNomWeight())

# # load samples JES down
# input_samples_down = df.InputSamples(options.getInputDirectory()+"_JESdown", options.getActivatedSamples(), options.getTestPercentage())

# # define all samples JES down
# input_samples_down.addSample(options.getDefaultName("ttH"), label = "ttH", normalization_weight = options.getNomWeight())
# input_samples_down.addSample(options.getDefaultName("ttbb") , label = "ttbb" , normalization_weight = options.getNomWeight())
# input_samples_down.addSample(options.getDefaultName("tt2b") , label = "tt2b" , normalization_weight = options.getNomWeight())
# #input_samples_down.addSample(options.getDefaultName("ttb")  , label = "ttb"  , normalization_weight = options.getNomWeight())
# input_samples_down.addSample(options.getDefaultName("ttcc") , label = "ttcc" , normalization_weight = options.getNomWeight())
# input_samples_down.addSample(options.getDefaultName("ttlf") , label = "ttlf" , normalization_weight = options.getNomWeight())

if options.isBinary():
    input_samples.addBinaryLabel(options.getSignal(), options.getBinaryBkgTarget())
    # input_samples_up.addBinaryLabel(options.getSignal(), options.getBinaryBkgTarget())
    # input_samples_down.addBinaryLabel(options.getSignal(), options.getBinaryBkgTarget())


###### code for NN output comparison ######   

def anns_calc_mean_std(n_NNs, input_dir):
    pred_list = []
    for i in range(n_NNs):
        i+=1
        print "Iteration: {}".format(i)
        preds = dnn.load_trained_model(input_dir + "/ann_{}_ge4j_ge3t".format(i))
        pred_list.append(preds)
    test_preds = np.concatenate(pred_list, axis=1)
    return np.mean(test_preds, axis=1), np.std(test_preds, axis=1)


def plot_correlation_two_NNs(NN_pred1, NN_pred2, NN_pred1_std, NN_pred2_std, x_lab, y_lab, save_dir, save_name):
    from matplotlib.colors import LogNorm
    plt.hist2d(NN_pred1, NN_pred2, bins=[50,50], cmin=1, norm=LogNorm())
    plt.plot([0,1],[0,1],'k')
    plt.colorbar()
    plt.xlabel("$\mu$ "+x_lab, fontsize = 16)
    plt.ylabel("$\mu$ "+y_lab, fontsize = 16)
    plt.savefig(save_dir+"/plots/mu_{}.png".format(save_name))
    print "mu_{}.png was created".format(save_name)
    plt.savefig(save_dir+"/plots/mu_{}.pdf".format(save_name))
    print "mu_{}.pdf was created".format(save_name)
    plt.close()

    n_max = np.amax([np.amax(NN_pred1_std), np.amax(NN_pred2_std)])
    plt.hist2d(NN_pred1_std, NN_pred2_std, bins=[50,50], range=[[0.,n_max],[0.,n_max]], cmin=1, norm=LogNorm())
    plt.plot([0,n_max],[0,n_max],'k')
    plt.colorbar()
    plt.xlabel("$\sigma$ "+x_lab, fontsize = 16)
    plt.ylabel("$\sigma$ "+y_lab, fontsize = 16)
    plt.savefig(save_dir+"/plots/std_{}.png".format(save_name))
    print "std_{}.png was created".format(save_name)
    plt.savefig(save_dir+"/plots/std_{}.pdf".format(save_name))
    print "std_{}.pdf was created".format(save_name)
    plt.close()


# initializing DNN training class
dnn = DNN.DNN(
    save_path       = options.getOutputDir(),
    input_samples   = input_samples,
    category_name   = options.getCategory(),
    train_variables = options.getTrainVariables(),
    # number of epochs
    train_epochs    = options.getTrainEpochs(),
    # metrics for evaluation (c.f. KERAS metrics)
    eval_metrics    = ["acc"],
    # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
    test_percentage = options.getTestPercentage(),
    # balance samples per epoch such that there amount of samples per category is roughly equal
    balanceSamples  = options.doBalanceSamples(),
    shuffle_seed    = 42,
    evenSel         = options.doEvenSelection(),
    norm_variables  = options.doNormVariables())

l2, dout = "7", "40"
out_dir_1 = "/local/scratch/hdd/nshadskiy/ANNs_l2-{}_dout{}".format(l2, dout)
nn1_pred, nn1_pred_std = anns_calc_mean_std(n_NNs=100, input_dir=out_dir_1)

# initializing BNN training class
bnn = BNN.BNN(
    save_path       = options.getOutputDir(),
    input_samples   = input_samples,
    category_name   = options.getCategory(),
    train_variables = options.getTrainVariables(),
    # number of epochs
    train_epochs    = options.getTrainEpochs(),
    # metrics for evaluation (c.f. KERAS metrics)
    eval_metrics    = ["acc"],
    # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
    test_percentage = options.getTestPercentage(),
    # balance samples per epoch such that there amount of samples per category is roughly equal
    balanceSamples  = options.doBalanceSamples(),
    shuffle_seed    = 42,
    evenSel         = options.doEvenSelection(),
    norm_variables  = options.doNormVariables(),
    sys_variation   = False,
    gen_vars        = False)

# # initializing BNN training class
# bnn_up = BNN.BNN(
#     save_path       = options.getOutputDir(),
#     input_samples   = input_samples,  #_up
#     category_name   = options.getCategory(),
#     train_variables = options.getTrainVariables(),
#     # number of epochs
#     train_epochs    = options.getTrainEpochs(),
#     # metrics for evaluation (c.f. KERAS metrics)
#     eval_metrics    = ["acc"],
#     # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
#     test_percentage = options.getTestPercentage(),
#     # balance samples per epoch such that there amount of samples per category is roughly equal
#     balanceSamples  = options.doBalanceSamples(),
#     shuffle_seed    = 42,
#     evenSel         = options.doEvenSelection(),
#     norm_variables  = options.doNormVariables(),
#     sys_variation   = False,
#     gen_vars        = True)

# # initializing BNN training class
# bnn_down = BNN.BNN(
#     save_path       = options.getOutputDir(),
#     input_samples   = input_samples,  #_down
#     category_name   = options.getCategory(),
#     train_variables = options.getTrainVariables(),
#     # number of epochs
#     train_epochs    = options.getTrainEpochs(),
#     # metrics for evaluation (c.f. KERAS metrics)
#     eval_metrics    = ["acc"],
#     # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
#     test_percentage = options.getTestPercentage(),
#     # balance samples per epoch such that there amount of samples per category is roughly equal
#     balanceSamples  = options.doBalanceSamples(),
#     shuffle_seed    = 42,
#     evenSel         = options.doEvenSelection(),
#     norm_variables  = options.doNormVariables(),
#     sys_variation   = False,
#     gen_vars        = True)

# bnn_prior_1 = "1_genCSV"
# out_dir_1 = "/home/nshadskiy/Documents/draco-bnns/workdir/bnn_prior_{}_ge4j_ge3t".format(bnn_prior_1)
bnn_prior_2 = "1_nomCSV"
out_dir_2 = "/home/nshadskiy/Documents/draco-bnns/workdir/bnn_prior_{}_ge4j_ge3t".format(bnn_prior_2)
# bnn_prior_3 = "1_mixCSV"
# out_dir_3 = "/home/nshadskiy/Documents/draco-bnns/workdir/bnn50_prior_{}_ge4j_ge3t".format(bnn_prior_3)

nn2_pred, nn2_pred_std, labels2 = bnn.load_trained_model(out_dir_2)
# bin_range = options.getBinaryBinRange()
# #bin_range = [-1., 1.5]
# bnn.plot_binaryOutput(
#     log         = options.doLogPlots(),
#     privateWork = options.isPrivateWork(),
#     printROC    = options.doPrintROC(),
#     nbins       = 15,
#     bin_range   = bin_range,
#     name        = options.getName(),
#     sigScale    = options.getSignalScale())

# nn1_up_pred, nn1_up_pred_std, labels1_up = bnn_up.load_trained_model(out_dir_2)

# nn1_down_pred, nn1_down_pred_std, labels1_down = bnn_down.load_trained_model(out_dir_3)

# bnn_prior_2 = "0p1"
# out_dir_2 = "/home/nshadskiy/Documents/draco-bnns/workdir/bnn_prior_{}_ge4j_ge3t".format(bnn_prior_2)
# nn2_pred, nn2_pred_std, labels2 = bnn.load_trained_model(out_dir_2)


nn2_sig_pred, nn2_sig_pred_std, nn1_sig_pred, nn1_sig_pred_std, nn2_bkg_pred, nn2_bkg_pred_std, nn1_bkg_pred, nn1_bkg_pred_std = [],[],[],[],[],[],[],[]
for i in range(len(labels2)):
    if labels2[i]==1:
        nn1_sig_pred.append(nn1_pred[i])
        nn1_sig_pred_std.append(nn1_pred_std[i])
        nn2_sig_pred.append(nn2_pred[i])
        nn2_sig_pred_std.append(nn2_pred_std[i])
    elif labels2[i]==0:
        nn1_bkg_pred.append(nn1_pred[i])
        nn1_bkg_pred_std.append(nn1_pred_std[i])
        nn2_bkg_pred.append(nn2_pred[i])
        nn2_bkg_pred_std.append(nn2_pred_std[i])
    else:
        print "--wrong event--"


# plot_correlation_two_NNs(nn1_pred, nn2_pred, nn1_pred_std, nn2_pred_std, "BNN 1", "BNN 2", out_dir_2, "bnn1_bnn2_prior_{}_{}".format(bnn_prior_1, bnn_prior_2))
# plot_correlation_two_NNs(nn1_sig_pred, nn2_sig_pred, nn1_sig_pred_std, nn2_sig_pred_std, "BNN 1 signal", "BNN 2 signal", out_dir_2, "sig_bnn1_bnn2_prior_{}_{}".format(bnn_prior_1, bnn_prior_2))
# plot_correlation_two_NNs(nn1_bkg_pred, nn2_bkg_pred, nn1_bkg_pred_std, nn2_bkg_pred_std, "BNN 1 background", "BNN 2 background", out_dir_2, "bkg_bnn1_bnn2_prior_{}_{}".format(bnn_prior_1, bnn_prior_2))

plot_correlation_two_NNs(nn1_pred, nn2_pred, nn1_pred_std, nn2_pred_std, "ANNs", "BNN", out_dir_2, "anns_bnn_l2_{}_prior_{}".format(l2, bnn_prior_2))
plot_correlation_two_NNs(nn1_sig_pred, nn2_sig_pred, nn1_sig_pred_std, nn2_sig_pred_std, "ANNs signal", "BNN signal", out_dir_2, "sig_anns_bnn_l2_{}_prior_{}".format(l2, bnn_prior_2))
plot_correlation_two_NNs(nn1_bkg_pred, nn2_bkg_pred, nn1_bkg_pred_std, nn2_bkg_pred_std, "ANNs background", "BNN background", out_dir_2, "bkg_anns_bnn_l2_{}_prior_{}".format(l2, bnn_prior_2))


###### code for evaluation of systematic uncertainties ######

# make plots of the output distribution for one single event
def plot_event_distribution(save_dir, n_events=20000):
    #if len(preds) < n_events: return "not enouth events to draw outout distribution"
    for i in range(n_events):
        evt_id = bnn_down.data.get_test_data(as_matrix = False).index[i]
        #print evt_id
        if evt_id in bnn_up.data.get_test_data(as_matrix = False).index:
            j = bnn_up.data.get_test_data(as_matrix = False).index.get_loc(evt_id)
            #print "up"
            if evt_id in bnn.data.get_test_data(as_matrix = False).index:
                #print "nominal"
                print evt_id
                k = bnn.data.get_test_data(as_matrix = False).index.get_loc(evt_id)
                x = np.linspace(nn1_pred[k] - 4*nn1_pred_std[k], nn1_pred[k] + 4*nn1_pred_std[k], 200)
                x_up = np.linspace(nn1_up_pred[j] - 4*nn1_up_pred_std[j], nn1_up_pred[j] + 4*nn1_up_pred_std[j], 200)
                x_down = np.linspace(nn1_down_pred[i] - 4*nn1_down_pred_std[i], nn1_down_pred[i] + 4*nn1_down_pred_std[i], 200)
                plt.plot(x, stats.norm.pdf(x, nn1_pred[k], nn1_pred_std[k]), color="b", label="nominal $\mu$={0:.3f}$\pm${1:.3f}".format(nn1_pred[k], nn1_pred_std[k]))
                plt.plot(x_up, stats.norm.pdf(x_up, nn1_up_pred[j], nn1_up_pred_std[j]), color="r", label="up $\mu$={0:.3f}$\pm${1:.3f}".format(nn1_up_pred[j], nn1_up_pred_std[j]))
                plt.plot(x_down, stats.norm.pdf(x_down, nn1_down_pred[i], nn1_down_pred_std[i]), color="g", label="down $\mu$={0:.3f}$\pm${1:.3f}".format(nn1_down_pred[i], nn1_down_pred_std[i]))
                plt.xlabel("$\mu$ of event", fontsize = 16)
                #plt.ylabel("number of samples", fontsize = 16)
                if labels1[k]==1:
                    plt.title("signal event", fontsize = 16)
                else:
                    plt.title("background event", fontsize = 16)
                plt.legend()
                plt.savefig(save_dir+"/events/event_{}_{}_{}_dists.pdf".format(evt_id[0], evt_id[1], evt_id[2]))
                plt.savefig(save_dir+"/events/event_{}_{}_{}_dists.png".format(evt_id[0], evt_id[1], evt_id[2]))
                print "/events/event_{}_{}_{}_dists.pdf".format(evt_id[0], evt_id[1], evt_id[2])+" saved"
                plt.close()
                event_path = save_dir + "/events/event_{}_{}_{}_vars.csv".format(evt_id[0], evt_id[1], evt_id[2])
                with open(event_path, "w") as f:
                    f.write("variable,value,value JES up,value JES down\n")
                    used_vars = bnn.train_variables + ["N_Jets", "N_BTagsM"]
                    for v in used_vars:
                        f.write("{},{},{},{}\n".format(v, bnn.data.get_all_test_data(unnormed=True).loc[evt_id,v], bnn_up.data.get_all_test_data(unnormed=True).loc[evt_id,v], bnn_down.data.get_all_test_data(unnormed=True).loc[evt_id,v]))
                    print "/events/event_{}_{}_{}_vars.csv".format(evt_id[0], evt_id[1], evt_id[2])+" saved"

def plot_3_diff_hist(save_dir):
    sig_preds, sig_preds_up, sig_preds_down, bkg_preds, bkg_preds_up, bkg_preds_down = [], [], [], [], [], []
    df_test = bnn.data.get_test_data(as_matrix = False)
    df_test_up = bnn_up.data.get_test_data(as_matrix = False)
    df_test_down = bnn_down.data.get_test_data(as_matrix = False)
    #print df_test, df_test_up, df_test_down
    for i in tqdm.tqdm(range(len(labels1_down))):
        evt_id = df_test_down.index[i]
        #evt_id = tuple(map(float,evt_id))
        if evt_id in df_test_up.index:
            j = df_test_up.index.get_loc(evt_id)
            if evt_id in df_test.index:
                k = df_test.index.get_loc(evt_id)
                #print evt_id
                if labels1[k]==1:
                    sig_preds.append(nn1_pred[k])
                    sig_preds_up.append(nn1_up_pred[j])
                    sig_preds_down.append(nn1_down_pred[i])
                elif labels1[k]==0:
                    bkg_preds.append(nn1_pred[k])
                    bkg_preds_up.append(nn1_up_pred[j])
                    bkg_preds_down.append(nn1_down_pred[i])

    plt.hist(sig_preds, bins=15, range=(0,1), histtype='step', density=True, label="ttH", color="b")
    plt.hist(sig_preds_up, bins=15, range=(0,1), histtype='step', density=True, linestyle=('--'), color="b")
    plt.hist(sig_preds_down, bins=15, range=(0,1), histtype='step', density=True, linestyle=(':'), color="b")
    plt.hist(bkg_preds, bins=15, range=(0,1), histtype='step', density=True, label="bkg", color="r")
    plt.hist(bkg_preds_up, bins=15, range=(0,1), histtype='step', density=True, linestyle=('--'), color="r")
    plt.hist(bkg_preds_down, bins=15, range=(0,1), histtype='step', density=True, linestyle=(':'), color="r")
    plt.xlabel("$\mu$", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/discr_diff_bnns.png") #samples
    print "discr_diff_samples.png was created"
    plt.savefig(save_dir+"/plots/discr_diff_bnns.pdf") #samples
    print "discr_diff_samples.pdf was created"
    plt.close()

def plot_mixing_diff_hist(save_dir):
    sig_preds, sig_preds_up, bkg_preds, bkg_preds_up = [], [], [], []
    df_test = bnn.data.get_test_data(as_matrix = False)
    df_test_up = bnn_up.data.get_test_data(as_matrix = False)
    for i in tqdm.tqdm(range(len(labels1_up))):
        evt_id = df_test_up.index[i]
        if evt_id in df_test.index:
            j = df_test.index.get_loc(evt_id)
            if labels1[j]==1:
                sig_preds.append(nn1_pred[j])
                sig_preds_up.append(nn1_up_pred[i])
            elif labels1[j]==0:
                bkg_preds.append(nn1_pred[j])
                bkg_preds_up.append(nn1_up_pred[i])
    print "matching events (sig/bkg): ", len(sig_preds), len(bkg_preds)
    plt.hist(sig_preds, bins=15, range=(0,1), histtype='step', density=True, label="ttH", color="b")
    plt.hist(sig_preds_up, bins=15, range=(0,1), histtype='step', density=True, linestyle=('--'), color="b")
    plt.hist(bkg_preds, bins=15, range=(0,1), histtype='step', density=True, label="bkg", color="r")
    plt.hist(bkg_preds_up, bins=15, range=(0,1), histtype='step', density=True, linestyle=('--'), color="r")
    plt.xlabel("$\mu$", fontsize = 16)
    plt.ylabel("normed", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/JES_mixed_varied_discrX.png")
    print "JES_mixed_varied_discr.png was created"
    plt.savefig(save_dir+"/plots/JES_mixed_varied_discrX.pdf")
    print "JES_mixed_varied_discr.pdf was created"
    plt.close()

def plot_2_uncert_diff(save_dir):
    sig_preds_std, sig_preds_std_up, sig_preds_std_down, bkg_preds_std, bkg_preds_std_up, bkg_preds_std_down = [], [], [], [], [], []
    df_test = bnn.data.get_test_data(as_matrix = False)
    df_test_up = bnn_up.data.get_test_data(as_matrix = False)
    df_test_down = bnn_down.data.get_test_data(as_matrix = False)
    for i in tqdm.tqdm(range(len(labels1_down))):
        evt_id = df_test_down.index[i]
        if evt_id in df_test_up.index:
            j = df_test_up.index.get_loc(evt_id)
            if evt_id in df_test.index:
                k = df_test.index.get_loc(evt_id)
                #print evt_id
                if labels1[k]==1:
                    sig_preds_std.append(nn1_pred_std[k])
                    sig_preds_std_up.append(nn1_up_pred_std[j])
                    sig_preds_std_down.append(nn1_down_pred_std[i])
                elif labels1[k]==0:
                    bkg_preds_std.append(nn1_pred_std[k])
                    bkg_preds_std_up.append(nn1_up_pred_std[j])
                    bkg_preds_std_down.append(nn1_down_pred_std[i])
    plot_uncert(save_dir, "sig", sig_preds_std, sig_preds_std_up, sig_preds_std_down)
    plot_uncert(save_dir, "bkg", bkg_preds_std, bkg_preds_std_up, bkg_preds_std_down)

    sig_delta_up = (np.array(sig_preds_std_up)-np.array(sig_preds_std))/((np.array(sig_preds_std_up)+np.array(sig_preds_std))/2.)
    sig_delta_down = (np.array(sig_preds_std_down)-np.array(sig_preds_std))/((np.array(sig_preds_std_down)+np.array(sig_preds_std))/2.)

    n_sig_up, bins_sig_up, sig_p_ = plt.hist(sig_delta_up, bins=61, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{nominal} - \sigma$", color="r")
    n_sig_down, bins_sig_down, sig_p_ = plt.hist(sig_delta_down, bins=61, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{JES} - \sigma$", color="b")

    s_sig_up, s_sig_down = 0., 0.
    for i in range(len(n_sig_up)):
        s_sig_up += n_sig_up[i] * ((bins_sig_up[i] + bins_sig_up[i+1]) / 2)
        s_sig_down += n_sig_down[i] * ((bins_sig_down[i] + bins_sig_down[i+1]) / 2)
    mean_sig_up = s_sig_up / np.sum(n_sig_up)
    mean_sig_down = s_sig_down / np.sum(n_sig_down)

    t_sig_up, t_sig_down = 0., 0.
    for i in range(len(n_sig_up)):
        t_sig_up += n_sig_up[i] * (((bins_sig_up[i] + bins_sig_up[i+1]) / 2) - mean_sig_up)**2
        t_sig_down += n_sig_down[i] * (((bins_sig_down[i] + bins_sig_down[i+1]) / 2) - mean_sig_down)**2
    std_sig_up = np.sqrt(t_sig_up / np.sum(n_sig_up))
    std_sig_down = np.sqrt(t_sig_down / np.sum(n_sig_down))

    sig_x_up = np.linspace(mean_sig_up - 4*std_sig_up, mean_sig_up + 4*std_sig_up, 250)
    sig_x_down = np.linspace(mean_sig_down - 4*std_sig_down, mean_sig_down + 4*std_sig_down, 250)
    plt.plot(sig_x_up, stats.norm.pdf(sig_x_up, mean_sig_up, std_sig_up), color="r", label="$\mu$={0:.3f}$\pm${1:.2f}".format(mean_sig_up, std_sig_up), alpha=0.5)
    plt.plot(sig_x_down, stats.norm.pdf(sig_x_down, mean_sig_down, std_sig_down), color="b", label="$\mu$={0:.3f}$\pm${1:.2f}".format(mean_sig_down, std_sig_down), alpha=0.5)

    plt.grid()
    plt.xlabel("$(\sigma_{varied} - \sigma_{gen})|_{normalized}$", fontsize = 16)
    plt.ylabel("normalized", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/bnn_2_uncert_diff_bnns_sig.png")
    print "bnn_2_uncert_diff_sig.png was created"
    plt.savefig(save_dir+"/plots/bnn_2_uncert_diff_bnns_sig.pdf")
    print "bnn_2_uncert_diff_sig.pdf was created"
    plt.close()

    bkg_delta_up = (np.array(bkg_preds_std_up)-np.array(bkg_preds_std))/((np.array(bkg_preds_std_up)+np.array(bkg_preds_std))/2.)
    bkg_delta_down = (np.array(bkg_preds_std_down)-np.array(bkg_preds_std))/((np.array(bkg_preds_std_down)+np.array(bkg_preds_std))/2.)

    n_up, bins_up, p_ = plt.hist(bkg_delta_up, bins=61, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{nominal} - \sigma$", color="r")
    n_down, bins_down, p_ = plt.hist(bkg_delta_down, bins=61, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{JES} - \sigma$", color="b")

    s_up, s_down = 0., 0.
    for i in range(len(n_up)):
        s_up += n_up[i] * ((bins_up[i] + bins_up[i+1]) / 2)
        s_down += n_down[i] * ((bins_down[i] + bins_down[i+1]) / 2)
    mean_up = s_up / np.sum(n_up)
    mean_down = s_down / np.sum(n_down)

    t_up, t_down = 0., 0.
    for i in range(len(n_up)):
        t_up += n_up[i] * (((bins_up[i] + bins_up[i+1]) / 2) - mean_up)**2
        t_down += n_down[i] * (((bins_down[i] + bins_down[i+1]) / 2) - mean_down)**2
    std_up = np.sqrt(t_up / np.sum(n_up))
    std_down = np.sqrt(t_down / np.sum(n_down))

    x_up = np.linspace(mean_up - 4*std_up, mean_up + 4*std_up, 250)
    x_down = np.linspace(mean_down - 4*std_down, mean_down + 4*std_down, 250)
    plt.plot(x_up, stats.norm.pdf(x_up, mean_up, std_up), color="r", label="$\mu$={0:.3f}$\pm${1:.2f}".format(mean_up, std_up), alpha=0.5)
    plt.plot(x_down, stats.norm.pdf(x_down, mean_down, std_down), color="b", label="$\mu$={0:.3f}$\pm${1:.2f}".format(mean_down, std_down), alpha=0.5)

    plt.grid()
    plt.xlabel("$(\sigma_{varied} - \sigma_{gen})|_{normalized}$", fontsize = 16)
    plt.ylabel("normalized", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/bnn_2_uncert_diff_bnns_bkg.png")
    print "bnn_2_uncert_diff_bkg.png was created"
    plt.savefig(save_dir+"/plots/bnn_2_uncert_diff_bnns_bkg.pdf")
    print "bnn_2_uncert_diff_bkg.pdf was created"
    plt.close()


def plot_1_uncert_diff(save_dir):
    sig_preds_std, sig_preds_std_up, bkg_preds_std, bkg_preds_std_up = [], [], [], []
    df_test = bnn.data.get_test_data(as_matrix = False)
    df_test_up = bnn_up.data.get_test_data(as_matrix = False)
    for i in tqdm.tqdm(range(len(labels1_up))):
        evt_id = df_test_up.index[i]
        if evt_id in df_test.index:
            j = df_test.index.get_loc(evt_id)
            if labels1[j]==1:
                sig_preds_std.append(nn1_pred_std[j])
                sig_preds_std_up.append(nn1_up_pred_std[i])
            elif labels1[j]==0:
                bkg_preds_std.append(nn1_pred_std[j])
                bkg_preds_std_up.append(nn1_up_pred_std[i])

    sig_delta_up = (np.array(sig_preds_std_up)-np.array(sig_preds_std))/((np.array(sig_preds_std_up)+np.array(sig_preds_std))/2.)
    print np.max(sig_delta_up), np.min(sig_delta_up)

    n_sig_up, bins_sig_up, sig_p_ = plt.hist(sig_delta_up, bins=30, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{JES} - \sigma$", color="b")

    s_sig_up = 0.
    for i in range(len(n_sig_up)):
        s_sig_up += n_sig_up[i] * ((bins_sig_up[i] + bins_sig_up[i+1]) / 2)
    mean_sig_up = s_sig_up / np.sum(n_sig_up)

    t_sig_up = 0.
    for i in range(len(n_sig_up)):
        t_sig_up += n_sig_up[i] * (((bins_sig_up[i] + bins_sig_up[i+1]) / 2) - mean_sig_up)**2
    std_sig_up = np.sqrt(t_sig_up / np.sum(n_sig_up))

    sig_x_up = np.linspace(mean_sig_up - 5*std_sig_up, mean_sig_up + 5*std_sig_up, 250)
    sig_pdf_y = 1.0/np.sqrt(2*np.pi*std_sig_up**2)*np.exp(-0.5*(sig_x_up-mean_sig_up)**2/std_sig_up**2)
    plt.plot(sig_x_up, sig_pdf_y, color="r", label="$\mu$={0:.5f}$\pm${1:.4f}".format(mean_sig_up, std_sig_up)) #stats.norm.pdf(sig_x_up, mean_sig_up, std_sig_up)

    plt.grid()
    plt.xlabel("$\sigma_{JES} - \sigma$", fontsize = 16)
    plt.ylabel("normed", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/bnn_uncert_diff_sig.png")
    print "bnn_uncert_diff_sig.png was created"
    plt.savefig(save_dir+"/plots/bnn_uncert_diff_sig.pdf")
    print "bnn_uncert_diff_sig.pdf was created"
    plt.close()

    bkg_delta_up = (np.array(bkg_preds_std_up)-np.array(bkg_preds_std))/((np.array(bkg_preds_std_up)+np.array(bkg_preds_std))/2.)
    print np.max(bkg_delta_up), np.min(bkg_delta_up)

    n_up, bins_up, p_ = plt.hist(bkg_delta_up, bins=30, range=(-1.5,1.5), histtype='step', density=True, label="$\sigma_{JES} - \sigma$", color="b")

    s_up = 0.
    for i in range(len(n_up)):
        s_up += n_up[i] * ((bins_up[i] + bins_up[i+1]) / 2)
    mean_up = s_up / np.sum(n_up)

    t_up = 0.
    for i in range(len(n_up)):
        t_up += n_up[i] * (((bins_up[i] + bins_up[i+1]) / 2) - mean_up)**2
    std_up = np.sqrt(t_up / np.sum(n_up))

    x_up = np.linspace(mean_up - 5*std_up, mean_up + 5*std_up, 250)
    pdf_y = 1.0/np.sqrt(2*np.pi*std_up**2)*np.exp(-0.5*(x_up-mean_up)**2/std_up**2)
    plt.plot(x_up, pdf_y, color="r", label="$\mu$={0:.5f}$\pm${1:.4f}".format(mean_up, std_up)) #stats.norm.pdf(x_up, mean_up, std_up)

    plt.grid()
    plt.xlabel("$\sigma_{JES} - \sigma$", fontsize = 16)
    plt.ylabel("normed", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/bnn_uncert_diff_bkg.png")
    print "bnn_uncert_diff_bkg.png was created"
    plt.savefig(save_dir+"/plots/bnn_uncert_diff_bkg.pdf")
    print "bnn_uncert_diff_bkg.pdf was created"
    plt.close()

def plot_uncert(save_dir, tag, uncert1, uncert2, uncert3):
    plt.hist(uncert1, bins=50, range=(0.,0.08), histtype='step', density=True, label="Gen $\mu=${0:.3f}$\pm${1:.3f}".format(np.mean(uncert1),np.std(uncert1)), color="b")
    plt.hist(uncert2, bins=50, range=(0.,0.08), histtype='step', density=True, label="Nominal $\mu=${0:.3f}$\pm${1:.3f}".format(np.mean(uncert2),np.std(uncert2)), color="r")
    plt.hist(uncert3, bins=50, range=(0.,0.08), histtype='step', density=True, label="Mixed $\mu=${0:.3f}$\pm${1:.3f}".format(np.mean(uncert3),np.std(uncert3)), color="g")
    plt.xlabel("$\sigma$", fontsize = 16)
    plt.ylabel("normalized", fontsize = 16)
    plt.legend()
    plt.savefig(save_dir+"/plots/bnn_uncert_bnns_{}.png".format(tag))
    print "bnn_uncert_{}.png was created".format(tag)
    plt.savefig(save_dir+"/plots/bnn_uncert_bnns_{}.pdf".format(tag))
    print "bnn_uncert_{}.pdf was created".format(tag)
    plt.close()



#plot_event_distribution(out_dir_1)

#plot_3_diff_hist(out_dir_1)
#plot_mixing_diff_hist(out_dir_1)

#plot_2_uncert_diff(out_dir_1)
#plot_1_uncert_diff(out_dir_1)


###### evaliation code for BNN uncertainty dependency ######

# calculating the statistical uncertainty dependence
# prior = ["0p001", "0p0025", "0p01", "0p025", "0p1", "0p25", "1", "2p5","10", "25", "100", "250", "1000"]
# prior_ = [0.001, 0.0025, 0.01, 0.025, 0.1, 0.25, 1., 2.5, 10., 25., 100., 250., 1000.]
prior = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
prior_ = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
stds = []
stds_std = []

for i in prior:
    # initializing BNN training class
    bnn = BNN.BNN(
        save_path       = options.getOutputDir(),
        input_samples   = input_samples,
        category_name   = options.getCategory(),
        train_variables = options.getTrainVariables(),
        # number of epochs
        train_epochs    = options.getTrainEpochs(),
        # metrics for evaluation (c.f. KERAS metrics)
        eval_metrics    = ["acc"],
        # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
        test_percentage = options.getTestPercentage(),
        # balance samples per epoch such that there amount of samples per category is roughly equal
        balanceSamples  = options.doBalanceSamples(),
        shuffle_seed    = 42,
        evenSel         = options.doEvenSelection(),
        norm_variables  = options.doNormVariables())

    # bnn_pred, bnn_pred_std, labels = bnn.load_trained_model("/home/nshadskiy/Documents/draco-bnns/workdir/bnn_prior_{}_nomCSV_ge4j_ge3t".format(i))
    bnn_pred, bnn_pred_std, labels = bnn.load_trained_model("/home/nshadskiy/Documents/DRACO-MLfoy/workdir/bnn{}_prior_1_nomCSV_ge4j_ge3t".format(i))
    stds.append(stats.mode(bnn_pred_std)[0])
    stds_std.append(stats.tstd(bnn_pred_std))


plt.errorbar(prior_, stds, yerr=stds_std, fmt='o')
#plt.xlabel("prior width", fontsize = 16)
plt.xlabel("trained on sample size in %", fontsize = 16) # ~ 830 000 events
#plt.xscale("log")
plt.ylabel("mean of event $\sigma$", fontsize = 16)
plt.savefig("/home/nshadskiy/Documents/draco-bnns/workdir/bnn_stats_std.pdf")
print "bnns_std.pdf was created"
