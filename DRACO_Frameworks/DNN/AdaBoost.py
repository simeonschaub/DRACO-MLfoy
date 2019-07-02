import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import json

# local imports
filedir  = os.path.dirname(os.path.realpath(__file__))
DRACOdir = os.path.dirname(filedir)
basedir  = os.path.dirname(DRACOdir)
sys.path.append(basedir)

# import with ROOT
from pyrootsOfTheCaribbean.evaluationScripts import plottingScripts

# imports with keras
import utils.generateJTcut as JTcut
import data_frame

import keras
import keras.optimizers as optimizers
import keras.models as models
import keras.layers as layer
from keras import backend as K
import pandas as pd

# Limit gpu usage
import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
K.tensorflow_backend.set_session(tf.Session(config=config))


class AdaBoost():
    def __init__(self,
            save_path,
            input_samples,
            event_category,
            train_variables,
            train_epochs    = 500,
            test_percentage = 0.2,
            eval_metrics    = None,
            shuffle_seed    = None,
            balanceSamples  = False,
            adaboost_epochs = 100,
            evenSel         = None):

        # save some information
        # list of samples to load into dataframe
        self.input_samples = input_samples

        # output directory for results
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs( self.save_path )

        # name of event category (usually nJet/nTag category)
        self.JTstring       = event_category
        self.event_category = JTcut.getJTstring(event_category)
        self.categoryLabel  = JTcut.getJTlabel(event_category)
        # selection
        self.evenSel = ""
        self.oddSel = "1."
        if not evenSel == None:
            if evenSel == True:
                self.evenSel = "(Evt_Odd==0)"
                self.oddSel  = "(Evt_Odd==1)"
            elif evenSel == False:
                self.evenSel = "(Evt_Odd==1)"
                self.oddSel  = "(Evt_Odd==0)"

        # list of input variables
        self.train_variables = train_variables

        # percentage of events saved for testing
        self.test_percentage = test_percentage

        # number of train epochs
        self.train_epochs = train_epochs

        # additional metrics for evaluation of the training process
        self.eval_metrics = eval_metrics

        #number of adaboost_epochs
        self.adaboost_epochs = adaboost_epochs

        # load data set
        self.data = self._load_datasets(shuffle_seed, balanceSamples)
        self.event_classes = self.data.output_classes

        # save variable norm
        self.cp_path = self.save_path+"/checkpoints/"
        if not os.path.exists(self.cp_path):
            os.makedirs(self.cp_path)
        out_file = self.cp_path + "/variable_norm.csv"
        self.data.norm_csv.to_csv(out_file)
        print("saved variabe norms at "+str(out_file))

        # make plotdir
        self.plot_path = self.save_path+"/plots/"
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

        # layer names for in and output (needed for c++ implementation)
        self.inputName = "inputLayer"
        self.outputName = "outputLayer"


    def _load_datasets(self, shuffle_seed, balanceSamples):
        ''' load data set '''
        return data_frame.DataFrame(
            input_samples       = self.input_samples,
            event_category      = self.event_category,
            train_variables     = self.train_variables,
            test_percentage     = self.test_percentage,
            shuffleSeed         = shuffle_seed,
            balanceSamples      = balanceSamples,
            evenSel             = self.evenSel)


    def _load_architecture(self, config):
        ''' load the architecture configs '''
        # defnie default network configuration
        self.architecture = {
            "layers":                   [200,100],
            "loss_function":            "squared_hinge",
            "Dropout":                  0.3,
            "L2_Norm":                  0.,
            "batch_size":               4000,
            "optimizer":                optimizers.Adadelta(),
            "activation_function":      "selu",
            "output_activation":        "Tanh",
            "earlystopping_percentage": None,
            "earlystopping_epochs":     None,
            }

        for key in config:
            self.architecture[key] = config[key]


    def load_trained_model(self, inputDirectory):
        ''' load an already trained model '''
        pass


    def build_default_model(self):
        ''' build default straight forward DNN from architecture dictionary '''

        # infer number of input neurons from number of train variables
        number_of_input_neurons     = self.data.n_input_neurons

        # get all the architecture settings needed to build model
        number_of_neurons_per_layer = self.architecture["layers"]
        dropout                     = self.architecture["Dropout"]
        activation_function         = self.architecture["activation_function"]
        if activation_function == "leakyrelu":
            activation_function = "linear"
        l2_regularization_beta      = self.architecture["L2_Norm"]
        output_activation           = self.architecture["output_activation"]

        # define input layer
        Inputs = keras.layers.Input(
            shape = (number_of_input_neurons,),
            name  = self.inputName)

        X = Inputs
        self.layer_list = [X]

        # loop over dense layers
        for iLayer, nNeurons in enumerate(number_of_neurons_per_layer):
            X = keras.layers.Dense(
                units               = nNeurons,
                activation          = activation_function,
                kernel_regularizer  = keras.regularizers.l2(l2_regularization_beta),
                name                = "DenseLayer_"+str(iLayer)
                )(X)

            if self.architecture["activation_function"] == "leakyrelu":
                X = keras.layers.LeakyReLU(alpha=0.3)(X)

            # add dropout percentage to layer if activated
            if not dropout == 0:
                X = keras.layers.Dropout(dropout, name = "DropoutLayer_"+str(iLayer))(X)

        # generate output layer
        X = keras.layers.Dense(
            units               = self.data.n_output_neurons,
            activation          = output_activation.lower(),
            kernel_regularizer  = keras.regularizers.l2(l2_regularization_beta),
            name                = self.outputName
            )(X)

        # define model
        model = models.Model(inputs = [Inputs], outputs = [X])
        model.summary()

        return model


    def get_alpha(self):
        '''Calculate weighted error and return alpha_t after each training'''
        # model_prediction_vector = self.model.predict(self.data.get_test_data(as_matrix = True))
        #hier kann man auch self... verwenden da prediciton vectoren schon in train_model erstellt
        model_train_prediction = self.model.predict(self.data.get_train_data(as_matrix = True))
        model_train_label = self.data.get_train_labels(as_categorical = False) #not sure if should be True
        model_train_weights = self.data.get_train_weights()
        #Calculate epsilon and alpha
        num = model_train_prediction.shape[0]
        # make_discret = lambda x: -1 if x<0 else 1
        model_train_prediction_discret = np.array([])
        for x in model_train_prediction:
            if x<0:
                model_train_prediction_discret = np.append(model_train_prediction_discret, -1)
            else:
                model_train_prediction_discret = np.append(model_train_prediction_discret, 1)
        weight_sum = np.sum(model_train_weights)
        weight_false = 0
        for i in np.arange(0,num):
            if model_train_prediction_discret[i] != model_train_label[i]:
                weight_false += model_train_weights[i]
        epsilon = weight_false/weight_sum
        alpha = 0.5*np.log((1-epsilon)/epsilon)
        #adjust weights
        self.data.ada_adjust_weights(model_train_prediction_discret, alpha)
        #check if epsilon < 0.5
        if epsilon > 0.5:
            print("# DEBUG: In ada_eval_training epsilon > 0.5")
        return alpha


    def build_model(self, config):
        ''' build a DNN model (weak Classifier)
            use options defined in 'config' dictionary '''

        self._load_architecture(config)
        model = self.build_default_model()

        # compile the model
        model.compile(
            loss        = self.architecture["loss_function"],
            optimizer   = self.architecture["optimizer"],
            metrics     = self.eval_metrics)

        # save the model
        self.model = model

        # save net information
        out_file    = self.save_path+"/model_summary.yml"
        yml_model   = self.model.to_yaml()
        with open(out_file, "w") as f:
            f.write(yml_model)


    def train_model(self):
        '''train the model'''

        self.weak_model_trainout = [] #does not contain the trained model
        self.weak_model_trained = [] #trained weak Classifier
        self.alpha_t = []
        self.train_prediction_vector = []   #collect prediction vector for each weak classifier
        self.test_prediction_vector = []
        # self.train_label = []   #labels need to be collected because order of df changes after evaluation
        # self.test_label = []
        for t in np.arange(0,self.adaboost_epochs):
            self.weak_model_trainout.append(self.model.fit(
                x = self.data.get_train_data(as_matrix = True),
                y = self.data.get_train_labels(),
                batch_size          = self.architecture["batch_size"],
                epochs              = self.train_epochs,
                shuffle             = True,
                # callbacks           = callbacks,
                validation_split    = 0.25,
                sample_weight       = self.data.get_train_weights()))
            #get prediction vector for training and test
            self.train_prediction_vector.append(self.model.predict(self.data.get_train_data(as_matrix = True)))
            self.test_prediction_vector.append(self.model.predict(self.data.get_test_data(as_matrix = True)))
            #get labels
            # self.train_label.append(self.data.get_train_labels(as_categorical = False))
            # self.test_label.append(self.data.get_test_labels(as_categorical = False))
            #get alpha
            self.alpha_t.append(self.get_alpha())   #make dict alpha -> model
            #collect weak classifier
            self.weak_model_trained.append(self.model)


    def save_model(self):
        pass


    def weight_prediction(self, pred, alpha):
        for i in np.arrange(0,len(alpha)):
            pred[i] = pred[i]*alpha[i]
        return pred


    def strong_classification(self, pred, alpha):
        '''builds prediciton vector for strong classifier'''
        pred_array = np.asarray(pred)
        for i in np.arange(0,len(alpha)):
            pred_array[i] = pred_array[i]*alpha[i]
        sum = np.sum(pred_array, axis = 0)
        final_prediction_vector = np.array([])
        for x in sum:
            if x<0:
                final_prediction_vector = np.append(final_prediction_vector, -1)
            else:
                final_prediction_vector = np.append(final_prediction_vector, 1)
        return final_prediction_vector


    def eval_model(self):
        '''evalute trained model'''
        '''Should contain:  -Plot prediciton_fraction
                            -Get roc'''
        self.train_label = self.data.get_train_labels(as_categorical = False)
        self.test_label = self.data.get_test_labels(as_categorical = False)
        #get values after each adaboost_epoch
        train_fraction = np.array([])
        test_fraction = np.array([])
        for i in np.arange(0, len(self.train_prediction_vector)):
            train_prediction_final = self.strong_classification(self.train_prediction_vector, self.alpha_t[0:i])
            test_prediction_final = self.strong_classification(self.test_prediction_vector, self.alpha_t[0:1])
            print("# DEBUG: count_nonzero: ", np.count_nonzero(test_prediction_final==self.test_label))
            train_fraction = np.append(train_fraction,
                        np.count_nonzero(train_prediction_final==self.train_label)/float(self.train_label.shape[0]))
            test_fraction = np.append(test_fraction,
                        np.count_nonzero(test_prediction_final==self.test_label)/float(self.test_label.shape[0]))
        #plot
        epoches = np.arange(1, len(self.train_prediction_vector)+1)
        # print("# DEBUG: check dimension: ", epoches.shape, train_fraction.shape)
        # print("# DEBUG: test_fraction: ", test_fraction)
        # print("# DEBUG: train_fraction: ", train_fraction)
        plt.plot(epoches, train_fraction, 'r--')
        plt.plot(epoches, test_fraction, 'g--')
        plt.show()
