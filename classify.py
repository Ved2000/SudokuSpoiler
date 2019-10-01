from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
image_size = 28 # width and length
no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
image_pixels = image_size * image_size                     
train_data = np.loadtxt( "mnist_train.csv", 
                        delimiter=",")
test_data = np.loadtxt( "mnist_test.csv", 
                       delimiter=",") 
fac = 0.99 / 255                                            # all this from this website : 
train_imgs = np.asfarray(train_data[:, 1:]) * fac + 0.01    # https://www.python-course.eu/
test_imgs = np.asfarray(test_data[:, 1:]) * fac + 0.01      # neural_network_mnist.php
train_labels = np.asfarray(train_data[:, :1])
test_labels = np.asfarray(test_data[:, :1])

my_train_labels = np.asfarray(train_data[:, 0])

my_test_labels = np.asfarray(test_data[:, 0])

lr = np.arange(no_of_different_labels)
## transform labels into one hot representation
train_labels_one_hot = (lr==train_labels).astype(np.float)
test_labels_one_hot = (lr==test_labels).astype(np.float)
## we don't want zeroes and ones in the labels neither:
train_labels_one_hot[train_labels_one_hot==0] = 0.01
train_labels_one_hot[train_labels_one_hot==1] = 0.99
test_labels_one_hot[test_labels_one_hot==0] = 0.01
test_labels_one_hot[test_labels_one_hot==1] = 0.99
@np.vectorize
def sigmoid(x):
    return 1 / (1 + np.e ** -x)
activation_function = sigmoid
from scipy.stats import truncnorm
def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, 
                     (upp - mean) / sd, 
                     loc=mean, 
                     scale=sd)
