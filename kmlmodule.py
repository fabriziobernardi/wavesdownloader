# #################################################
# 
# Description: set of functions for creating kml files in Python
#
# Copyright (c) 2010 - 2011 Konstantin Filimoennkov <kfilimonenkov@gmail.com>
#
# #################################################


from xml.dom import minidom, Node 

###################################################
## KML element
###################################################
def createKMLElement(kmlDoc):
    kmlElement = kmlDoc.createElement("kml")
    kmlElement.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
    kmlElement.setAttribute("xmlns:gx", "http://www.google.com/kml/ext/2.2")
    kmlElement = kmlDoc.appendChild(kmlElement)
    
    return kmlElement

###################################################
## Folder element
###################################################
def createFolderElement(kmlDoc,  id="",  name="New Folder",  description="New Description", open=0):
    folderElement = kmlDoc.createElement("Folder")
    # id
    if id is not "":
        folderElement.setAttribute("id",  id)
    # name
    nameElement = kmlDoc.createElement("name")
    nameText = kmlDoc.createTextNode(name)
    nameElement.appendChild(nameText)
    folderElement.appendChild(nameElement)
    # description
    descriptionElement = kmlDoc.createElement("description")
    descriptionCDATASection = kmlDoc.createCDATASection(description)
    descriptionElement.appendChild(descriptionCDATASection)
    folderElement.appendChild(descriptionElement)
    # open
    openElement = kmlDoc.createElement("open")
    openText = kmlDoc.createTextNode(str(open))
    openElement.appendChild(openText)
    folderElement.appendChild(openElement)
    
    return folderElement
    
###################################################
## Document element
###################################################
def createDocumentElement(kmlDoc,  id="",  name="New Document",  description="New Description",  open=0):
    documentElement = kmlDoc.createElement("Document")
    # id
    if id is not "":
        documentElement.setAttribute("id",  id)
    # name
    nameElement = kmlDoc.createElement("name")
    nameText = kmlDoc.createTextNode(name)
    nameElement.appendChild(nameText)
    documentElement.appendChild(nameElement)
    # description
    descriptionElement = kmlDoc.createElement("description")
    descriptionCDATASection = kmlDoc.createCDATASection(description)
    descriptionElement.appendChild(descriptionCDATASection)
    documentElement.appendChild(descriptionElement)
    # open
    openElement = kmlDoc.createElement("open")
    openText = kmlDoc.createTextNode(str(open))
    openElement.appendChild(openText)
    documentElement.appendChild(openElement)
    
    return documentElement
    
###################################################
## Document Internal  element
###################################################
def createDocumentInternalElement(kmlDoc,  targetId=""):
    documentElement = kmlDoc.createElement("Document")
    documentElement.setAttribute("targetId",  targetId)
    
    return documentElement
    
###################################################
## Placemark element
###################################################    
def createPlacemarkElement(kmlDoc,  id="",  name="New Name",  description="New Description"):
    placemarkElement = kmlDoc.createElement("Placemark")        
    #comment = kmlDoc.createComment("This is my comment")    
    #placemarkElement.appendChild(comment)
    # id
    if id is not "":
        placemarkElement.setAttribute("id",  id)
    # name
    nameElement = kmlDoc.createElement("name")
    nameText = kmlDoc.createTextNode(name)
    nameElement.appendChild(nameText)
    placemarkElement.appendChild(nameElement)
     # description
    descriptionElement = kmlDoc.createElement("description")
    #descriptionText = kmlDoc.createTextNode(description)
    descriptionCDATASection = kmlDoc.createCDATASection(description)
    descriptionElement.appendChild(descriptionCDATASection)
    placemarkElement.appendChild(descriptionElement)
    
    return placemarkElement

