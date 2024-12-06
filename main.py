import pygame as pg

import Car
import Map
import Ray

def main():
    pg.init()

    screen = pg.display.set_mode((600, 600))
    pg.display.set_caption("Racing AI")
    clock = pg.time.Clock()

    # Create player car
    playerCar = Car.Car("Lambo.png", maxSpeed=5, accel=3, steerSpeed=4)
    playerCar.setImageAssetWidth(25)

    map = Map.Map()
    map.load("simpleTrackMap.json")
    map.generateWalls(80)
    map.generateCollisionLines()

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

        # Update car
        playerCar.steer(arrowKeyInput.x)
        playerCar.drive(arrowKeyInput.y)

        # Draw everything
        screen.fill("white")
        screen.blit(playerCar.transformedImageAsset, playerCar.transformedImageRect.topleft)

        drawTrack(screen, map.trackPoints)
        drawTrack(screen, map.leftWallPoints)
        drawTrack(screen, map.rightWallPoints)

        playerCar.castRays(map.collisionLines, 180, 6, 300)
        playerCar.drawRays(screen)

        # Refresh display
        pg.display.flip()
        clock.tick(60)  # Limit
        print(clock.get_fps())
    
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