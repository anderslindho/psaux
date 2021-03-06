import logging

import pyglet
from pyrr import Vector3

from psaux.config import PsauxConfig
from psaux.utils import BLUE
from psaux.world import World


class ParticleSimulator(pyglet.window.Window):
    def __init__(self, config: PsauxConfig = PsauxConfig(), *args, **kwargs):
        super().__init__(
            caption="psaux",
            width=config.width,
            height=config.height,
            resizable=True,
            *args,
            **kwargs,
        )
        pyglet.gl.glClearColor(*config.bg_color)
        pyglet.clock.schedule_interval(self.update, 1.0 / config.max_fps)

        # todo: figure out if line can be moved into batch
        self.mouse_line = pyglet.shapes.Line(0.0, 0.0, 0.0, 0.0, width=2, color=BLUE)
        self.mouse_line.visible = False
        self.world = World()

        self.click_coord = None
        self.drag = False

    def on_draw(self):
        self.clear()
        self.world.draw()
        self.mouse_line.draw()

    def update(self, delta_time: float):
        self.world.update(delta_time)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.click_coord = (x, y)
        self.mouse_line.x, self.mouse_line.y = x, y
        if modifiers & pyglet.window.key.MOD_SHIFT:
            self.world.place_sun(x, y)

        logging.debug(f"User pressed {button=} with {modifiers=} at {x=}, {y=}")

    def on_mouse_drag(
        self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int
    ):
        """
        two modes:
        - left click spawns particle, which has velocity relative to movement
        - right click moves screen
        """
        if buttons == pyglet.window.mouse.LEFT:
            self.drag = True
            self.mouse_line.visible = True
            self.mouse_line.x2, self.mouse_line.y2 = x, y
        else:
            for particle in self.world.entities:
                particle.position += Vector3([dx, dy, 0])

        logging.debug(
            f"User dragging mouse {buttons=} with {modifiers=} at {dx=}, {dy=}"
        )

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.drag and modifiers ^ pyglet.window.key.MOD_SHIFT:
            start_x, start_y = self.click_coord
            movement_vector = Vector3([x - start_x, y - start_y, 0])
            delta_x, delta_y, _ = movement_vector * self.world.settings.drag_sensitivity

            self.world.spawn_planet(
                position=Vector3([start_x, start_y, 0.0]),
                velocity=Vector3([delta_x, delta_y, 0.0]),
            )

        self.click_coord = None
        self.drag = False
        self.mouse_line.visible = False

    def on_mouse_scroll(self, x: float, y: float, scroll_x: float, scroll_y: float):
        """changes physical time speed. can be negative"""
        self.world.modify_time_warp(scroll_x)

        logging.debug(f"User scrolling mouse: {scroll_x=}, {scroll_y}")
