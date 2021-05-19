from dataclasses import dataclass


@dataclass
class PsauxConfig:
    width: int = 1024
    height: int = 768
    max_fps: int = 60
    bg_color: tuple = (0.15, 0.1, 0.2, 1.0)


def delta_time():
    return 1.0 / PsauxConfig.max_fps


@dataclass()
class WorldSettings:
    gravity_constant: float = 6.67e-11
    time_warp_factor: float = 1e5
    time_warp_multiplier: float = 1e4
    drag_sensitivity: float = 5e-6