###################################################
## LookAt element
###################################################    
def createLookAtElement(kmlDoc,
                        id = "", 
                        longitude=0, 
                        latitude=0,  
                        altitude=0,  
                        range = 0,  
                        tilt=0,  
                        heading=0,  
                        altitudeMode="clampToGround"):

    lookAtElement = kmlDoc.createElement("LookAt")
    # id
    if id is not "":
        lookAtElement.setAttribute("id",  id)
    # longitude
    longituteElement = kmlDoc.createElement("longitude")
    textNode = kmlDoc.createTextNode(str(longitude))
    longituteElement.appendChild(textNode)
    lookAtElement.appendChild(longituteElement)
    # latitude
    latitudeElement = kmlDoc.createElement("latitude")
    textNode = kmlDoc.createTextNode(str(latitude))
    latitudeElement.appendChild(textNode)
    lookAtElement.appendChild(latitudeElement)
    # altitude
    altitudeElement = kmlDoc.createElement("altitude")
    textNode = kmlDoc.createTextNode(str(altitude))
    altitudeElement.appendChild(textNode)
    lookAtElement.appendChild(altitudeElement)
    # range
    rangeElement = kmlDoc.createElement("range")
    textNode = kmlDoc.createTextNode(str(range))
    rangeElement.appendChild(textNode)
    lookAtElement.appendChild(rangeElement)
    # tilt
    tiltElement = kmlDoc.createElement("tilt")
    textNode = kmlDoc.createTextNode(str(tilt))
    tiltElement.appendChild(textNode)
    lookAtElement.appendChild(tiltElement)
    # heading
    headingElement = kmlDoc.createElement("heading")
    textNode = kmlDoc.createTextNode(str(heading))
    headingElement.appendChild(textNode)
    lookAtElement.appendChild(headingElement)
    # altitudeMode
    altitudeModeElement = kmlDoc.createElement("altitudeMode")
    textNode = kmlDoc.createTextNode(altitudeMode)
    altitudeModeElement.appendChild(textNode)
    lookAtElement.appendChild(altitudeModeElement)
    
    return lookAtElement
    
###################################################
## LookAt element with time stamp
###################################################    
def createLookAtElementTime(kmlDoc,
                        id = "", 
                        dataTime = "", 
                        longitude=0, 
                        latitude=0,  
                        altitude=0,  
                        range = 0,  
                        tilt=0,  
                        heading=0,  
                        altitudeMode="clampToGround"):

    lookAtElement = kmlDoc.createElement("LookAt")
    # id
    if id is not "":
        lookAtElement.setAttribute("id",  id)
    #timeStamp
    gxTimeStampElement = createGxTimeStampElement(kmlDoc,  dataTime)
    lookAtElement.appendChild(gxTimeStampElement)
    # longitude
    longituteElement = kmlDoc.createElement("longitude")
    textNode = kmlDoc.createTextNode(str(longitude))
    longituteElement.appendChild(textNode)
    lookAtElement.appendChild(longituteElement)
    # latitude
    latitudeElement = kmlDoc.createElement("latitude")
    textNode = kmlDoc.createTextNode(str(latitude))
    latitudeElement.appendChild(textNode)
    lookAtElement.appendChild(latitudeElement)
    # altitude
    altitudeElement = kmlDoc.createElement("altitude")
    textNode = kmlDoc.createTextNode(str(altitude))
    altitudeElement.appendChild(textNode)
    lookAtElement.appendChild(altitudeElement)
    # range
    rangeElement = kmlDoc.createElement("range")
    textNode = kmlDoc.createTextNode(str(range))
    rangeElement.appendChild(textNode)
    lookAtElement.appendChild(rangeElement)
    # tilt
    tiltElement = kmlDoc.createElement("tilt")
    textNode = kmlDoc.createTextNode(str(tilt))
    tiltElement.appendChild(textNode)
    lookAtElement.appendChild(tiltElement)
    # heading
    headingElement = kmlDoc.createElement("heading")
    textNode = kmlDoc.createTextNode(str(heading))
    headingElement.appendChild(textNode)
    lookAtElement.appendChild(headingElement)
    # altitudeMode
    altitudeModeElement = kmlDoc.createElement("altitudeMode")
    textNode = kmlDoc.createTextNode(altitudeMode)
    altitudeModeElement.appendChild(textNode)
    lookAtElement.appendChild(altitudeModeElement)
    
    return lookAtElement

###################################################
## Point element
###################################################    
def createPointElement(kmlDoc,  
                       id="",  
                       extrude=0,  
                       altitudeMode="clampToGround", 
                       coordinates =[[0,  0,  0]]):
    pointElement = kmlDoc.createElement("Point")
#   # id
#   if id is not "":
#       pointElement.setAttribute("id",  id)
#   # extrude
#   extrudeElement = kmlDoc.createElement("extrude")
#   textNode = kmlDoc.createTextNode(str(extrude))
#   extrudeElement.appendChild(textNode)
#   pointElement.appendChild(extrudeElement)
#   # altitudeMode
#   altitudeModeElement = kmlDoc.createElement("altitudeMode")
#   textNode = kmlDoc.createTextNode(altitudeMode)
#   altitudeModeElement.appendChild(textNode)
#   pointElement.appendChild(altitudeModeElement)
#   # coordinates
    coordinatesElement = createCoordiantesElement(kmlDoc,  coordinates) 
    pointElement.appendChild(coordinatesElement)
    
    return pointElement

