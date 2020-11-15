import random
import math

import pyglet
from pyglet.gl import GL_POINTS


FPS = 120.0
DELTA_TIME = 1.0 / FPS
WIDTH = 800
HEIGHT = 600
CENTER = (WIDTH / 2, HEIGHT / 2)

MAX_PARTICLES = 50
MAX_ADD_PARTICLES = 1
GRAVITY = 1.5
START_POINT = [WIDTH / 2, 500]


class ParticleWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.gl.glClearColor(0.2, 0.1, 0.3, 1.0)
        pyglet.clock.schedule_interval(self.update, DELTA_TIME)
        self.world = World()

    def on_draw(self):
        self.clear()
        self.world.draw()

    def update(self, delta_time: float):
        self.world.update_particles(delta_time)
        self.world.update_sun(delta_time)
        # cap the max nbr that can be spawned
        for i in range(
            min(MAX_ADD_PARTICLES, MAX_PARTICLES - len(self.world.particles))
        ):
            self.world.add_particles()


class World:
    def __init__(self):
        self.particle_batch = pyglet.graphics.Batch()
        self.particles = list()
        self.sun = self.add_sun()

    def add_sun(self):
        sun = pyglet.shapes.Circle(
            CENTER[0], CENTER[1], radius := 15, color=(255, 255, 0)
        )
        sun.x, sun.y = sun.position
        sun.dx, sun.dy = 0, 0
        sun.mass = radius
        return sun

    def update_sun(self, delta_time: float):
        pass

    def add_particles(self):
        starting_point = list(START_POINT)
        starting_point[1] += (random.random() - 0.5) * 50
        particle = self.particle_batch.add(
            1, GL_POINTS, None, ("v2f/stream", starting_point)
        )
        particle.dx = (random.random()) * WIDTH / 2
        particle.dy = (random.random() - 0.5) * HEIGHT / 4
        particle.mass = 1
        particle.dead = False
        self.particles.append(particle)

    def update_particles(self, delta_time: float):
        for particle in self.particles:
            vertices = particle.vertices
            xpos = vertices[0]
            ypos = vertices[1]

            # check boundaries, else kill
            if (math.fabs(xpos - self.sun.x) < self.sun.radius) and (
                math.fabs(ypos - self.sun.y) < self.sun.radius
            ):
                particle.delete()
                particle.dead = True
                print(f"particle died at ({xpos}, {ypos})")

            # apply "gravity"
            particle.dy -= (ypos - self.sun.y) * GRAVITY * delta_time
            particle.dx -= (xpos - self.sun.x) * GRAVITY * delta_time
            vertices[0] += particle.dx * delta_time
            vertices[1] += particle.dy * delta_time
        self.particles = [p for p in self.particles if not p.dead]

    def draw(self):
        self.particle_batch.draw()
        self.sun.draw()


if __name__ == "__main__":
    ParticleWindow(width=WIDTH, height=HEIGHT, caption="Hello, World!")
    pyglet.app.run()
