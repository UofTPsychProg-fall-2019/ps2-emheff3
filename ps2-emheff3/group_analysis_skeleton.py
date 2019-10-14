#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil
import csv

#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename

dirpath = os.getcwd() #get the current directory
testingrooms = ['A','B','C']
try:
    for room in testingrooms: #for each testing room, try to copy the data file into the rawdata folder
        srcFilePath = dirpath + "/testingroom" + room + "/experiment_data.csv"
        destFilePath = dirpath + "/rawdata/data" + room + ".csv"
        shutil.copyfile(srcFilePath, destFilePath)
                
except:
    print("An error occurred. Please make sure the correct files and folders exist in the following location: " + dirpath)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5)) #Create an empty np array to store the data
for room in testingrooms:
    tmp = sp.loadtxt(dirpath + "/rawdata/data" + room + ".csv", delimiter = ",")
    data = np.vstack([data,tmp]) #Add the data row by row to the data array

#print(data)

#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.mean(data[:,3])   # 91.48%
mrt_avg = np.mean(data[:,4])   # 477.3 ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
#Create variables in which to store the sum for each measure, and two variables to count the 
#number of face and word data points
words_acc_sum = 0
words_rt_sum = 0
faces_acc_sum = 0
faces_rt_sum = 0
word_count = 0
face_count = 0
for row in data:
    if row[1]==1:
        words_acc_sum += row[3]
        words_rt_sum += row[4]
        word_count += 1
    elif row[1]==2: #could just use "else", as this value can only be 1 or 2
        faces_acc_sum += row[3]
        faces_rt_sum += row[4]
        face_count += 1

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms
#Calculate averages by dividing each sum by the number of values
mean_words_acc = words_acc_sum/word_count
mean_words_rt = words_rt_sum/word_count
mean_faces_acc = faces_acc_sum/face_count
mean_faces_rt = faces_rt_sum/face_count

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
#Calculate the average of the rt and acc columns, slicing the data depending on whether the third
#column is equal to 1 or 2. 
acc_wp = np.mean(data[data[:,2]==1,3]) # 94.0%
acc_bp = np.mean(data[data[:,2]==2,3])   # 88.9%
mrt_wp = np.mean(data[data[:,2]==1,4]) # 469.6 ms
mrt_bp = np.mean(data[data[:,2]==2,4])   # 485.1 ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
#avg_med_words_wp_arr = data[data[:,1]==1 and data[:2 == 1],4]
#Separate the data into words and faces
words_data = data[data[:,1]==1]
faces_data = data[data[:,1]==2]

#Separate the data again, this time into wp and bp categories
words_wp_data = words_data[words_data[:,2]==1]
words_bp_data = words_data[words_data[:,2]==2]
faces_wp_data = faces_data[faces_data[:,2]==1]
faces_bp_data = faces_data[faces_data[:,2]==2]

#Calculate the averages (I wasn't sure if I was allowed to use the np.mean function)
words_wp_med_avg = sum(words_wp_data[:,4])/len(words_wp_data)
words_bp_med_avg = sum(words_bp_data[:,4])/len(words_bp_data)
faces_wp_med_avg = sum(faces_wp_data[:,4])/len(faces_wp_data)
faces_bp_med_avg = sum(faces_bp_data[:,4])/len(faces_bp_data)

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#

import scipy.stats
ttest_words_t, ttest_words_p = scipy.stats.ttest_rel(words_data[words_data[:,2]==1,4], words_data[words_data[:,2]==2,4])
ttest_faces_t, ttest_faces_p = scipy.stats.ttest_rel(faces_data[faces_data[:,2]==1,4], faces_data[faces_data[:,2]==2,4])

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096

#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print("Mean Word Accuracy: {:4.1f}%".format(100*mean_words_acc))
print("Mean Word Reaction Time: {:5.1f} ms".format(mean_words_rt))
print("Mean Face Accuracy: {:4.1f}%".format(100*mean_faces_acc))
print("Mean Face Reaction Time: {:5.1f} ms".format(mean_faces_rt))
print("Mean Accuracy (wp): {:4.1f}%, Mean Accuracy (bp): {:4.1f}%".format(acc_wp*100, acc_bp*100))
print("Mean Reaction Time (wp): {:5.1f} ms, Mean Reaction Time (bp): {:5.1f} ms".format(mrt_wp, mrt_bp))
print("Words (white/pleasant) median average: {:5.1f} ms".format(words_wp_med_avg))
print("Words (black/pleasant) median average: {:5.1f} ms".format(words_bp_med_avg))
print("Faces (white/pleasant) median average: {:5.1f} ms".format(faces_wp_med_avg))
print("Faces (black/pleasant) median average: {:5.1f} ms".format(faces_bp_med_avg))
print("t-test for words: t = {:4.2f}, p = {:.2E}".format(ttest_words_t, ttest_words_p))
print("t-test for faces: t = {:4.2f}, p = {:.2E}".format(ttest_faces_t, ttest_faces_p))
#%%