###################################################
## LineString element
###################################################    
def createLineStringElement(kmlDoc,  id="",  extrude=0,  tessellate=0,  altitudeMode="clampToGround",  coordinates=[[0,  0,  0],  [10, 10,  0]]):
    lineStringElement = kmlDoc.createElement("LineString")
    # id
    if id is not "":
        lineStringElement.setAttribute("id",  id)
    # extrude
    extrudeElement = kmlDoc.createElement("extrude")
    textNode = kmlDoc.createTextNode(str(extrude))
    extrudeElement.appendChild(textNode)
    lineStringElement.appendChild(extrudeElement)
    # tessellate
    tessellateElement = kmlDoc.createElement("tessellate")
    textNode = kmlDoc.createTextNode(str(tessellate))
    tessellateElement.appendChild(textNode)
    lineStringElement.appendChild(tessellateElement)
    # altitudeMode
    altitudeModeElement = kmlDoc.createElement("altitudeMode")
    textNode = kmlDoc.createTextNode(altitudeMode)
    altitudeModeElement.appendChild(textNode)
    lineStringElement.appendChild(altitudeModeElement)
    # coordinates
    coordinatesElement = createCoordiantesElement(kmlDoc,  coordinates) 
    lineStringElement.appendChild(coordinatesElement)
    
    return lineStringElement

###################################################
## LinearRing element
###################################################    
def createLinearRingElement(kmlDoc,  
                            id="",  
                            extrude=0,  
                            tessellate=0,  
                            altitudeMode="clampToGround",  
                            coordinates=[[0,  0,  0],  [10, 10,  0]]):
    linearRingElement = kmlDoc.createElement("LinearRing")
    # id
    if id is not "":
        lineStringElement.setAttribute("id",  id)
    # extrude
    extrudeElement = kmlDoc.createElement("extrude")
    textNode = kmlDoc.createTextNode(str(extrude))
    extrudeElement.appendChild(textNode)
    linearRingElement.appendChild(extrudeElement)
    # tessellate
    tessellateElement = kmlDoc.createElement("tessellate")
    textNode = kmlDoc.createTextNode(str(tessellate))
    tessellateElement.appendChild(textNode)
    linearRingElement.appendChild(tessellateElement)
    # altitudeMode
    altitudeModeElement = kmlDoc.createElement("altitudeMode")
    textNode = kmlDoc.createTextNode(altitudeMode)
    altitudeModeElement.appendChild(textNode)
    linearRingElement.appendChild(altitudeModeElement)
    # coordinates
    
    #############################################
    # to make it closed ring
    firstCoord = coordinates[0]
    lastCoord = coordinates[len(coordinates)-1]
    if (firstCoord != lastCoord):
    	coordinates.append(firstCoord)
	#############################################    	
	
    coordinatesElement = createCoordiantesElement(kmlDoc,  coordinates) 
    linearRingElement.appendChild(coordinatesElement)
    
    return linearRingElement
    
###################################################
## Polygon element
###################################################    
def createPolygonElement(kmlDoc,  
                            id="",  
                            extrude=0,  
                            tessellate=0,  
                            altitudeMode="clampToGround",  
                            outer = 1, 
                            coordinatesOuter=[[0,  0,  0],  [10, 10,  0]], 
                            inner = 1, 
                            coordinatesInner=[[0,  0,  0],  [10, 10,  0]]):
    polygonElement = kmlDoc.createElement("Polygon")
    if id is not "":
        polygonElement.setAttribute("id",  id)
    # extrude
    extrudeElement = kmlDoc.createElement("extrude")
    textNode = kmlDoc.createTextNode(str(extrude))
    extrudeElement.appendChild(textNode)
    polygonElement.appendChild(extrudeElement)
    # tessellate
    tessellateElement = kmlDoc.createElement("tessellate")
    textNode = kmlDoc.createTextNode(str(tessellate))
    tessellateElement.appendChild(textNode)
    polygonElement.appendChild(tessellateElement)
    # altitudeMode
    altitudeModeElement = kmlDoc.createElement("altitudeMode")
    textNode = kmlDoc.createTextNode(altitudeMode)
    altitudeModeElement.appendChild(textNode)
    polygonElement.appendChild(altitudeModeElement)
    if outer == 1:
        outerBoundaryIsElement = kmlDoc.createElement("outerBoundaryIs")
        linearRingElement = kmlDoc.createElement("LinearRing")
        coordinatesElement = createCoordiantesElement(kmlDoc,  coordinatesOuter)
        linearRingElement.appendChild(coordinatesElement)
        outerBoundaryIsElement.appendChild(linearRingElement)
        polygonElement.appendChild(outerBoundaryIsElement)
    if inner == 1:
        innerBoundaryIsElement = kmlDoc.createElement("innerBoundaryIs")
        linearRingElement = kmlDoc.createElement("LinearRing")
        coordinatesElement = createCoordiantesElement(kmlDoc,  coordinatesInner)
        linearRingElement.appendChild(coordinatesElement)
        innerBoundaryIsElement.appendChild(linearRingElement)
        polygonElement.appendChild(innerBoundaryIsElement)
    
    return polygonElement



