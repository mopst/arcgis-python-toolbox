## Version: 1.0.0
## Versioning approach based on Semantic Versioning https://semver.org/ with adaptions as suggested here: https://softwareengineering.stackexchange.com/questions/200002/semantic-versioning-for-desktop-applications/357887#357887
## i.e. MAJOR.MINOR.PATCH
## MAJOR major changes to interface / installation process
## MINOR new features, no new installation required
## PATCH bug-fixing


import arcpy, os
from arcpy.sa import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "MOPST Model"
        self.alias = "MOPSTModel"

        # List of tool classes associated with this toolbox
        self.tools = [MOPSTModel]


class MOPSTModel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "MOPST Model"
        self.description = "description (help file here)"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
		############
		# Land cover & sensitivity & seasonality section #
		############
		
		# 0th [0] parameter: Land Cover (Shapefile)
        landcover_shape = arcpy.Parameter(
            displayName="Land Cover (Shapefile)",
			name="landcover_shape",
			datatype="Feature Layer",
			parameterType="Required",
			direction="Input")
        landcover_shape.filter.list = ["Polygon"]
		
		# First [1] parameter: Land Cover Sensitivity (CSV File)
        landcover_sensitivity = arcpy.Parameter(  ##ideally need to update to CSV only
            displayName="Land Cover Sensitivity (CSV File)",
			name="landcover_sensitivity",
			datatype="GPTableView",
			parameterType="Required",
			direction="Input")
		
		# Second [2] parameter: Land Cover Sensitivity Score (Field/Column)
		## To select the column in the CSV file that contains the Land Cover Sensitivity Score
        landcover_sensitivity_field = arcpy.Parameter( ##ideally need to remove ActiveX control warning
			displayName="Land Cover Sensitivity Score (Field/Column)",
			name="landcover_sensitivity_field",
			datatype="Field",
			parameterType="Required",
			direction="Input")
		
		# set to pull field names from CSV file and supply to dropdown box
        landcover_sensitivity_field.parameterDependencies = [landcover_sensitivity.name]
		
		# Third [3] parameter: Seasonality File
        seasonality_score = arcpy.Parameter(  ##ideally need to update to CSV only
            displayName="Seasonality Score (CSV File)",
			name="seasonality_score",
			datatype="GPTableView",
			parameterType="Required",
			direction="Input")
			
		############
		# Opportunity, pressure and raster section #
		############
		
        # Forth [4] parameter: #used for extent when exporting raster data
        pressure_raster = arcpy.Parameter(
			displayName="Pressure Raster Layer",
			name="pressure_raster",
			datatype="GPRasterLayer",
			parameterType="Required",
			direction="Input")
			
		# Fifth [5] parameter
        opportunity_raster = arcpy.Parameter(
			displayName="Opportunity Raster Layer ",
			name="opportunity_raster",
			datatype="GPRasterLayer",
			parameterType="Required",
			direction="Input")

		# Sixth [6] parameter: Factor Weights (CSV File)
        factor_weights = arcpy.Parameter(  ##ideally need to update to CSV only
            displayName="Factor Weights (CSV File)",
			name="factor_weights",
			datatype="GPTableView",
			parameterType="Required",
			direction="Input")
			
        # Seven [7] parameter: Scenario Weights (CSV File)
        scenario_weights = arcpy.Parameter(  ##ideally need to update to CSV only
            displayName="Scenario Weights (CSV File)",
			name="scenario_weights",
			datatype="GPTableView",
			parameterType="Required",
			direction="Input")
			
		# Eighth [8] parameter
        factor_rasters = arcpy.Parameter(
			displayName="Factor Raster Layers",
			name="factor_rasters",
			datatype="GPRasterLayer",
			parameterType="Required",
			direction="Input",
			multiValue=True)
		
		#pass parameters into code execution
        params = [landcover_shape, landcover_sensitivity, landcover_sensitivity_field, seasonality_score, pressure_raster, opportunity_raster, factor_weights, scenario_weights, factor_rasters]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
		# Need Spatial Analyst license

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation.
		E.g. make sure all required layers defined. """
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
			
		##Set parameter values & print values
        messages.addMessage("\nParameter Values:")
		
        messages.addMessage(".Land cover & sensitivity & seasonality section")
		# Get Shapefile
        landcover_shape = parameters[0].valueAsText
        messages.addMessage("..Land Cover Shapefile: {0}".format(landcover_shape))
		# get CSV file
        landcover_sensitivity = parameters[1].valueAsText
        messages.addMessage("..Land Cover Sensitivity File: {0}".format(landcover_sensitivity))
		# get sensitivity field value
        landcover_sensitivity_field = parameters[2].valueAsText
        messages.addMessage("..Sensitivity Score Field/Column: {0}".format(landcover_sensitivity_field))
		# get seasonality score
        seasonality_score = parameters[3].valueAsText
        messages.addMessage("..Seasonality File: {0}".format(seasonality_score))

        messages.addMessage(".Opportunity, pressure and raster section")
		# get pressure raster layer
        pressure_raster = parameters[4].valueAsText
        messages.addMessage("..Pressure Raster Layer: {0}".format(pressure_raster))
		# get opportunity raster
        opportunity_raster = parameters[5].valueAsText
        messages.addMessage("..Opportunity Raster Layer: {0}".format(opportunity_raster))
		# get factor weights
        factor_weights = parameters[6].valueAsText
        messages.addMessage("..Factor Weights File: {0}".format(factor_weights))
		# get scenario weights
        scenario_weights = parameters[7].valueAsText
        messages.addMessage("..Scenario Weights File: {0}".format(scenario_weights))
		# get raster layers
        factor_rasters = parameters[8].valueAsText #returns full path if selected through browse, filename if not. 
        #print full details
		#messages.addMessage("..Factor Raster Layers: {0}".format(factor_rasters))
        #calculate and print how many are selected
        factors_split = factor_rasters.split(";")
        count = len(factors_split)
        messages.addMessage("..Number of Factor Raster Layers: {0}".format(count))
		
		
		############
		# Land cover & sensitivity & seasonality section #
		############
		
        messages.addMessage("\nLand cover & sensitivity & seasonality section")
		## Join CSV file to layer - land cover sensitivity
        messages.addMessage(".Starting process of joining sensitivity data")
		# see https://community.esri.com/t5/arcgis-pro-questions/arcpy-toolbox-import-csv-table-and-join-to/m-p/166242#M7504 and examples\join-example.txt for joining info. Have to use geodb. 
		#set geodb
        defaultGeoDb = arcpy.env.workspace
		#set to over write existing files
        arcpy.env.overwriteOutput = True
        messages.addMessage(".Converting CSV to Geodatabase table")
		#Convert the CSV file to a table - the new table will be saved in the geodatabase
        arcpy.TableToTable_conversion(landcover_sensitivity,defaultGeoDb,"landcover_sensitivity_CSV")
        sourceShp = parameters[0].valueAsText
        outputFeatureClass = "landcover_shapefile"
        arcpy.CopyFeatures_management(sourceShp,outputFeatureClass) #copy into geodatabase
        tempLayer = 'outputFeatureLayer' #somewhere to save the layer to
        arcpy.MakeFeatureLayer_management (outputFeatureClass, tempLayer) #create new layer
        messages.addMessage(".Performing Join")
		#perform the join landcover (tempLayer) and landcover_sensitivity_CSV (CSV file)
        newJoinLayer = arcpy.AddJoin_management(tempLayer, 'Main_habit', 'landcover_sensitivity_CSV', 'Habitat_environment_type', 'KEEP_ALL')
        # Copy the shapefile with join to a new permanent feature class in GDB - join will not be needed after
        arcpy.CopyFeatures_management(newJoinLayer, "LC_Sens_J")
        messages.addMessage(".Finished process of joining sensitivity data") #print message
        #messages.addMessage(newJoinLayer) #print joined layer name
		
		## Join seasonality data
        messages.addMessage("\n.Starting process of joining seasonality data") #print message
		#join seasonality_score (Habitat_environment_type) to LC_Sens_J (Habitat_environment_type)
        messages.addMessage(".Converting CSV to Geodatabase table")
		#Convert the CSV file to a table - the new table will be saved in the geodatabase
        arcpy.TableToTable_conversion(seasonality_score,defaultGeoDb,"seasonality_score_CSV")
        #messages.addMessage(seasonality_score) #print seasonality_score filename
        #sourceShp = "LC_Sens_J"
        #outputFeatureClass = "Landcover_Sensitivity_Joined_feature"
        #arcpy.CopyFeatures_management(sourceShp,outputFeatureClass) #copy into geodatabase
        #tempLayer2 = 'outputFeatureLayer' #somewhere to save the layer to
        #arcpy.MakeFeatureLayer_management ("LC_Sens_J", tempLayer2) #create new layer
        messages.addMessage(".Performing Join")
        tempLayer2 = 'outputFeatureLayer' #somewhere temp to save the layer into GBD
		# Create a feature layer from the vegtype featureclass
        arcpy.MakeFeatureLayer_management ("LC_Sens_J",  tempLayer2)	
		#used to have print info code here, see example-python-code.txt for details
		#perform the join landcover (tempLayer2) and seasonality_score_CSV (CSV file)
		#join field is landcover_sensitivity_CSV_Habitat_environment_type because name changed due to join
        newJoinLayer2 = arcpy.AddJoin_management(tempLayer2, 'landcover_sensitivity_CSV_Habitat_environment_type', 'seasonality_score_CSV', 'Habitat_environment_type', 'KEEP_ALL')
        # Copy the shapefile with join to a new permanent feature class in GDB - join will not be needed after
        arcpy.CopyFeatures_management(newJoinLayer2, "LC_Sens_Seas_J")
        messages.addMessage(".Finished process of joining seasonality data") #print message
        #messages.addMessage(newJoinLayer2) #print layer name

        ##extract winter and summer land cover data
        messages.addMessage("\n.Setting Extent for raster data conversion")
		#set extent of raster layer
        pressure_raster = parameters[4].valueAsText
        arcpy.env.extent = Raster(pressure_raster)
		#multiply out
		# save specified column (ND_North_Devon) as base_raster
        messages.addMessage(".Converting shape file to raster")
		#converting shapefile layer ("LC_Sens_Seas_J") to raster (ND_North_Devon) (landcover_sensitivity_field)
        #base file
        arcpy.conversion.FeatureToRaster("LC_Sens_Seas_J", landcover_sensitivity_field, "base_raster", "25")
        messages.addMessage(".Base raster conversion complete")
        #messages.addMessage("base_raster") #print "base_raster"
		# do specified column (ND_North_Devon) * winter, save as raster
        messages.addMessage(".Starting winter multiplication and conversion")
		# add field, see https://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/calculate-field.htm
        arcpy.AddField_management("LC_Sens_Seas_J", "winter_score", "DOUBLE", 18, 11)
		#work out field name
			#field prefix: LC_Sens_J_landcover_sensitivity_CSV_
			#variable containing field name: landcover_sensitivity_field
        landcover_sensitivity_field_name = ('LC_Sens_J_landcover_sensitivity_CSV_' + landcover_sensitivity_field)
		#complete calculation, including conversion to floating point number (from string/text)
        expression = "float(!" + landcover_sensitivity_field_name + "!) * !seasonality_score_CSV_Winter!"      
        arcpy.CalculateField_management("LC_Sens_Seas_J", "winter_score", expression, "PYTHON_9.3")
		#float is needed as ArcMap intreprets the sensitivity score as a string (so we need to convert to a float). 
		#This is based on the schema.ini file in the same folder (data) and may be able to be changed here. 
		#see https://gis.stackexchange.com/questions/45050/preparing-csv-files-for-use-in-arcgis-desktop for details
		#save as raster
        arcpy.conversion.FeatureToRaster("LC_Sens_Seas_J", "winter_score", "winter_landcover_raster", "25")
        messages.addMessage(".Finished winter multiplication and conversion")
        # messages.addMessage("winter_landcover_raster") #print winter_landcover_raster
		## summer conversion
        messages.addMessage(".Starting summer multiplication and conversion")
		# do specified column (ND_North_Devon) * summer, save as raster
        arcpy.AddField_management("LC_Sens_Seas_J", "summer_score", "DOUBLE", 18, 11)
		#complete calculation, including conversion to floating point number (from string/text)
        expression = "float(!" + landcover_sensitivity_field_name + "!) * !seasonality_score_CSV_Summer!"      
        arcpy.CalculateField_management("LC_Sens_Seas_J", "summer_score", expression, "PYTHON_9.3")
		#save as raster
        arcpy.conversion.FeatureToRaster("LC_Sens_Seas_J", "summer_score", "summer_landcover_raster", "25")
        messages.addMessage(".Finished summer multiplication and conversion")
        # messages.addMessage("summer_landcover_raster") #print summer_landcover_raster
		
        messages.addMessage(".Conversion complete")
        #messages.addMessage("\n")
		
		############
		# Opportunity, pressure and raster section #
		############
		
        messages.addMessage("\nOpportunity, pressure and raster section")
		#setup 'blank' rasters to add things to, baseline
        all_factors_pressure_raster_summer = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_summer = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_winter = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_winter = Raster(opportunity_raster) * 0
		#scenarios
        all_factors_pressure_raster_summer_profit = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_summer_profit = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_summer_business = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_summer_business = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_summer_custodianship = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_summer_custodianship = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_winter_profit = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_winter_profit = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_winter_business = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_winter_business = Raster(opportunity_raster) * 0
        all_factors_pressure_raster_winter_custodianship = Raster(pressure_raster) * 0
        all_factors_opportunity_raster_winter_custodianship = Raster(opportunity_raster) * 0
		#process factor rasters
        factor_rasters = parameters[8].valueAsText #returns full path if selected through browse, filename if not. 
		#split file path into separate objects (factors_split)
        factors_split = factor_rasters.split(";")
		# For each factor:
        arcpy.AddMessage(".Starting loop through each factor")
        i = 1 #counter
        for factor in factors_split:
			# factor contains an individual factor file path (e.g. "C:\..\data\factor-rasters\business-clusters-food-and-drink.tif"
            #messages.addMessage(factor) #print full file path
            try: #if it is a path, then cut out the file name
                factor_filename = factor.rsplit(os.sep, 1)[1]
				#extract filename, based on https://community.esri.com/t5/python-questions/parsing-list-object-file-paths-for-file-name/td-p/490526
				#using rsplit (right split), which takes out the file name, e.g. business-clusters-food-and-drink.tif
                #messages.addMessage("Split") #print message to show filename needs to be split from path
                #messages.addMessage(factor_filename) #print filename
            except: #if not, assume file name is good to go
                #messages.addMessage("Not Split") #print message to show split  is not needed
                factor_filename = factor
			#find value in factor-weights.csv
			# see https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-functions/searchcursor.htm
                #messages.addMessage(factor_filename) #print filename
            factor_filename = factor_filename.replace('\'','') #remove any stray ' from filename
            #messages.addMessage(factor_filename) #print filename
            cursor = arcpy.SearchCursor(factor_weights)
            field = "factor-file"
            #messages.addMessage(factor_filename) #print filename
            for row in cursor: #loop through each row in factor-weights.csv
                if row.getValue(field) == factor_filename: #if current row matches file we are looking at
				#multiply raster by factor weight and save 
				#baseline pressure_summer
                    factor_pressure_raster_summer = Raster("summer_landcover_raster") * row.getValue("pressure-weight")
                    #add to all factors variable
                    all_factors_pressure_raster_summer = all_factors_pressure_raster_summer + factor_pressure_raster_summer
                    #opportunity_summer
                    factor_opportunity_raster_summer = Raster("summer_landcover_raster") * row.getValue("opportunity-weight")
                    all_factors_opportunity_raster_summer = all_factors_opportunity_raster_summer + factor_opportunity_raster_summer       
				#baseline pressure_winter 
                    factor_pressure_raster_winter = Raster("winter_landcover_raster") * row.getValue("pressure-weight")
                    all_factors_pressure_raster_winter = all_factors_pressure_raster_winter + factor_pressure_raster_winter
                    #opportunity_winter
                    factor_opportunity_raster_winter = Raster("winter_landcover_raster") * row.getValue("opportunity-weight")
                    all_factors_opportunity_raster_winter = all_factors_opportunity_raster_winter + factor_opportunity_raster_winter       
				#baseline print message
                    messages.addMessage(".." + str(i) + "/" + str(count) + ": " + str(factor_filename) + "; P:" + str(row.getValue("pressure-weight")) + " O:" + str(row.getValue("opportunity-weight")))
				#scenario, opp summer
					#find value in scenario-weights.csv
                    cursor_scenario = arcpy.SearchCursor(scenario_weights)
                    field_scenario = "scenario"
                    field_factor = "factor-file"
                    for row in cursor_scenario: #loop through each row (scenario) in scenario-weights.csv
						#find matching factor (which we are already looking at)
                        if row.getValue(field_factor) == factor_filename: #factor we are already working
                            #multiply for each scenario
                            if row.getValue(field_scenario) == "Profit": #Profit scenario
                                arcpy.AddMessage("...Profit Scenario")
								##remember we need base weight as well as scenario weight
								#summer
                                factor_pressure_raster_summer_profit = factor_pressure_raster_summer * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_summer_profit = all_factors_pressure_raster_summer_profit + factor_pressure_raster_summer_profit
                                factor_opportunity_raster_summer_profit = factor_opportunity_raster_summer * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_summer_profit = all_factors_opportunity_raster_summer_profit + factor_opportunity_raster_summer_profit
                                #winter
                                factor_pressure_raster_winter_profit = factor_pressure_raster_winter * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_winter_profit = all_factors_pressure_raster_winter_profit + factor_pressure_raster_winter_profit
                                factor_opportunity_raster_winter_profit = factor_opportunity_raster_winter * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_winter_profit = all_factors_opportunity_raster_winter_profit + factor_opportunity_raster_winter_profit
                            if row.getValue(field_scenario) == "Business as usual": #Business as usual scenario
                                arcpy.AddMessage("...Business as usual Scenario")
								##remember we need base weight as well as scenario weight
                                #summer
                                factor_pressure_raster_summer_business = factor_pressure_raster_summer * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_summer_business = all_factors_pressure_raster_summer_business + factor_pressure_raster_summer_business
                                factor_opportunity_raster_summer_business = factor_opportunity_raster_summer * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_summer_business = all_factors_opportunity_raster_summer_business + factor_opportunity_raster_summer_business
								#winter
                                factor_pressure_raster_winter_business = factor_pressure_raster_winter * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_winter_business = all_factors_pressure_raster_winter_business + factor_pressure_raster_winter_business
                                factor_opportunity_raster_winter_business = factor_opportunity_raster_winter * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_winter_business = all_factors_opportunity_raster_winter_business + factor_opportunity_raster_winter_business
                            if row.getValue(field_scenario) == "Custodianship": #Custodianship scenario
                                arcpy.AddMessage("...Custodianship Scenario")
								##remember we need base weight as well as scenario weight
								#summer
                                factor_pressure_raster_summer_custodianship = factor_pressure_raster_summer * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_summer_custodianship = all_factors_pressure_raster_summer_custodianship + factor_pressure_raster_summer_custodianship
                                factor_opportunity_raster_summer_custodianship = factor_opportunity_raster_summer * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_summer_custodianship = all_factors_opportunity_raster_summer_custodianship + factor_opportunity_raster_summer_custodianship
								#winter
                                factor_pressure_raster_winter_custodianship = factor_pressure_raster_winter * row.getValue("pressure-multiplier") 
                                all_factors_pressure_raster_winter_custodianship = all_factors_pressure_raster_winter_custodianship + factor_pressure_raster_winter_custodianship
                                factor_opportunity_raster_winter_custodianship = factor_opportunity_raster_winter * row.getValue("opportunity-multiplier")
                                all_factors_opportunity_raster_winter_custodianship = all_factors_opportunity_raster_winter_custodianship + factor_opportunity_raster_winter_custodianship
                    i += 1 #move counter to next factor
        #end of for loop
		#save layers to geodatabase
        all_factors_pressure_raster_summer.save("baseline_pressure_raster_summer")
        all_factors_opportunity_raster_summer.save("baseline_opportunity_raster_summer")	
        all_factors_pressure_raster_winter.save("baseline_pressure_raster_winter") 
        all_factors_opportunity_raster_winter.save("baseline_opportunity_raster_winter") 
        messages.addMessage(".Opportunity and pressure, winter and summer baseline rasters saved")		

        all_factors_pressure_raster_summer_profit.save("profit_pressure_raster_summer")
        all_factors_opportunity_raster_summer_profit.save("profit_opportunity_raster_summer")
        all_factors_pressure_raster_winter_profit.save("profit_pressure_raster_winter")
        all_factors_opportunity_raster_winter_profit.save("profit_opportunity_raster_winter")

        all_factors_pressure_raster_summer_business.save("business_pressure_raster_summer")
        all_factors_opportunity_raster_summer_business.save("business_opportunity_raster_summer")
        all_factors_pressure_raster_winter_business.save("business_pressure_raster_winter")
        all_factors_opportunity_raster_winter_business.save("business_opportunity_raster_winter")
        
        all_factors_pressure_raster_summer_custodianship.save("custodianship_pressure_raster_summer")
        all_factors_opportunity_raster_summer_custodianship.save("custodianship_opportunity_raster_summer")
        all_factors_pressure_raster_winter_custodianship.save("custodianship_pressure_raster_winter")
        all_factors_opportunity_raster_winter_custodianship.save("custodianship_opportunity_raster_winter")
		
        messages.addMessage(".Scenario rasters saved")				
	
        return
