import matplotlib.pyplot as plt
import numpy as np
import random
image_size = 28 # width and length
no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
image_pixels = image_size * image_size
data_path = "/home/harshad/Desktop/"                        
train_data = np.loadtxt(data_path + "mnist_train.csv", 
                        delimiter=",")
test_data = np.loadtxt(data_path + "mnist_test.csv", 
                       delimiter=",") 
fac = 0.99 / 255                                            # all this from this website : 
train_imgs = np.asfarray(train_data[:, 1:]) * fac + 0.01    # https://www.python-course.eu/
test_imgs = np.asfarray(test_data[:, 1:]) * fac + 0.01      # neural_network_mnist.php
train_labels = np.asfarray(train_data[:, :1])
test_labels = np.asfarray(test_data[:, :1])

my_train_labels = np.asfarray(train_data[:, 0])
my_test_labels = np.asfarray(test_data[:, 0])

#no apparent use of the following snippet
lr = np.arange(no_of_different_labels)
## transform labels into one hot representation
train_labels_one_hot = (lr==train_labels).astype(np.float)
test_labels_one_hot = (lr==test_labels).astype(np.float)
## we don't want zeroes and ones in the labels neither:
train_labels_one_hot[train_labels_one_hot==0] = 0.01
train_labels_one_hot[train_labels_one_hot==1] = 0.99
test_labels_one_hot[test_labels_one_hot==0] = 0.01
test_labels_one_hot[test_labels_one_hot==1] = 0.99

def find_pixel_array(n):
    if (n==0):
        ans=np.full((28,28), 0.01)
        for i in range(28):
            for j in range(28):
                if (i==0 or i==27 or j==0 or j==27):        # border
                    ans[i][j]=0.60
                else:
                    ans[i][j]=random.random()/4             # noise
        return ans
    else:
        m=random.randint(1,9000)                        # there 10000 choices, i choose from 9000
        while (my_test_labels[m]!=n):                   
            m=m+1                                      
        ans=test_imgs[m].reshape((28,28))
        for i in range(28):
            if (i==0 or i==27):
                for j in range(28):
                    ans[i][j]=0.60
            else:
                ans[i][0]=0.60
                ans[i][27]=0.60
        return ans

#### this one was returning an unnecessary white border along 2 sides ###
#def form_full_pixel_array(arr):
#    ans=np.full((28,280), 0.01)
#    for i in range(9):
#        row=np.full((28,28), 0.01)
#        for j in range(9):
#            #arri=find_pixel_array(arr[i][j])
#            arrf=find_pixel_array(arr[i][j])
#            row=np.concatenate((row,arrf), axis=1)
#        ans=np.concatenate((ans,row), axis=0)
#    return ans

def firstofrow(arr, i):                             
    return find_pixel_array(arr[i][0])              

def firstrow(arr):
    row=firstofrow(arr, 0)
    for i in range(1,9):
        arrf=find_pixel_array(arr[0][i])
        row=np.concatenate((row,arrf), axis=1)
    return row

def form_full_pixel_array(arr):
    ans=firstrow(arr)
    for i in range(1,9):
        row=firstofrow(arr, i)
        for j in range(1,9):
            arrf=find_pixel_array(arr[i][j])
            row=np.concatenate((row,arrf), axis=1)
        ans=np.concatenate((ans,row), axis=0)
    for i in range(84,252,84):
        for j in range(252):
            ans[i][j]=0.99
            ans[i-1][j]=0.99                            # dark border
            ans[j][i]=0.99
            ans[j][i-1]=0.99
    return ans

def convert(sudoku, i):
    pixel_arr=form_full_pixel_array(sudoku)
    plt.figure(figsize=(2.52,2.52))                                 # this
    img=plt.imshow(pixel_arr, cmap="Greys")
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)          # with this removes the padding
    filename="image"+str(i)+".jpeg"
    plt.savefig(filename)                                           # now this image has size 252x252 pixels

sudoku25=[[0,0,0,3,7,0,0,2,0],
          [0,9,0,0,8,5,7,0,0],
          [3,0,0,9,0,0,0,0,5],
          [1,0,0,0,0,0,0,8,0],
          [0,0,0,0,0,0,3,0,0],
          [0,0,0,0,9,0,0,0,7],
          [2,0,0,6,0,0,0,0,1],
          [0,4,8,0,0,0,6,0,0],
          [0,3,1,0,0,0,0,4,0]]
