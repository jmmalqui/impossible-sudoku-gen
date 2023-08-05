import pygame as pg


def draw_rect(
    surface,
    color,
    rect,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
):
    return pg.draw.rect(
        surface,
        color,
        rect,
        width,
        border_radius,
        border_top_left_radius,
        border_top_right_radius,
    )


def draw_line(surface, color, start_pos, end_pos, width: int = 1):
    return pg.draw.line(surface, color, start_pos, end_pos, width)
