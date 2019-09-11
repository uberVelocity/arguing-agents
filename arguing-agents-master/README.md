# arguing-agents
The project files pertaining to the the arguing agents course of 2018 (group 12)

# Running the code
For the best model we have found, please see `train_lstm.py` in the top directory

Model files and weights are not included as the files are massive (800MB+), you will have to generate those yourself.

A small bash script is included `pre_train.sh`. This exists so that you don't have to personally chase down dependencies.
The script installs everything you should need to run the code.
**Check the bash script before you run it!**

As a benchmark, `train_lstm.py` takes around 30 minutes to run on 2 physical (4 virtual) cores.
Given more cores it will likely be faster as Keras utilizes all available processing cores to compute tensors.

To run the SVM model just run the main_new.py
