<!--
document_lifecycle: ACCEPTED
generated_by_skill: experiment-provenance-and-reproducibility
skill_version: 0.1.0
source_commit: repro-fixture@9c3f1a2
source_documents:
  - source-recipe.md
last_verified: 2026-08-02
-->

# Train ResNet-50 on ImageNet

We provide below the recipe to train a ResNet-50 [model](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html) on the ImageNet dataset and achieve 74.05% single crop accuracy on the validation set. This recipe was based on models that were previously trained in [TensorFlow](https://github.com/tensorflow/models/tree/master/official/resnet) and [Caffe](https://github.com/KaimingHe/deep-residual-networks).

## Data

### Raw data

#### Description

The ImageNet dataset contains ~14M images that are classified into ~21K categories from the WordNet hierarchy. The classification task in the ImageNet Large Scale Visual Recognition Competition (ILSVRC) uses a subset of 1000 categories with ~1M associated images for training. Each image has a single label associated, and a bounding box with the object location may be available.

#### Path
Information on how to download ImageNet can be found on the dataset [website](http://image-net.org/). You need to sign up for an account in order to access the data. 

### Data Processing Methods

#### Description

Images are downloaded and processed into the TFRecord format. The training data is sharded into 1024 training files with names `train-0????-of-01024` and 128 validation files with names `validation-0????-of-00128`. The classes are randomly distributed within each file. Data processing may take up to half a day. 

#### Code
We follow the data processing methods from the Inception [guide](https://github.com/tensorflow/models/tree/master/research/inception#getting-started). 

#### Path
The processed data can be found in HDFS at `hdfs:/projects/ml/data/imagenet_bbox`. Contact the author for permissions and access.

## Training

### Performance metrics

#### Target metrics

During evaluation we resize the image such that the minimum edge, and run inference using the 224 x 224 x 3 center crop. The top-1 single crop accuracy is 74.0% after 500K iterations.

#### Code

The accuracy is computed by the training script automatically. It can be read using TensorBoard as shown below.

![accuracy_validation_set](figures/accuracy3.png)

## Inference

#### Code
We provide a [notebook](inference.ipynb) that provides an example of how to run inference on sample images. 

#### Timing information
We measure the model latency using the inference notebook. The latency including preprocessing is 11ms with a batch size of 1. Note that the inference code doesn't run on a CPU because the channel ordering is NCHW and the max pooling operation only supports NHWC on a CPU device. 

#### Serialization 
Not applicable. The model was trained for research purposes and is not deployed to production.

## Miscellaneous

* Performance is 2\% below published results. We plan on running the training code from the TensorFlow models repository to determine whether there is a discrepancy in the code or in the training data
* Using 8 GPUs did not increase the throughput. It is worth determining the bottleneck in the data pipeline in order to further parallelize the code and decrease the training time. The Stanford DAWN Deep Learning [Benchmark](https://dawn.cs.stanford.edu/benchmark/) provides relevant pointers regarding state-of-the-art training times for ImageNet.
