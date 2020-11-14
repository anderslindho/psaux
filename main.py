import sys

from psaux.particle import Particle, Position, Velocity


class Application:
    """main application; provides run-loop"""

    def __init__(self, particles=None):
        self.running = True
        if particles is None:
            self.particles = []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def run(self):
        while self.running:
            for particle in self.particles:
                particle.update()
                print(f"The particle's position is {particle.position}")


if __name__ == "__main__":
    app = Application()
    app.add_particle(
        Particle(
            Position(0, 0),
            0.0,
            Velocity(0.1, 0.2),
        )
    )
    app.run()
    sys.exit()
