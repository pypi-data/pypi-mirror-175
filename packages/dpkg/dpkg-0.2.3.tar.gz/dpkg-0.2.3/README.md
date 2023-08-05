
# dpkg

dpkg is a package that collects functions frequently used in healthcare analysis.

## install
```
pip install dpkg
```


# apk

Computes the average precision at k. This function computes the average prescision at k between two lists of items.

Parameters
* actual : list
> A list of elements that are to be predicted (order doesn't matter)
* predicted : list
> A list of predicted elements (order does matter)
* k : int, optional
> The maximum number of predicted elements

Returns
* score : double The average precision at k over the input lists

Simple example
```python
from dpkg.apk import ApkScore

ApkScore(actual, predicted, k)
```


# mapk

Mean Average Precision (mAP) is commonly used to analyze the performance of object detection and segmentation systems. 

Parameters
* apk_list : list
> A list of apk scores

Returns
* score : Mean average precision score of input apk lists

Simple example
```python
from dpkg.mapk import MapkScore

MapkScore(apk_list)
```


# dataset

Dataset is a package that loads data sets related to food, bio, and healthcare.

Dataset
* khane : Korean Health and Nutrition Survey dataset(2016)
> * main : main dataset including meta information
> * ffq : food frequency questionnaires dataset including meta information
> * 24rc : dietary assessment by 24-hour dataset including meta information
> * oe : oral examination dataset including meta information

Parameters
* khane dataset
> data type : 'main', 'ffq', '24rc', 'oe'

Simple example
```python
from dpkg.dataset import Khane

main_ds, main_meta = Khane().load_data('main')
```