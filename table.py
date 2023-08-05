import pygame as pg
from utils import *
import random


def create_data():
    data = []
    for i in range(9):
        data.append([[[i for i in range(1, 10)], 2] for j in range(9)])
    return data


def print_data(data):
    data = clean_data(data)
    for row in data:
        print(str(row) + "\n")


def clean_data(data):
    cleaned = []
    for row in data:
        this_row = []
        for element in row:
            if element[1] == 0:
                this_row.append("Empty")
            else:
                this_row.append(element[0])
        cleaned.append(this_row)
    return cleaned


def get_error_cells(data):
    data = clean_data(data)
    error = []
    return error


def wave_function_collapse_implementation(data):
    for y, row in enumerate(data):
        # row check
        collapsed = []
        for x, element in enumerate(row):
            if len(element[0]) == 1:
                collapsed.append(element[0][0])
        for x, element in enumerate(row):
            if len(element[0]) == 1:
                continue
            for index, number in enumerate(element[0]):
                if number in collapsed:
                    data[y][x][0][index] = " "

    for x in range(9):
        # column check
        collapsed = []
        for y in range(9):
            if len(data[y][x][0]) == 1:
                collapsed.append(data[y][x][0][0])
        for y in range(9):
            if len(data[y][x][0]) == 1:
                continue
            for index, number in enumerate(data[y][x][0]):
                if number in collapsed:
                    data[y][x][0][index] = " "

    for y in range(3):
        for x in range(3):
            # chunk check
            collapsed = []
            for off_y in range(3):
                for off_x in range(3):
                    if len(data[3 * y + off_y][3 * x + off_x][0]) == 1:
                        collapsed.append(data[3 * y + off_y][3 * x + off_x][0][0])
            for off_y in range(3):
                for off_x in range(3):
                    if len(data[3 * y + off_y][3 * x + off_x][0]) == 1:
                        continue
                    for index, number in enumerate(
                        data[3 * y + off_y][3 * x + off_x][0]
                    ):
                        if number in collapsed:
                            data[3 * y + off_y][3 * x + off_x][0][index] = " "


def post_wave_function_collapse_implementation(data):
    probability = 100
    for y in range(9):
        for x in range(9):
            if len(data[y][x][0]) == 0:
                continue
            rand_num = random.randint(0, 100)
            if rand_num <= probability:
                values_copy = data[y][x][0].copy()
                random.shuffle(values_copy)
                for item in values_copy:
                    if isinstance(item, int) == False:
                        values_copy.remove(item)
                picked = values_copy[0]
                data[y][x][0] = list([picked])
                wave_function_collapse_implementation(data)


def digit_hiding(data):
    probabily = 40
    for y in range(9):
        for x in range(9):
            rand_num = random.randint(0, 100)
            if rand_num <= probabily:
                data[y][x][1] = 0


class Table:
    def __init__(self, app) -> None:
        from app import App

        self.app: App = app
        self.data = create_data()
        wave_function_collapse_implementation(self.data)
        post_wave_function_collapse_implementation(self.data)
        digit_hiding(self.data)
        self.cell_selected = False
        self.current_cell_selected = [-2, -2]
        self.font = pg.font.SysFont("Arial", 24, True)
        self.smallfont = pg.font.SysFont("Arial", 12, True)

    def get_highlighted_cell(self):
        mouse = pg.mouse.get_pos()
        grid_position = [(mouse[0] - 30) // 60, (mouse[1] - 30) // 60]
        return grid_position

    def draw_lines(self):
        for i in range(8):
            color = "gray"
            if (i + 1) % 3 == 0:
                color = "black"
            draw_line(
                self.app.display,
                color,
                [30 + (i + 1) * 60, 30],
                [30 + (i + 1) * 60, 570],
            )
        for i in range(8):
            color = "gray"
            if (i + 1) % 3 == 0:
                color = "black"
            draw_line(
                self.app.display,
                color,
                [30 + (i + 1) * 60, 30][::-1],
                [30 + (i + 1) * 60, 570][::-1],
            )

    def draw_numbers(self):
        for y, row in enumerate(self.data):
            for x, number in enumerate(row):
                if number[1] == 1 or number[1] == 2:
                    color = "gray"
                    if number[1] == 1:
                        color = "black"
                    if len(number[0]) > 1:
                        for index, value in enumerate(number[0]):
                            color = "gray"
                            number_surface = self.smallfont.render(
                                str(value), True, color, None
                            )
                            _x = index % 3
                            _y = index // 3
                            self.app.display.blit(
                                number_surface,
                                [
                                    30
                                    + x * 60
                                    + 20 * _x
                                    + 10
                                    - number_surface.get_width() * 0.5,
                                    30
                                    + y * 60
                                    + 20 * _y
                                    + 10
                                    - number_surface.get_height() * 0.5,
                                ],
                            )
                    else:
                        number_surface = self.font.render(
                            str(number[0][0]), True, color, None
                        )
                        self.app.display.blit(
                            number_surface,
                            [
                                30 + x * 60 + 30 - number_surface.get_width() * 0.5,
                                30 + y * 60 + 30 - number_surface.get_height() * 0.5,
                            ],
                        )

    def mouse_on_grid(self):
        mouse_grid_pos = self.get_highlighted_cell()
        if mouse_grid_pos[0] < 0 or mouse_grid_pos[0] > 8:
            return False
        if mouse_grid_pos[1] < 0 or mouse_grid_pos[1] > 8:
            return False
        return True

    def draw_highlighted_cell(self):
        mouse_grid_pos = self.get_highlighted_cell()
        if self.mouse_on_grid():
            draw_rect(
                self.app.display,
                "lightblue",
                pg.Rect(
                    30 + mouse_grid_pos[0] * 60, 30 + mouse_grid_pos[1] * 60, 60, 60
                ),
                5,
            )

    def draw_selected_cell(self):
        cell = self.select_cell()
        draw_rect(
            self.app.display,
            "red",
            pg.Rect(30 + cell[0] * 60, 30 + cell[1] * 60, 60, 60),
            5,
        )

    def edit_cell(self, cell, value):
        self.data[cell[1]][cell[0]][0] = value
        self.data[cell[1]][cell[0]][1] = 2

    def is_editable(self):
        return (
            self.data[self.current_cell_selected[1]][self.current_cell_selected[0]][1]
            == 0
            or self.data[self.current_cell_selected[1]][self.current_cell_selected[0]][
                1
            ]
            == 2
        )

    def select_cell(self):
        if self.mouse_on_grid() and pg.mouse.get_pressed(3)[0]:
            self.current_cell_selected = self.get_highlighted_cell()
            self.cell_selected = True
            return self.get_highlighted_cell()
        elif pg.mouse.get_pressed(3)[0] == True and self.mouse_on_grid() == False:
            self.cell_selected = False
            self.current_cell_selected = [-2, -2]
            return [-2, -2]
        else:
            return self.current_cell_selected

    def render(self):
        draw_rect(self.app.display, "white", pg.Rect(30, 30, 540, 540), 0, 10)
        draw_rect(self.app.display, "black", pg.Rect(30, 30, 540, 540), 1, 10)
        self.draw_lines()
        self.draw_numbers()
        self.draw_highlighted_cell()
        self.draw_selected_cell()
