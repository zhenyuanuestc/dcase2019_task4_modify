import math
import os
import pandas as pd

workspace = ".."
# Dataset Paths
weak = 'dataset/metadata/train/weak.csv'
unlabel = 'dataset/metadata/train/unlabel_in_domain.csv'
synthetic = 'dataset/metadata/train/synthetic.csv'
validation = 'dataset/metadata/validation/validation.csv'
test2018 = 'dataset/metadata/validation/test_dcase2018.csv'
eval2018 = 'dataset/metadata/validation/eval_dcase2018.csv'

# config
# prepare_data
sample_rate = 44100
n_window = 2048
hop_length = 511
n_mels = 64
max_len_seconds = 10.
max_frames = math.ceil(max_len_seconds * sample_rate / hop_length)

f_min = 0.
f_max = 22050.

lr = 0.0001
initial_lr = 0.
beta1_before_rampdown = 0.9
beta1_after_rampdown = 0.5
beta2_during_rampdup = 0.99
beta2_after_rampup = 0.999
weight_decay_during_rampup = 0.99
weight_decay_after_rampup = 0.999

max_consistency_cost = 2
max_learning_rate = 0.001

median_window = 5

# Main
num_workers = 12
batch_size = 24
n_epoch = 100

checkpoint_epochs = 1

save_best = True

file_path = os.path.abspath(os.path.dirname(__file__))
# read_csv中的sep='\t'表示以TAB为分隔符，dropna()表示删除为NAN的行，最终返回一个包含无重复的event_label的list
classes = pd.read_csv(os.path.join(file_path, "..", validation), sep="\t").event_label.dropna().sort_values().unique()

'''resnet_kwargs = {'n_in_channel': 1,
                 'mel_features': n_mels,
                 'num_classes': len(classes),
                 'dropout': 0.5,
                 "kernel_size": 3 * [3], "padding": 3 * [1], "stride": 3 * [1], "nb_filters": [64, 64, 64],
                 'pooling': list(3 * ((2, 4),))}'''

crnn_kwargs = {"n_in_channel": 1, "nclass": len(classes), "attention": True, "n_RNN_cell": 64,
               "n_layers_RNN": 2,
                "activation": "glu",
                "dropout": 0.5,
               "kernel_size": 3 * [3], "padding": 3 * [1], "stride": 3 * [1], "nb_filters": [64, 64, 64],
                "pooling": list(3 * ((2, 4),))}
pooling_time_ratio = 8  # 2 * 2 * 2
