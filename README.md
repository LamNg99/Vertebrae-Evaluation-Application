<div align="center">

![Vertebral Scan](./icon/bone.png) 

# VertScan

</div>

## Overview

DXA scans are the standard for assessing the quality of a patient’s bone in terms of their BMD. However, CT scans are a more prevalent subset of medical imaging that do not have an established method through which a patient’s bone quality is evaluated through their BMD. This project’s main objective is to propose a software tool by which image processing techniques can be applied using Python in order to extract BMD information about a vertebrae bone sample from a CT scan. Along with developing the software, another objective was to segment multiple vertebrae from a CT scan and validate the information that the tool can provide by using finite element analysis (FEA) to perform a pedicle-screw pullout test across multiple vertebrae. The relationship between the BMD and CT scan could then be used to assess the tool’s capability. The software tool, VertScan, was successfully developed and is able to extract BMD values of the vertebrae. However, the FEA procedure was only completed for a single vertebrae due to issues in implementation of the design process, and as such, cannot definitively validate the capabilities of this software. The methodology by which FEA analysis can be conducted is included in the report, and may be replicated at a future time to determine the accuracy of a CT-based tool such as VertScan. At the current stage of this project, it is inconclusive as to how accurately the software tool can perform analysis of bone quality, and rather, the detailed methodologies by which a CT-based software application can be made for such a purpose are outlined in this report.

## Getting Started

### Prerequisites

Python 3.x

### Installing

Installing the requirements

```
pip install -r requirements.txt
```

### Running 

1. Clone the repo

```
git clone https://github.com/LamNg99/Vertebrae-Evaluation-Application.git
```

2. Run `python3 app.py`

## Demo Video

[![VertScan Demo](https://img.youtube.com/vi/PU7ogfivMOU/0.jpg)](https://youtu.be/PU7ogfivMOU)


## Acknowledgments
- [bone.png](https://github.com/LamNg99/Vertebrae-Evalution-Application/blob/main/icon/bone.png) under "Flaticon license" downloaded from [flaticon](https://www.flaticon.com/free-icon/bone_753151?term=bone+serach&related_id=753151) 
- 3D volumn reconstruction modified from [Howard Chen's Post](https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/)

