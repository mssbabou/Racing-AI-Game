import pygame as pg

class Line:
    def __init__(self, a: pg.Vector2, b: pg.Vector2):
        self.a = a
        self.b = b

class Ray:
    def __init__(self, origin: pg.Vector2, direction: pg.Vector2, length: float):
        self.origin = origin
        self.direction = direction.normalize()
        self.length = length

        self.hit_point = None
        self.distance = None
        self.distance_normalized = None

    def cast(self, scene):
        closest_point = None
        min_distance = float('inf')

        for line in scene:
            intersection = self._intersect_line(line)
            if intersection:
                distance = self.origin.distance_to(intersection)
                if distance < min_distance and distance <= self.length:
                    min_distance = distance
                    closest_point = intersection

        # Update attributes
        self.hit_point = closest_point
        if closest_point:
            self.distance = min_distance
            self.distance_normalized = min_distance / self.length
        else:
            self.distance = None
            self.distance_normalized = None

        return closest_point

    def _intersect_line(self, line):
        # Parametric line intersection
        x1, y1 = line.a.x, line.a.y
        x2, y2 = line.b.x, line.b.y
        x3, y3 = self.origin.x, self.origin.y
        x4, y4 = self.origin.x + self.direction.x * self.length, self.origin.y + self.direction.y * self.length

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # Lines are parallel or coincident

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

        if 0 <= t <= 1 and 0 <= u <= 1:
            # Intersection point
            ix = x1 + t * (x2 - x1)
            iy = y1 + t * (y2 - y1)
            return pg.Vector2(ix, iy)
        return None
    
    def draw(self, screen):
        # Draw the ray
        end_point = self.origin + self.direction * self.length
        pg.draw.line(screen, (60, 60, 60), self.origin, end_point, 1)

        # Highlight hit point, if any
        if self.hit_point:
            pg.draw.circle(screen, (255, 0, 0), (int(self.hit_point.x), int(self.hit_point.y)), 5)
            pg.draw.line(screen, (0, 255, 0), self.origin, self.hit_point, 2)

        # Display distance text
        #font = pg.font.Font(None, 24)
        #if self.hit_point and self.distance is not None:
        #    text = font.render(f"Distance: {self.distance:.2f}", True, (0, 0, 0))
        #    screen.blit(text, (self.origin.x + 10, self.origin.y - 20))
        #else:
        #    text = font.render("No Hit", True, (0, 0, 0))
        #    screen.blit(text, (self.origin.x + 10, self.origin.y - 20))