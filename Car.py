import math
import pygame as pg

class Car:
    def __init__(self, imageAssetPath, maxSpeed, accel, steerSpeed):
        self.ImageAsset = pg.image.load(imageAssetPath)
        self.transformedImageAsset = self.ImageAsset
        self.transformedImageRect = self.transformedImageAsset.get_rect()

        self.MaxSpeed = maxSpeed
        self.Accel = accel
        self.SteerSpeed = steerSpeed

        self.currentSpeed = 0
        self.position = pg.Vector2(300, 50)  # Start in the middle of the screen
        self.velocity = pg.Vector2()
        self.direction = pg.Vector2(0, -1)  # Default to facing upward
        self.rotation = 90

    def drive(self, drive):
        if drive != 0:
            # Apply acceleration or braking
            self.currentSpeed += -drive * self.Accel * (1 / 60)
            self.currentSpeed = max(-self.MaxSpeed, min(self.currentSpeed, self.MaxSpeed))
        else:
            # Apply friction when no input is provided
            if self.currentSpeed > 0:
                self.currentSpeed -= self.Accel * 0.5 * (1 / 60)  # Decelerate forward motion
                self.currentSpeed = max(0, self.currentSpeed)  # Ensure it doesn't go below 0
            elif self.currentSpeed < 0:
                self.currentSpeed += self.Accel * 0.5 * (1 / 60)  # Decelerate reverse motion
                self.currentSpeed = min(0, self.currentSpeed)  # Ensure it doesn't go above 0

        # Update position based on direction and speed
        self.position += self.direction * self.currentSpeed

    def steer(self, steer):
        # Update rotation
        self.rotation += steer * self.SteerSpeed

        # Update direction
        self.direction = self.getDirection()

        # Rotate the image
        self.transformedImageAsset = pg.transform.rotate(self.ImageAsset, -self.rotation)
        self.transformedImageRect = self.transformedImageAsset.get_rect(center=(self.position.x, self.position.y))

    def getDirection(self):
        # Calculate direction vector based on rotation
        return pg.Vector2(
            math.sin(math.radians(self.rotation)),
            -math.cos(math.radians(self.rotation))
        )
    
    def getSpeedNormalized(self):
        return self.currentSpeed / self.MaxSpeed
    
    def setImageAssetWidth(self, width):
        # Scale image with aspect ratio maintained
        oldWidth, oldHeight = self.ImageAsset.get_size()
        aspectRatio = oldHeight / oldWidth
        self.ImageAsset = pg.transform.scale(self.ImageAsset, (width, int(width * aspectRatio)))
