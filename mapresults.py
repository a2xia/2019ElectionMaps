# Elections 2015 Map Creator
# v.0.5 by Andrew Xia [andrew.xia -at- uwaterloo.ca]

# Note: To run in Powershell: navigate to C:\Python35 and enter
	# [Environment]::SetEnvironmentVariable("Path",$env:Path;C:\Python35", "User")
	# then restart Powershell for changes to take effect

# Usage: Navigate to C:\Python35\files
	# > python simplecsvtest.py results.csv

# Import required libraries
import csv
import sys
import simplekml
import shapefile
import operator

# Open csv file containing poll-by-poll results
# sys.argv[1] takes the file name from the command prompt
file = open(sys.argv[1], 'rt')

try:
	print("...Opening CSV file...")
	reader = csv.reader(file, delimiter=',')

	# Allocate memory for data arrays
	print("...Allocating memory for data arrays...")
	poll = []
	cpc = []
	ndp = []
	lpc = []
	gpc = []
	other = []
	total = []
	electors = []
	share = []
	turnout = []
	quintile = []


	# Read csv data and store into arrays
	print("...Reading and storing csv data...")
	for row in reader:
		pollr = row[0]
		cpcr  = row[1]
		ndpr  = row[2]
		lpcr  = row[3]
		gpcr  = row[4]
		otherr = row[5]
		totalr = row[6]
		electorsr = row[7]
		sharer = row[8]
		turnoutr = row[9]
		quintiler = row[10]

		# Attach imported data to lists
		poll.append(pollr)
		cpc.append(cpcr)
		ndp.append(ndpr)
		lpc.append(lpcr)
		gpc.append(gpcr)
		other.append(otherr)
		total.append(totalr)
		electors.append(electorsr)
		share.append(sharer)
		turnout.append(turnoutr)
		quintile.append(quintiler)

finally:
	# Close the CSV file
	file.close()
	print("...Closing csv file...")

# Open the shapefile containing poll boundaries
sf = shapefile.Reader("nwb")
print("...shape file opened...")

# Reading field information from shapefile
fields = sf.fields
print("...importing field information from shape file...")

# Reading shapeRecords information
	# This function imports both the polygons and its attached database fields
pollRecs = sf.shapeRecords()

# Reverse polygon point order (see note 1)
for i in range(len(pollRecs)):
	pollRecs[i].shape.points.reverse()

# Sort shapefile data into ascending poll order to match csv data
pollRecs.sort(key=lambda x: int(x.record[15]), reverse=False)
print("...sorting shapefile data...")

# Convert quartile 'string' to 'int' for if-statements
for i in range(1, len(quintile)):
	quintile[i] = int(quintile[i])

# Instantiate KML writer
kml = simplekml.Kml()
print("...simplekml object instantiated...")

# Create KML entity for each poll
# See Note 2 regarding colors
for i in range(len(pollRecs)):
	polypol = kml.newpolygon(name=pollRecs[i].record[15], outerboundaryis = pollRecs[i].shape.points)
	polypol.style.linestyle.color = simplekml.Color.orange
	polypol.style.linestyle.width = 2
	# Note: simplekml does not seem to support if-elif-else structures
	if quintile[i+1] == 1:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.darkorange)
	if quintile[i+1] == 2:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.orange)
	if quintile[i+1] == 3:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.orangered)
	if quintile[i+1] == 4:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.deepskyblue)
	if quintile[i+1] == 5:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.darkslateblue)
	if quintile[i+1] == 6:
		polypol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.gray)
		print("Call %d" % i)
	schema = kml.newschema(name='pollData')
	schema.newsimplefield(name='NDP', type='int', displayname='NDP')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('NDP', ndp[i+1])
	schema.newsimplefield(name='Liberal', type='int', displayname='Liberal')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Liberal', lpc[i+1])
	schema.newsimplefield(name='Conservative', type='int', displayname='Conservative')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Conservative', cpc[i+1])
	schema.newsimplefield(name='Green', type='int', displayname='Green')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Green', gpc[i+1])
	schema.newsimplefield(name='Other', type='int', displayname='Other')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Other', other[i+1])
	schema.newsimplefield(name='Total Votes', type='int', displayname='Total Votes')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Total Votes', total[i+1])
	schema.newsimplefield(name='Percent NDP', type='string', displayname='Percent NDP')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Percent NDP', share[i+1])
	schema.newsimplefield(name='Turnout', type='string', displayname='Turnout')
	polypol.extendeddata.schemadata.schemaurl = schema.id
	polypol.extendeddata.schemadata.newsimpledata('Turnout', turnout[i+1])

# Save the KML file
kml.save("resultsmap.kml")

# Note 1: The coordinate order in the polygons of the shape file provided by
		# Elections Canada goes counter-clockwise. In order for the polygons
		# to be displayed properly on Google Maps, they need to be in clock-
		# wise order, hence a reverse function call is needed.

# Note 2: KML coloring does not use standard HTML hexadecimal color codes, 
		# instead it uses KML color (ref: www.zonums.com/gmaps/kml_color/)
		# whereby the hex value goes aa-rr-gg-bb (alpha, red, green, blue)