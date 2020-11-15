import pyglet
from pyglet.gl import glViewport

from psaux.world import World
from psaux.config import WIDTH, HEIGHT, DELTA_TIME, MAX_PARTICLES, MAX_ADD_PARTICLES


class ParticleWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(width=WIDTH, height=HEIGHT, resizable=True, *args, **kwargs)
        pyglet.gl.glClearColor(0.15, 0.1, 0.2, 1.0)
        pyglet.clock.schedule_interval(self.update, DELTA_TIME)
        self.world = World()

    def on_draw(self):
        self.clear()
        self.world.particle_batch.draw()
        self.world.sun.draw()

    def update(self, delta_time: float):
        self.world.apply_forces(delta_time)
        # cap the max nbr that can be spawned
        for i in range(
            min(MAX_ADD_PARTICLES, MAX_PARTICLES - len(self.world.particles))
        ):
            self.world.add_particle()


if __name__ == "__main__":
    window = ParticleWindow(caption="psaux")
    window.set_minimum_size(640, 480)
    pyglet.app.run()
