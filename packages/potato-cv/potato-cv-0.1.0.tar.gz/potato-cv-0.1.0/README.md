# Semantic Segmentation and Edge Detection

## Setup

```Bash
# install mmcv and pytorch

# install other dependencies
pip install -r requirements.txt

# If you want to install potato globally
python setup.py develop
```

## Datasets

```Bash
python tools/convert_datasets/preprocess_cityscapes.py
```

## Training

```Bash
CUDA_VISIBLE_DEVICES=0,1 ./tools/dist_train.sh <path/to/config> <num_gpus>
```

## Test


### Evaluate and Visualize Segmentatation and Edges

```Bash
CUDA_VISIBLE_DEVICES=0,1 ./tools/dist_train.sh <path/to/config> <path/to/ckpt> <num_gpus> ...
```

To evaluate F-boundary scores:

```Bash
# only supports single gpu
CUDA_VISIBLE_DEVICES=0, python tools/test_boundary_fscore.py <path/to/config> <path/to/ckpt> ...
```

### Evaluate Edges

```Bash
# save edges
CUDA_VISIBLE_DEVICES=0,1 ./tools/dist_train.sh <path/to/config> <path/to/ckpt> <num_gpus> --save-edge ...

python tools/test_edge.py <path/to/config> <path/to/predictions> ...
```

Evaluating edges will take a very long time (depends on the hardware).
