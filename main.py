import torch
import torch.nn as nn
import pygame as pg
import json

import Car
import Map
import Ray
import Utils

def main():
    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()

    screen = pg.display.set_mode((600, 600))
    pg.display.set_caption("Racing AI")
    clock = pg.time.Clock()

    # Create player car
    playerCar = Car.Car("Lambo.png", maxSpeed=4, accel=3, steerSpeed=3)
    playerCar.setImageAssetWidth(25)

    map = Map.Map()
    map.load("simpleTrackMap.json")
    map.generateWalls(100)
    map.generateCollisionLines()

    trainingData = []

    model = torch.load("GPT5.pth")
    model.eval()

    running = True
    while running:
        arrowKeyInput = pg.Vector2()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pg.mouse.get_pos()
                    #map.trackPoints.append(pg.Vector2(mousePos[0], mousePos[1]))
                    #ap.generateWalls(80)

        # Handle input
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            arrowKeyInput.y -= 1
        if keys[pg.K_DOWN]:
            arrowKeyInput.y += 1
        if keys[pg.K_LEFT]:
            arrowKeyInput.x -= 1
        if keys[pg.K_RIGHT]:
            arrowKeyInput.x += 1

        if pg.joystick.get_count() > 0:
            # X-axis from left joystick (Axis 0)
            x_axis = joystick.get_axis(0)

            # Y-axis from triggers: Right (Axis 5), Left (Axis 4)
            right_trigger = joystick.get_axis(4)  # Typically 0.0 to 1.0
            left_trigger = joystick.get_axis(5)   # Typically 0.0 to 1.0

            # Combine triggers into a single Y-axis
            y_axis = right_trigger - left_trigger

            # Create the vector
            arrowKeyInput = pg.Vector2(x_axis, y_axis)

        screen.fill("white")
        
        playerCar.castRays(map.collisionLines, 180, 6, 300)
        playerCar.drawRays(screen)

        inferenceInput = playerCar.getRayDistances() + [playerCar.getSpeedNormalized()]
        inferenceInput = torch.tensor([inferenceInput], dtype=torch.float32)
        modelOutput = []
        with torch.no_grad():
            modelOutput = model(inferenceInput)

        output = modelOutput.tolist()
        # Update car
        playerCar.steer(output[0][0])
        playerCar.drive(output[0][1])

        # Draw everything
        screen.blit(playerCar.transformedImageAsset, playerCar.transformedImageRect.topleft)

        #drawTrack(screen, map.trackPoints)
        drawTrack(screen, map.leftWallPoints)
        drawTrack(screen, map.rightWallPoints)

        trainingData.append({
            "inputs": {"rays": playerCar.getRayDistances(), "speed": playerCar.getSpeedNormalized()},
            "outputs": {"drive": Utils.vector2ToArray(arrowKeyInput)}
        })

        # Refresh display
        pg.display.flip()
        clock.tick(60)  # Limit
        print(clock.get_fps())
    
    #with open('training_data.json', 'w') as json_file:
    #    json.dump(trainingData, json_file, indent=4)
    #map.simplifyTrack(10)
    #map.save("simpleTrackMap.json")
    
def drawTrack(screen, trackPoints):
    if(len(trackPoints) == 0):
        return
     
    lastPoint = 0
    for point in trackPoints:
        if (lastPoint != 0):
            pg.draw.line(screen, "black", lastPoint, point)
        #pg.draw.circle(screen, "blue", point, 8)
        lastPoint = point
    pg.draw.line(screen, "black", trackPoints[0], trackPoints[-1])

if __name__ == "__main__":
    main()