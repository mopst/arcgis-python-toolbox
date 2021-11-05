# MOPST ArcGIS Python Toolbox

Version of the MOPST (Mapping Opportunity & Pressures for Sustainable Tourism) tool for ArcGIS, running as a Python Toolbox. 
 
 
## Requirements

This needs **ArcMap 10.5** or greater to run, with the **Spatial Analyst extension**. *It will not work on ArcGIS Pro.*

This has been tested on ArcMap 10.5 and should work on later versions of ArcMap (it has also been tested on 10.8.1). It may also work on earlier versions of ArcMap (10.x) but this has not been tested. *Please let us know if it works for you*. Basic, Standard and Advanced licenses should all work. 
 
  
## Quick Setup & Demo Data

There is some demonstration data so you can test out the Toolbox on your computer. 

- Download the [MOPST Python Toolbox](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/MOPST-ArcGIS-Python-Toolbox.pyt). Save this somewhere on your machine you can find it (e.g. Downloads). 
- Download the [`demo.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/demo.zip) file and extract it. This contains all the files you need to run the Toolbox. 
- Open the `demo.mxd` file. 
- Set the Default Geodatabase (File > Map Document Properties). 
- Open the **Catalog** tab. 
- **Connect To Folder** to the folder you downloaded the files. 
- Open **MOPST-ArcGIS-Python-Toolbox.pyt** and double click **MOPST Model**. 
- Set the input files, [like this image](demo-MOPST-tool-inputs.png). 
- Click **OK** to run the model.
- Wait for model to run (about 5 minutes or so). 
- Check output log (sample in `demo.zip`). 
- Look at model outputs in the default geodatabase (sample in [`output-geodatabase.gdb.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/output-geodatabase.gdb.zip)). 

For more details, please look at the [Demonstration Files](demo.md) page. 
 
 
## Useful Information

This script makes use of the Default File Geodatabase in ArcMap to save working files and outputs. This is usually in C:\Users\<username>\Documents\ArcGIS\Default.gdb. You can adjust this when opening a new Map Document, or via File > Map Document Properties > Default Geodatabase. 

It is helpful if all the layers needed for the tool (apart from raster factors) are added to the Map Document before running the script. 
  
  
## Input File Specification

This toolbox makes use of a range of input files. The files in (demo) are in this required format. The requirements are summarised below. See [input-file-specification](input-file-specification.md) for more details. 

- All files must cover the same geographic areas
- All files must be in the same coordinate system 

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
  
 
## Output Files:

The exported files (total number = 24) are stored in the default Geodatabase (usually in C:\Users\<username>\Documents\ArcGIS\Default.gdb). They are:

Filename | Output or working file? | Description
-- | -- | --
base_raster | Working file | 
baseline_opportunity_raster_summer | Working file | 
baseline_opportunity_raster_winter | Working file | 
baseline_pressure_raster_summer | Working file | 
baseline_pressure_raster_winter | Working file | 
business_opportunity_raster_summer | Output file | Summer Opportunity file for business scenario
business_opportunity_raster_winter | Output file | Winter Opportunity file for business scenario
business_pressure_raster_summer | Output file | Summer Pressure file for business scenario
business_pressure_raster_winter | Output file | Winter Pressure file for business scenario
custodianship_opportunity_raster_summer | Output file | Summer Opportunity file for custodianship scenario
custodianship_opportunity_raster_winter | Output file | Winter Opportunity file for custodianship scenario
custodianship_pressure_raster_summer | Output file | Summer Pressure file for custodianship scenario
custodianship_pressure_raster_winter | Output file | Winter Pressure file for custodianship scenario
landcover_sensitivity_CSV | Working file | 
landcover_shapefile | Working file | 
LC_Sens_J | Working file | 
LC_Sens_Seas_J | Working file | 
profit_opportunity_raster_summer | Output file | Summer Opportunity file for profit scenario
profit_opportunity_raster_winter | Output file | Winter Opportunity file for profit scenario
profit_pressure_raster_summer | Output file | Summer Pressure file for profit scenario
profit_pressure_raster_winter | Output file | Winter Pressure file for profit scenario
seasonality_score_CSV | Working file | 
summer_landcover_raster | Working file | 
winter_landcover_raster | Working file | 

They are available in [`output-geodatabase.gdb.zip`](https://github.com/mopst/arcgis-python-toolbox/releases/download/v1.0.0/output-geodatabase.gdb.zip). 
 

## Comments / Feedback

Please do let me know if you have any comments / feedback, via email: [nick@geospatialtrainingsolutions.co.uk](mailto:nick@geospatialtrainingsolutions.co.uk), or please submit a Pull Request on GitHub. 
 
 