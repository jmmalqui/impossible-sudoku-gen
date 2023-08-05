import pygame as pg
from sys import exit
from table import Table, clean_data
import argparse


class App:
    def __init__(self) -> None:
        pg.init()
        self.display = pg.display.set_mode([600, 600])
        self.table = Table(self)
        self.not_saved = True

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if self.table.cell_selected:
                if event.type == pg.TEXTINPUT:
                    if event.text.isnumeric() and self.table.is_editable():
                        self.table.edit_cell(
                            self.table.current_cell_selected, [int(event.text)]
                        )

    def update(self):
        ...

    def render(self):
        self.display.fill("lightgray")
        self.table.render()
        if self.not_saved:
            pg.image.save(self.display, "output.png")
            self.not_saved = False
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.render()
