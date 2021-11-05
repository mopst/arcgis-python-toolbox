## Demonstration Files

The [`demo.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/demo.zip) file contains some example files to show how the tool works. You can use these files to verify if the Toolbox is working properly on your machine. 

### Requirements

This needs ArcMap 10.5 or greater to run, with the Spatial Analyst extension. *It will not work on ArcGIS Pro.*

This has been tested on ArcMap 10.5 and should work on later versions of ArcMap (it has also been tested on 10.8.1). It may also work on earlier versions of ArcMap (10.x) but this has not been tested. *Please let us know if it works for you*. Basic, Standard and Advanced licenses should all work. 

### Video

This video shows how to use the tool and the demo files. Step-by-step instructions are below. 

[![]()](https://www.youtube.com/watch?v=VID)

### Step by step instructions

- Download the [MOPST Python Toolbox](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/MOPST-ArcGIS-Python-Toolbox.pyt). Save this somewhere on your machine you can find it (e.g. Downloads). 

- Download the [`demo.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/demo.zip) file and extract it. This contains all the files you need to run the Toolbox. 

- Open the `demo.mxd` file in ArcMap. 

- Set the Default Geodatabase (**File > Map Document Properties**). This is where the output files will be saved. 

- Use the **Catalog** tab to have a look at the files provided. 

- Use the **Connect To Folder** button to connect to the folder where you downloaded the files. 

The input files (from `demo.zip`) are:

Name (Format) | Example Filename | Description
-- | -- | -- 
Land Cover (Shapefile) | *brighton-lewes-down-land-cover.shp* | Shapefile of the different land cover types. 
Land Cover Sensitivity (CSV File) | *land-cover-sensitivity.csv* | Sensitivity score for each land cover type.
Seasonality Score (CSV File) | seasonality.csv | Contains information on which land cover types are more sensitive in summer or winter. 
Pressure Raster Layer (Raster TIF) | *bldbr-pressures-merged.tif* | Identify the stakeholder identification of areas of tourism pressure. 
Opportunity Raster Layer (Raster TIF) | *bldbr-opportunity-merged.tif* | identify the stakeholder identification of areas of tourism opportunity. 
Factor Weights (CSV File) | *seasonality.csv* | Lists all of the Factor Raster Layers and the weights given to them for Pressure and Opportunity.
Scenario Weights (CSV File) | *scenario-weights.csv* | lists the three scenarios (Profit, Business as usual, Custodianship) and their weights. 
Factor Raster Layers (Raster TIF) | *factor-rasters* | show the presence (**1**) or absence (**0**) of a range of factors. 

The `factor-rasters` folder contains 9 example factors. These are all created using open source data and therefore are free to distribute. © OpenStreetMap contributors. 

- Open **MOPST-ArcGIS-Python-Toolbox.pyt** and double click **MOPST Model**. 

- Set the input files, the toolbox should look like this:

!()[demo-MOPST-tool-inputs.png]

- Click **OK** to run the model.

- Wait for model to run *(it will take about 5 minutes or so)*. 

These data took 5 minutes 5 seconds to run on my machine. Your computer might be quicker or slower, but it should be around this figure. 
 

- Check the output log *(it should look like the sample log `example-output-log.txt` in `demo.zip`)*. 

- Look at model outputs in the default geodatabase *(they should look like the sample files in [`output-geodatabase.gdb.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/output-geodatabase.gdb.zip))*. 

Outputs are listed in `output-geodatabase`, there should be 24 layers (see [README](readme.md) for details of the files). 

- Adjust the weights and re-run the model to see how the output varies.
