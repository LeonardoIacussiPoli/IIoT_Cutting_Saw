# IIoT Application on an Old Wood Cutting Saw
The general idea of this project is to use a mmachine learning algorithm installed on the STWIN board microprocessor by STMicroelectronics in order to understand when the machine is off, on or when the machine is cutting a wood table. The classification algorithm is based on the accelerometric data coming from the on board three axial accelerometer (ISM330DHCX).

![](images/system.png)

<br>

### Calculation of the cutting tool working time – why is it so important?

- Possible prediction of the tool wear
- Predictive maintenance (tool changing time)
- Analytics on machine usage
- Cutting process optimization 
- Energy consuption optimization



<br>

### Acquisition parameters

- Full Scale: **2g**
- Output Data Rate: **1666 Hz**

<br>
<br>
<br>


## Signal pre-processing

The raw signal has been processed in order to make the classification more robust and the signal pre-processing pipeline is represented in the following diagram. In order to find the correct labels, given the processed signal, an unsupervised clustering algorithm has been implemented.

![](images/pre_processing.png)


<br>
<br>
<br>

## Signal post-processing

![](images/post_processing.png)


<br>
<br>
<br>

## node-red interface

![](images/node_red.png)



<br>
<br>
<br>

## Graphical user interface

![](images/GUI.png)
