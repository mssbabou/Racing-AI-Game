import math
import pygame as pg

pg.init()

screen = pg.display.set_mode((600, 600))
pg.display.set_caption("Racing AI")
clock = pg.time.Clock()

CAR_MAX_SPEED = 5
CAR_STEER_SPEED = 4

carImageAsset = pg.image.load("Lambo.png")
carImageAssetWidth, carImageAssetHeight = carImageAsset.get_size()
carImageAssetAspectRatio = carImageAssetHeight / carImageAssetWidth
carImageAsset = pg.transform.scale(carImageAsset, (30, 30 * carImageAssetAspectRatio))
carImageRect = carImageAsset.get_rect(center=(300, 300))
carPosition = pg.Vector2(300, 300)
carAngle = 0

running = True
while running:
    arrowKeyInput = pg.Vector2()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        arrowKeyInput.y -= 1
    if keys[pg.K_DOWN]:
        arrowKeyInput.y += 1
    if keys[pg.K_LEFT]:
        arrowKeyInput.x -= 1
    if keys[pg.K_RIGHT]:
        arrowKeyInput.x += 1

    carAngle -= arrowKeyInput.x * CAR_STEER_SPEED 
    carPointing = pg.Vector2(math.sin(math.radians(carAngle)), math.cos(math.radians(carAngle)))
    carPosition += carPointing * arrowKeyInput.y * CAR_MAX_SPEED

    transformedCarImageAsset = pg.transform.rotate(carImageAsset, carAngle)
    transformedCarImageRect = transformedCarImageAsset.get_rect(center=carPosition)

    screen.fill("white")

    screen.blit(transformedCarImageAsset, transformedCarImageRect.topleft)

    pg.display.flip()

    clock.tick(60)  # limits FPS to 60

pg.quit()