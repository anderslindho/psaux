import random

import pyglet

from psaux.particle import Particle, Position, Velocity

FPS = 120.0
DELTA_TIME = 1.0 / FPS
WIDTH = 800
HEIGHT = 600


class ParticleWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pyglet.gl.glClearColor(0.2, 0.1, 0.3, 1.0)
        pyglet.clock.schedule_interval(self.update, DELTA_TIME)

        self.world = World()

    def on_draw(self):
        self.clear()
        self.world.batch.draw()

    def update(self, dt):
        self.world.update(dt)


class World:
    def __init__(self):
        self.particle = Particle(
            position=Position(WIDTH / 2, HEIGHT / 2),
            mass=10.0,
            velocity=Velocity(random.randrange(-30, 30), random.randrange(-30, 30)),
        )
        self.batch = pyglet.graphics.Batch()

        self.circle = pyglet.shapes.Circle(
            x=self.particle.position.x,
            y=self.particle.position.y,
            radius=self.particle.mass,
            batch=self.batch,
        )

    def update(self, delta_time):
        self.particle.update(delta_time)
        self.circle.anchor_position(self.particle.position.x, self.particle.position.y)


if __name__ == "__main__":
    window = ParticleWindow(width=WIDTH, height=HEIGHT, caption="Hello, World!")

    pyglet.app.run()
