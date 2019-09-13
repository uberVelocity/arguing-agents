#!/bin/bash

#######################
# BEFORE YOU RUN THIS!#
#######################
# make sure there's nothing in here that could harm your computer
# realize that you may have to run this script with sudo privileges, be careful!



# Comment out any of these if its already installed
pip3 install keras
pip3 install tensorflow
pip3 install spacy
pip3 install sklearn
pip3 install pandas
pip3 install numpy
pip3 install tqdm  # a funky little progress bar thing

# download spaCy model that we use

python3 -m spacy download en_core_web_lg

# commented out by default but add this in if you wish to immediately run the code
#python3 train_lstm.py
