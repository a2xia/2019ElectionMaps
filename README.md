# 2019ElectionMaps
Poll-by-Poll Results of Canadian Federal Ridings in preparation for the 2019 General Election

<p>This project is under an Apache 2.0 License. Please read the LICENSE file for more information.<br />
Hello! This is a Python script that does _ things:<br />
<ul>
	<li>Extract geometry information from a shape file</li>
	<li>Extract poll-by-poll results data from a CSV file</li>
	<li>Merge them together and write the results to a KML file</li>
</ul>
The purpose of this script is to easily create poll-by-poll Federal Election results from the 2015 Canadian Federal Election, for local campaigns to prepare for the next Federal election scheduled for 2019.</p>

<p>The data for this project can be obtained free-of-charge from Elections Canada (shapefiles and results data). The tools used for this project include QGIS to process the raw shapefile data. Python libraries used include simplekml (to write the kml files), shapefile (to open and read the shapefiles), and the standard csv and sys libraries.</p>

<p>Please note that this is still a work in progress, as the code still needs tweaks to be fully autonomous and ready for use for all Federal Ridings. For any questions, comments, or concerns, please email me at andrew.xia -at- uwaterloo.ca</p>

# How to Use
<p>Download the .py script into the same folder along with the .csv results file and the .shp shape file for your riding. (Please note that as of the current version, the .shp file needs to be filtered first through QGIS or a similar program.) Execute the script in the terminal with command [script name] [csv source name].</p>
