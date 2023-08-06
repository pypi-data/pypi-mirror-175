# Volume Segmantics User Interface

A GUI for the ['Volume Segmantics'](https://github.com/DiamondLightSource/volume-segmantics) segmentation toolkit.

This package provides an interactive web interface and API for training the PyTorch Segmentation models provided by Volume Segmantics and using these trained models to subsequently segment larger 3D datasets.<br>

The toolkit allows users with pre-labelled volumetric data to specialise models with pre-trained encoders.

## Requirements

A **linux** machine running CUDA enabled PyTorch.

## Installation 

The package must be populated with processes in the @/vsui/ap/processes directory as set out in the developer guide. The 'vsui' command can then be used to start the server. The web interface can be accessed by navigating to **localhost:8000** in a browser on the same machine.

## Usage

Output will be stored in the session working directory in folders with names corresponding to the task runs. The working directory can be set using the button on the right of the top navbar.<br>

Selecting *New Task* will open a popover with the defined processes. Selecting a process will open the settings pane. From here the required inputs can be set and the task started.<br>

A blue outline on the task pane indicates the task process is active. A grey outline indicates the process is inactive. When the process completes feedback will appear at the top of the task pane corresponding to the exit code of the process.<br>

A history of the tasks run this session will accumulate in the left navigation pane.