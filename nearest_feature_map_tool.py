# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NearestFeature
                                 A QGIS plugin
 Selects the nearest feature.
                              -------------------
        begin                : 2014-10-15
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Peter Wells for Lutra Consulting
        email                : info@lutraconsulting.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.gui import QgsMapTool
from qgis.core import QgsMapLayer, QgsMapToPixel, QgsFeature, QgsFeatureRequest, QgsGeometry
from qgis.PyQt.QtGui import QCursor, QPixmap
from qgis.PyQt.QtCore import Qt

class NearestFeatureMapTool(QgsMapTool):
    
    def __init__(self, canvas):
        
        super(QgsMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
        
    def activate(self):
        self.canvas.setCursor(self.cursor)

        
    def canvasReleaseEvent(self, mouseEvent):
        """
        Each time the mouse is clicked on the map canvas, perform the following tasks:
        Loop through all visible vector layers and for each:
            Ensure no features are selected
            Determine the distance of the closes feature in the layer to the mouse click
            Keep track of the layer id and id of the closest feature
        Select the id of the closes feature 
        """
        layerData = []
        
        for layer in self.canvas.layers():
            if layer.type() != QgsMapLayer.VectorLayer:
                # Ignore this layer as it's not a vector
                continue
                
            if layer.featureCount() == 0:
                # There are no features
                continue
                
            layer.removeSelection()
            
            # Determine the location of click in real-world coordinates
            layerPoint = self.toLayerCoordinates( layer, mouseEvent.pos() )
            
            shortestDistance = float("inf")
            closestFeatureId = -1
            
            # Loop through all features in layer
            for f in layer.getFeatures():
                dist = f.geometry().distance( QgsGeometry.fromPointXY( layerPoint ) )
                if dist < shortestDistance:
                    shortestDistance = dist
                    closestFeatureId = f.id()
                    
            info = ( layer, closestFeatureId, shortestDistance )
            layerData.append(info)
            
        if not len(layerData) > 0:
            # Looks like no vector layers were found
            return
        
        # Sort layer information by shortest distance
        layerData.sort( key=lambda element: element[2] )
        
        # Select the closest feature
        layerWithClosestFeature, closestFeatureId, shortestDistance = layerData[0]
        layerWithClosestFeature.select( closestFeatureId )