###################################################
## coordinates element
###################################################    
def createCoordiantesElement(kmlDoc,  coordinates=[[0,  0,  0]]):
    coordinatesElement = kmlDoc.createElement("coordinates")
    #print len(coordinates)
    for i in xrange(len(coordinates)):
        coordStr=""
        for j in range(3):
            #print coordinates[i][j]
            coordStr += str(coordinates[i][j])
            if j is not 2:
                coordStr += ","
            else:
                coordStr += " "
        textNode = kmlDoc.createTextNode(coordStr)
        coordinatesElement.appendChild(textNode)
    
    return coordinatesElement

###################################################
## TimeStamp element
###################################################    
def createTimeStampElement(kmlDoc, timeData):
    timeStampElement = kmlDoc.createElement("TimeStamp")
    whenElement = kmlDoc.createElement("when")
    textNode = kmlDoc.createTextNode(timeData)
    whenElement.appendChild(textNode)
    timeStampElement.appendChild(whenElement)
    
    return timeStampElement
    
###################################################
## TimeSpan element
###################################################    
def createTimeSpanElement(kmlDoc, begin,  end):
    timeSpanElement = kmlDoc.createElement("TimeSpan")
    # begin
    beginElement = kmlDoc.createElement("begin")
    textNode = kmlDoc.createTextNode(begin)
    beginElement.appendChild(textNode)
    timeSpanElement.appendChild(beginElement)
    # end
    endElement = kmlDoc.createElement("end")
    textNode = kmlDoc.createTextNode(end)
    endElement.appendChild(textNode)
    timeSpanElement.appendChild(endElement)
    
    return timeSpanElement
    
###################################################
## Update element
###################################################    
def createUpdateElement(kmlDoc, href):
    updateElement = kmlDoc.createElement("Update")
    targetHrefElement = kmlDoc.createElement("targetHref")
    textNode = kmlDoc.createTextNode(href)
    targetHrefElement.appendChild(textNode)
    updateElement.appendChild(targetHrefElement)
    
    return updateElement

###################################################
## Create element
###################################################    
def createCreateElement(kmlDoc):
    createElement = kmlDoc.createElement("Create")
    
    return createElement


###################################################
##
##
##                      gx: ELEMENTS
##                  
##
###################################################

    
###################################################
## gxTimeStamp element
###################################################    
def createGxTimeStampElement(kmlDoc, timeData):
    timeStampElement = kmlDoc.createElement("gx:TimeStamp")
    whenElement = kmlDoc.createElement("when")
    textNode = kmlDoc.createTextNode(timeData)
    whenElement.appendChild(textNode)
    timeStampElement.appendChild(whenElement)
    
    return timeStampElement

###################################################
## gxTour element
###################################################    
def createGxTourElement(kmlDoc, name,  description):
    gxTourElement = kmlDoc.createElement("gx:Tour")
    #name
    nameElement = kmlDoc.createElement("name")
    textNode = kmlDoc.createTextNode(name)
    nameElement.appendChild(textNode)
    gxTourElement.appendChild(nameElement)
    #description
    descriptionElement = kmlDoc.createElement("description")
    textNode = kmlDoc.createTextNode(description)
    descriptionElement.appendChild(textNode)
    gxTourElement.appendChild(descriptionElement)
    
    return gxTourElement