class NeuralNetwork:
    
    def __init__(self, 
                 no_of_in_nodes, 
                 no_of_out_nodes, 
                 no_of_hidden_nodes,
                 learning_rate):
        self.no_of_in_nodes = no_of_in_nodes
        self.no_of_out_nodes = no_of_out_nodes
        self.no_of_hidden_nodes = no_of_hidden_nodes
        self.learning_rate = learning_rate 
        self.create_weight_matrices()
        
    def create_weight_matrices(self):
        """ 
        A method to initialize the weight 
        matrices of the neural network
        """
        rad = 1 / np.sqrt(self.no_of_in_nodes)
        X = truncated_normal(mean=0, 
                             sd=1, 
                             low=-rad, 
                             upp=rad)
        self.wih = X.rvs((self.no_of_hidden_nodes, 
                                       self.no_of_in_nodes))
        rad = 1 / np.sqrt(self.no_of_hidden_nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.who = X.rvs((self.no_of_out_nodes, 
                                         self.no_of_hidden_nodes))
        
    
    def train(self, input_vector, target_vector):
        """
        input_vector and target_vector can 
        be tuple, list or ndarray
        """
        
        input_vector = np.array(input_vector, ndmin=2).T
        target_vector = np.array(target_vector, ndmin=2).T
        
        output_vector1 = np.dot(self.wih, 
                                input_vector)
        output_hidden = activation_function(output_vector1)
        
        output_vector2 = np.dot(self.who, 
                                output_hidden)
        output_network = activation_function(output_vector2)
        
        output_errors = target_vector - output_network
        # update the weights:
        tmp = output_errors * output_network \
              * (1.0 - output_network)     
        tmp = self.learning_rate  * np.dot(tmp, 
                                           output_hidden.T)
        self.who += tmp
        # calculate hidden errors:
        hidden_errors = np.dot(self.who.T, 
                               output_errors)
        # update the weights:
        tmp = hidden_errors * output_hidden * \
              (1.0 - output_hidden)
        self.wih += self.learning_rate \
                          * np.dot(tmp, input_vector.T)
        
        
    
    def run(self, input_vector):
        # input_vector can be tuple, list or ndarray
        input_vector = np.array(input_vector, ndmin=2).T
        output_vector = np.dot(self.wih, 
                               input_vector)
        output_vector = activation_function(output_vector)
        
        output_vector = np.dot(self.who, 
                               output_vector)
        output_vector = activation_function(output_vector)
    
        return output_vector
            
    def confusion_matrix(self, data_array, labels):
        cm = np.zeros((10, 10), int)
        for i in range(len(data_array)):
            res = self.run(data_array[i])
            res_max = res.argmax()
            target = labels[i][0]
            cm[res_max, int(target)] += 1
        return cm    
    def precision(self, label, confusion_matrix):
        col = confusion_matrix[:, label]
        return confusion_matrix[label, label] / col.sum()
    
    def recall(self, label, confusion_matrix):
        row = confusion_matrix[label, :]
        return confusion_matrix[label, label] / row.sum()
        
    
    def evaluate(self, data, labels):
        corrects, wrongs = 0, 0
        for i in range(len(data)):
            res = self.run(data[i])
            res_max = res.argmax()
            if res_max == labels[i]:
                corrects += 1
            else:
                wrongs += 1
        return corrects, wrongs
            
ANN = NeuralNetwork(no_of_in_nodes = image_pixels, 
                    no_of_out_nodes = 10, 
                    no_of_hidden_nodes = 100,
                    learning_rate = 0.1)
    
    
for i in range(len(train_imgs)):
    ANN.train(train_imgs[i], train_labels_one_hot[i])

#for i in range(20):
#    res = ANN.run(test_imgs[i])
#    print(test_labels[i], np.argmax(res), np.max(res))

def get_grayscale(image_path):
    rgb=plt.imread(image_path)
    gs=np.dot(rgb[...,:3],[0.299,0.587,0.114])               # convert rgb to greyscale
    gs=gs*fac+0.01                                          
    return 1-gs                                            # for some strange reason, gs was inverted : white ka black;
                                                            # black ka white. hence 1-gs.
threshold=0.55

def sliding_window(image_path):
    #im = Image.open("image25.jpeg")
    #img=im.convert(mode='L')
    #img=img.resize((252,252))
    gs=get_grayscale(image_path)
    ans=[[0]*9]*9
    for i in range(1,10):
        for j in range(1,10):
            one_digits_array=gs[(i-1)*28:i*28,(j-1)*28:j*28]
            abc=one_digits_array.reshape(784,1)
            res=ANN.run(abc[:,0]*fac+0.01)
            if (np.max(res)<threshold):
              ans[i-1][j-1]=0
            else:
              ans[i-1][j-1]=np.argmax(res)
    return ans 

print sliding_window("image25.jpeg") 
#print ans  

#this is the 28*28 array for the seven at the (0,4) position
arrfor7=array([[0.51635294, 0.52023529, 0.51635294, 0.51635294, 0.51635294,
        0.51635294, 0.51247059, 0.52411765, 0.51635294, 0.51635294,
        0.51635294, 0.51635294, 0.51635294, 0.51635294, 0.51635294,
        0.51635294, 0.51635294, 0.51635294, 0.51635294, 0.51635294,
        0.51635294, 0.51635294, 0.51635294, 0.51635294, 0.51635294,
        0.51635294, 0.52411765, 0.50470588],
       [0.51635294, 0.00388235, 0.        , 0.00776471, 0.        ,
        0.00776471, 0.        , 0.        , 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.        ,
        0.00776471, 0.        , 0.52411765],
       [0.51635294, 0.        , 0.01941176, 0.        , 0.00776471,
        0.00776471, 0.00776471, 0.01164706, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00776471,
        0.        , 0.01552941, 0.50082353],
       [0.51635294, 0.00776471, 0.        , 0.        , 0.        ,
        0.00388235, 0.01164706, 0.        , 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.        ,
        0.00776471, 0.        , 0.52411765],
       [0.52411765, 0.        , 0.00776471, 0.02717647, 0.        ,
        0.01164706, 0.        , 0.01164706, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00776471,
        0.01552941, 0.        , 0.52023529],
       [0.52023529, 0.01552941, 0.01164706, 0.        , 0.00388235,
        0.01552941, 0.        , 0.00776471, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00776471, 0.52023529],
       [0.50082353, 0.        , 0.01164706, 0.01941176, 0.00776471,
        0.        , 0.01164706, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00776471,
        0.        , 0.00776471, 0.51247059],
       [0.528     , 0.00388235, 0.        , 0.00776471, 0.        ,
        0.00388235, 0.        , 0.00776471, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.        ,
        0.00388235, 0.        , 0.53188235],
       [0.52411765, 0.        , 0.        , 0.01164706, 0.        ,
        0.01164706, 0.        , 0.00776471, 0.        , 0.01164706,
        0.        , 0.01164706, 0.        , 0.03105882, 0.05823529,
        0.04270588, 0.41541176, 0.46976471, 0.45811765, 0.132     ,
        0.03882353, 0.        , 0.01164706, 0.00388235, 0.00388235,
        0.00388235, 0.        , 0.52411765],
       [0.50858824, 0.01552941, 0.00776471, 0.02329412, 0.10870588,
        0.10870588, 0.10482353, 0.10870588, 0.11258824, 0.10870588,
        0.10482353, 0.52411765, 0.56682353, 0.83082353, 0.97447059,
        0.99      , 0.98223529, 0.98611765, 0.99      , 0.97058824,
        0.64058824, 0.01552941, 0.        , 0.        , 0.00776471,
        0.00776471, 0.00776471, 0.51247059],
       [0.528     , 0.        , 0.43482353, 0.69882353, 0.99      ,
        0.98611765, 0.98611765, 0.98223529, 0.98611765, 0.98223529,
        0.99      , 0.97447059, 0.99      , 0.98223529, 0.99      ,
        0.97835294, 0.98611765, 0.98611765, 0.99      , 0.99      ,
        0.98223529, 0.462     , 0.00776471, 0.00388235, 0.00776471,
        0.        , 0.        , 0.52023529],
       [0.51247059, 0.00388235, 0.99      , 0.99      , 0.97835294,
        0.98223529, 0.99      , 0.99      , 0.98223529, 0.98611765,
        0.99      , 0.98223529, 0.98611765, 0.99      , 0.858     ,
        0.57070588, 0.56294118, 0.10482353, 0.16694118, 0.86964706,
        0.97058824, 0.99      , 0.00388235, 0.00388235, 0.        ,
        0.00388235, 0.01164706, 0.528     ],
       [0.52411765, 0.        , 0.264     , 0.90458824, 0.45035294,
        0.45423529, 0.44258824, 0.49305882, 0.98611765, 0.85411765,
        0.45035294, 0.47364706, 0.20188235, 0.02717647, 0.04658824,
        0.        , 0.00776471, 0.        , 0.        , 0.66388235,
        0.99      , 0.98223529, 0.00388235, 0.        , 0.00776471,
        0.00776471, 0.        , 0.51247059],
       [0.51247059, 0.00388235, 0.        , 0.00388235, 0.        ,
        0.00776471, 0.01552941, 0.00776471, 0.00388235, 0.        ,
        0.        , 0.        , 0.        , 0.00388235, 0.02329412,
        0.00388235, 0.        , 0.01941176, 0.06211765, 0.83470588,
        0.99      , 0.95117647, 0.00388235, 0.01164706, 0.00388235,
        0.        , 0.00388235, 0.51635294],
       [0.50858824, 0.01164706, 0.00388235, 0.        , 0.01552941,
        0.        , 0.        , 0.        , 0.        , 0.00388235,
        0.02329412, 0.00776471, 0.01552941, 0.00776471, 0.        ,
        0.        , 0.01552941, 0.        , 0.17470588, 0.99      ,
        0.98223529, 0.45811765, 0.        , 0.00388235, 0.        ,
        0.00776471, 0.00776471, 0.51247059],
       [0.52411765, 0.        , 0.00776471, 0.00388235, 0.        ,
        0.01941176, 0.        , 0.00776471, 0.00776471, 0.00776471,
        0.        , 0.        , 0.00388235, 0.00776471, 0.        ,
        0.00776471, 0.00388235, 0.02717647, 0.88129412, 0.98611765,
        0.99      , 0.12811765, 0.00776471, 0.00388235, 0.01164706,
        0.00388235, 0.        , 0.52023529],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00776471, 0.        ,
        0.00776471, 0.00388235, 0.        , 0.01552941, 0.        ,
        0.00776471, 0.        , 0.05047059, 0.99      , 0.99      ,
        0.60952941, 0.02329412, 0.        , 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.52411765],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.        , 0.01164706,
        0.00388235, 0.01164706, 0.        , 0.        , 0.00388235,
        0.00388235, 0.        , 0.05435294, 0.97835294, 0.98223529,
        0.56294118, 0.00388235, 0.00388235, 0.00776471, 0.        ,
        0.00388235, 0.        , 0.50858824],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.        , 0.        , 0.00388235, 0.01941176, 0.00388235,
        0.00776471, 0.        , 0.50858824, 0.99      , 0.97447059,
        0.07764706, 0.01164706, 0.        , 0.01164706, 0.00388235,
        0.00388235, 0.00776471, 0.53576471],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.01552941,
        0.        , 0.01164706, 0.02329412, 0.        , 0.        ,
        0.00776471, 0.05435294, 0.97835294, 0.99      , 0.33776471,
        0.00776471, 0.        , 0.02717647, 0.        , 0.00776471,
        0.00776471, 0.        , 0.50858824],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.        ,
        0.01552941, 0.        , 0.00776471, 0.01164706, 0.00388235,
        0.00776471, 0.49694118, 0.99      , 0.98223529, 0.16694118,
        0.01164706, 0.        , 0.        , 0.00776471, 0.        ,
        0.01941176, 0.00388235, 0.51635294],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.        , 0.00776471, 0.00388235, 0.01164706,
        0.198     , 0.96670588, 0.99      , 0.81141176, 0.02717647,
        0.00388235, 0.        , 0.        , 0.00776471, 0.00776471,
        0.00776471, 0.00388235, 0.52023529],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.01552941,
        0.        , 0.02717647, 0.        , 0.        , 0.02329412,
        0.24847059, 0.97835294, 0.99      , 0.29894118, 0.        ,
        0.        , 0.01552941, 0.00388235, 0.        , 0.        ,
        0.01164706, 0.        , 0.51247059],
       [0.51635294, 0.00388235, 0.00388235, 0.00388235, 0.00388235,
        0.00388235, 0.00388235, 0.00388235, 0.00388235, 0.        ,
        0.00776471, 0.        , 0.01164706, 0.00776471, 0.        ,
        0.78035294, 0.99      , 0.94341176, 0.08541176, 0.00776471,
        0.00388235, 0.        , 0.00776471, 0.00388235, 0.01164706,
        0.        , 0.00776471, 0.528     ],
       [0.51635294, 0.        , 0.00776471, 0.00388235, 0.00776471,
        0.        , 0.01164706, 0.        , 0.        , 0.01552941,
        0.00388235, 0.        , 0.02329412, 0.        , 0.15917647,
        0.924     , 0.98223529, 0.77647059, 0.        , 0.01941176,
        0.        , 0.00388235, 0.00776471, 0.        , 0.        ,
        0.01164706, 0.00388235, 0.52411765],
       [0.51635294, 0.00776471, 0.        , 0.00776471, 0.        ,
        0.00388235, 0.        , 0.00388235, 0.00776471, 0.        ,
        0.01164706, 0.00776471, 0.        , 0.01552941, 0.28729412,
        0.98223529, 0.99      , 0.08929412, 0.        , 0.        ,
        0.01164706, 0.01164706, 0.        , 0.00776471, 0.00388235,
        0.01552941, 0.00388235, 0.50470588],
       [0.51247059, 0.        , 0.01164706, 0.        , 0.01164706,
        0.        , 0.        , 0.01552941, 0.00776471, 0.01164706,
        0.        , 0.00776471, 0.00388235, 0.00388235, 0.03105882,
        0.82305882, 0.53964706, 0.        , 0.01164706, 0.01164706,
        0.        , 0.        , 0.        , 0.00776471, 0.00776471,
        0.        , 0.00388235, 0.52411765],
       [0.51635294, 0.51635294, 0.51635294, 0.51247059, 0.51635294,
        0.52023529, 0.52023529, 0.51247059, 0.51247059, 0.51247059,
        0.528     , 0.51635294, 0.52023529, 0.51635294, 0.52023529,
        0.50082353, 0.51247059, 0.53188235, 0.50858824, 0.52023529,
        0.52411765, 0.52411765, 0.52023529, 0.50858824, 0.51247059,
        0.53188235, 0.51635294, 0.50858824]])