import json
import pygame as pg

import Ray
import Utils

class Map:
    def __init__(self):
        self.trackPoints = []
        self.leftWallPoints = []
        self.rightWallPoints = []

        self.collisionLines = []
    
    def save(self, filePath):
        with open(filePath, "w") as file:
            json.dump(Utils.serializeVector2Array(self.trackPoints), file, indent=4)

    def load(self, filePath):
        with open(filePath, "r") as file:
            self.trackPoints = Utils.deserializeVector2Array(json.load(file))
    
    def simplifyTrack(self, angleThreshold):
        # Always keep the first point
        newTrackPoints = [self.trackPoints[0]]
        
        for i in range(1, len(self.trackPoints) - 1):
            lastPoint = self.trackPoints[i - 1]
            currentPoint = self.trackPoints[i]
            nextPoint = self.trackPoints[i + 1]
            
            # Calculate the angle between vectors
            angle = Utils.angle_between(lastPoint, currentPoint, nextPoint)
            
            # Calculate the deflection angle
            deflection_angle = 180 - angle
            
            # Keep points where the deflection angle exceeds the threshold
            if deflection_angle > angleThreshold:
                newTrackPoints.append(currentPoint)
            # Else, the point is removed (not added)
        
        # Always keep the last point
        newTrackPoints.append(self.trackPoints[-1])
        
        # Update the track points
        self.trackPoints = newTrackPoints

    def generateWalls(self, trackWidth):
        self.leftWallPoints = []
        self.rightWallPoints = []
        num_points = len(self.trackPoints)

        for i in range(num_points):
            currentPoint = self.trackPoints[i]

            # Get previous and next points with wrapping
            prevPoint = self.trackPoints[i - 1]
            nextPoint = self.trackPoints[(i + 1) % num_points]

            # Compute the tangent vectors of the segments before and after the current point
            tangent1 = (currentPoint - prevPoint)
            tangent2 = (nextPoint - currentPoint)

            if tangent1.length() == 0 or tangent2.length() == 0:
                # Skip if any segment length is zero
                continue

            tangent1 = tangent1.normalize()
            tangent2 = tangent2.normalize()

            # Compute normals of the segments
            normal1 = pg.Vector2(-tangent1.y, tangent1.x)
            normal2 = pg.Vector2(-tangent2.y, tangent2.x)

            # Compute the bisector normal
            bisector = (normal1 + normal2)

            if bisector.length() == 0:
                # If normals are opposite, use one of them
                bisector = normal1
            else:
                bisector = bisector.normalize()

            # Compute left and right wall points
            leftPoint = currentPoint + bisector * (trackWidth / 2)
            rightPoint = currentPoint - bisector * (trackWidth / 2)

            self.leftWallPoints.append(leftPoint)
            self.rightWallPoints.append(rightPoint)
    
    def generateCollisionLines(self):
        self.collisionLines.clear()

        self.collisionLines.append(Ray.Line(self.leftWallPoints[-1], self.leftWallPoints[0]))
        for i in range(len(self.leftWallPoints)-1):
            self.collisionLines.append(Ray.Line(self.leftWallPoints[i], self.leftWallPoints[i+1]))
        
        self.collisionLines.append(Ray.Line(self.rightWallPoints[-1], self.rightWallPoints[0]))
        for i in range(len(self.rightWallPoints)-1):
            self.collisionLines.append(Ray.Line(self.rightWallPoints[i], self.rightWallPoints[i+1]))