###################################################
## gxPlaylist element
###################################################    
def createGxPlaylistElement(kmlDoc):
    #gxPlaylist
    gxPlaylistElement = kmlDoc.createElement("gx:Playlist")
    
    return gxPlaylistElement
    
###################################################
## gxAnimatedUpdate element
###################################################    
def createGxAnimatedUpdateElement(kmlDoc,  duration):
    gxAnimatedUpdatetElement = kmlDoc.createElement("gx:AnimatedUpdate")
    gxDurationElement = kmlDoc.createElement("gx:duration")
    textNode = kmlDoc.createTextNode(str(duration))
    gxDurationElement.appendChild(textNode)
    gxAnimatedUpdatetElement.appendChild(gxDurationElement)
    
    return gxAnimatedUpdatetElement    
    
    
###################################################
##
##
##                      STYLE ELEMENTS
##                  
##
###################################################


###################################################
## Style element
################################################### 
def createStyleElement(kmlDoc,  id=""):
    styleElement = kmlDoc.createElement("Style")
    if id is not "":
        styleElement.setAttribute("id",  id)
   
    return styleElement

###################################################
## StyleUrl element
################################################### 
def createStyleUrlElement(kmlDoc,  name=""):
    styleUrlElement = kmlDoc.createElement("styleUrl")
    textNode = kmlDoc.createTextNode("#"+name)
    styleUrlElement.appendChild(textNode)
    
    return styleUrlElement
    
###################################################
## IconStyle element
################################################### 
def createIconStyleElement(kmlDoc,  idIconStyle="", color="ffffffff",  scale=1,  idIcon="",  href="http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"):
    iconStyleElement = kmlDoc.createElement("IconStyle")
    if idIconStyle is not "":
        iconElement.setAttribute("id",  id)
    colorElement = createColorElement(kmlDoc,  color)
    iconStyleElement.appendChild(colorElement)
    scaleElement = createScaleElement(kmlDoc,  scale)
    iconStyleElement.appendChild(scaleElement)
    iconElement = createIconElement(kmlDoc,  idIcon, href  )
    iconStyleElement.appendChild(iconElement)
    
    return iconStyleElement

###################################################
## BalloonStyle element
################################################### 
def createBalloonStyleElement(kmlDoc,  id="",  bgColor="ffffffff", textColor="ff000000",  text=""):
    balloonStyleElement = kmlDoc.createElement("BalloonStyle")
    if (id is not ""):
        balloonStyleElement.setAttribute("id",  id)
    bgColorElement = createBgColorElement(kmlDoc,  bgColor)
    balloonStyleElement.appendChild(bgColorElement)
    textColorElement = createTextColorElement(kmlDoc,  textColor)
    balloonStyleElement.appendChild(textColorElement)
    textElement = createTextElement(kmlDoc,  text)
    balloonStyleElement.appendChild(textElement)
    
    return balloonStyleElement
    
###################################################
## LineStyle element
################################################### 
def createLineStyleElement(kmlDoc,  id="",  color="ffffffff", width=1):
    lineStyleElement = kmlDoc.createElement("LineStyle")
    if (id is not ""):
        lineStyleElement.setAttribute("id",  id)
    colorElement = createColorElement(kmlDoc,  color)
    lineStyleElement.appendChild(colorElement)
    widthElement = createWidthElement(kmlDoc,  width)
    lineStyleElement.appendChild(widthElement)
    
    return lineStyleElement

###################################################
## PolyStyle element
################################################### 
def createPolyStyleElement(kmlDoc,  id="",  color="ffffffff", colorMode="normal", fill=1, outline=1):
    polyStyleElement = kmlDoc.createElement("PolyStyle")
    if (id is not ""):
        lineStyleElement.setAttribute("id",  id)
    
    colorElement = createColorElement(kmlDoc,  color)
    polyStyleElement.appendChild(colorElement)
    
    colorModeElement = createColorModeElement(kmlDoc,  colorMode)
    polyStyleElement.appendChild(colorModeElement)
    
    fillElement = createFillElement(kmlDoc,  fill)
    polyStyleElement.appendChild(fillElement)
    
    outlineElement = createOutlineElement(kmlDoc,  outline)
    polyStyleElement.appendChild(outlineElement)
    
    return polyStyleElement

###################################################
## color element
###################################################   
def createColorElement(kmlDoc,  color="ffffffff"):
    colorElement = kmlDoc.createElement("color")
    textNode = kmlDoc.createTextNode(color)
    colorElement.appendChild(textNode)
    
    return colorElement
    
