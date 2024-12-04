import json

import Utils

class Map:
    def __init__(self):
        self.trackPoints = []
        self.leftWallPoints = []
        self.rightWallPoints = []
    
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