###################################################
## bgColor element
###################################################   
def createBgColorElement(kmlDoc,  bgColor="ffffffff"):
    bgColorElement = kmlDoc.createElement("bgColor")
    textNode = kmlDoc.createTextNode(bgColor)
    bgColorElement.appendChild(textNode)
    
    return bgColorElement

###################################################
## textColor element
###################################################   
def createTextColorElement(kmlDoc,  textColor="ff000000"):
    textColorElement = kmlDoc.createElement("textColor")
    textNode = kmlDoc.createTextNode(textColor)
    textColorElement.appendChild(textNode)
    
    return textColorElement
    
###################################################
## text element
###################################################   
def createTextElement(kmlDoc,  text=""):
    textElement = kmlDoc.createElement("text")
    #textNode = kmlDoc.createTextNode(text)
    #textElement.appendChild(textNode)
    textCDATASection = kmlDoc.createCDATASection(text)
    textElement.appendChild(textCDATASection)
    
    
    return textElement

###################################################
## width element
###################################################   
def createWidthElement(kmlDoc,  width=1):
    widthElement = kmlDoc.createElement("width")
    textNode = kmlDoc.createTextNode(str(width))
    widthElement.appendChild(textNode)
    
    return widthElement
    

###################################################
## colorMode element
###################################################   
def createColorModeElement(kmlDoc,  colorMode="normal"):
    colorModeElement = kmlDoc.createElement("colorMode")
    textNode = kmlDoc.createTextNode(colorMode)
    colorModeElement.appendChild(textNode)
    
    return colorModeElement

###################################################
## fill element
###################################################   
def createFillElement(kmlDoc,  fill=1):
    fillElement = kmlDoc.createElement("fill")
    textNode = kmlDoc.createTextNode(str(fill))
    fillElement.appendChild(textNode)
    
    return fillElement

###################################################
## fill element
###################################################   
def createOutlineElement(kmlDoc,  outline=1):
    outlineElement = kmlDoc.createElement("outline")
    textNode = kmlDoc.createTextNode(str(outline))
    outlineElement.appendChild(textNode)
    
    return outlineElement

###################################################
## scale element
###################################################       
def createScaleElement(kmlDoc,  scale=1):
    scaleElement = kmlDoc.createElement("scale")
    textNode = kmlDoc.createTextNode(str(scale))
    scaleElement.appendChild(textNode)
    
    return scaleElement
    
###################################################
## Icon element
################################################### 
def createIconElement(kmlDoc,  id="",  href="http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"):
    iconElement = kmlDoc.createElement("Icon")
     # id
    if id is not "":
        iconElement.setAttribute("id",  id)
    hrefElement = kmlDoc.createElement("href")
    textNode = kmlDoc.createTextNode(href)
    hrefElement.appendChild(textNode)
    iconElement.appendChild(hrefElement)
    
    return iconElement
    
    
    
    
    
    
    
    
    
def createSimpleLineString(fileName):
    kmlDoc = minidom.Document()
    kmlElement = createKMLElement(kmlDoc)
    documentElement = createDocumentElement(kmlDoc,  "",  "Tectonic Plates",  "",  1)
    documentElement = kmlElement.appendChild(documentElement)
    placemarkElement = createPlacemarkElement(kmlDoc,  "",  "Juan de Fuca Plate",  "")
    styleElement = createStyleElement(kmlDoc, "")
    lineStyleElement = createLineStyleElement(kmlDoc, "",  "ffff55ff",  2.5)
    styleElement.appendChild(lineStyleElement)
    placemarkElement.appendChild(styleElement)
    coordinates = [
                   [-130.597293, 50.678292, 3000], 
                   [-129.733457, 50.190606, 3000], 
                   [-130.509877, 49.387208, 3000], 
                   [-128.801553, 48.669761, 3000], 
                   [-129.156745, 47.858658, 3000], 
                   [-128.717835, 47.739997, 3000]]
    #lineStringElement = createLineStringElement(kmlDoc,  "",  0,  0,  "clampToGround",  coordinates)
    lineStringElement = createLineStringElement(kmlDoc,  "",  1,  0,  "relativeToGround",  coordinates)
    placemarkElement.appendChild(lineStringElement)
    documentElement.appendChild(placemarkElement)

    kmlFile = open(fileName,  'w')
    kmlFile.write(kmlDoc.toprettyxml(' '))
    kmlFile.close
 
