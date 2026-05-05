'''

'''
import json
import re
from aipi_lite import AiPiLite
class AiPiLiteUI:
    '''
    '''
    LINEMAX = 6
    _aipi_lite: AiPiLite
    _cursor_draw_index: int
    _cursor_data_index: int
    _line_draw_index: int
    _page_index: int
    _up_page_index: int
    _definition: dict
    _page: dict

    def __init__(self, master: AiPiLite, filename: str):
        self._aipi_lite = master
        self._cursor_data_index = 0
        self._cursor_draw_index = 0
        self._line_draw_index = 0
        self._up_page_index = 0
        self._page_index = 0
        with open(filename, 'r') as file:
            self._definition = json.load(file)
        self.load_page()   
        self.draw_page() 
        self._aipi_lite.send_command = self.run_command

    def run_command(self, command: str):
        command = command + str(self._cursor_data_index)
        for key, value in self._page["commands"].items():
            search_key = re.compile(key)
            if re.search(search_key, command):
                funct = value.get("method")
                args = value.get("args")
                method = getattr(self, funct)
                if args:
                    method(args)
                else:
                    method()
                return None
        print(f'No command found for {command} at index {self._cursor_data_index}')

    def draw_lines(self):
        i = 0
        starting_index = self._line_draw_index
        ending_index = min(len(self._page["lines"]),starting_index + self.LINEMAX)
        for _ in range(starting_index,ending_index):
            line = self._page["lines"][starting_index + i]
            self._aipi_lite.print_text(line["text"],line["color"],line["size"],i)
            i += 1
    
    def draw_page(self):
        if "lines" in self._page:
            self.draw_lines()
        if "cursor" in self._page:
            self.draw_cursor()
        if "pixels" in self._page:
            self.draw_pixels()
            
    def load_page(self):
        self._page = self._definition["pages"][self._page_index]
        self._cursor_data_index = 0
        self._cursor_draw_index = 0
        self._line_draw_index = 0
        self._aipi_lite.clean_screen(self._page["background"])

    def select_page(self, page_index: int):
        self._up_page_index = self._page_index
        self._page_index = int(page_index)
        self.load_page()
        self.draw_page()

    def up_page(self):
        if self._up_page_index != self._page_index:
            self.select_page(self._up_page_index)

    def draw_cursor(self, clear = False):
        cursor = self._page["cursor"]
        if clear:
            color = self._page["background"]
        else:
            color = cursor["color"]
        if cursor["vertical"]:
            pos = (-0.5 , self._cursor_draw_index)
            self._aipi_lite.draw_char(pos, cursor["character"], color, cursor["size"])
    
    def draw_pixels(self):
        for pixel in self._page["pixels"]:
            self._aipi_lite.draw_pixel((pixel["x"],pixel["y"]),pixel["color"])

    def inc_cursor(self):
        self.draw_cursor(clear = True)
        self._cursor_data_index += 1
        self._cursor_draw_index += 1
        if self._cursor_data_index >= self._page["cursor"]["locations"]:
            self._cursor_data_index = 0
            self._cursor_draw_index = 0
            # self._cursor_draw_index = 0
            # self._line_draw_index = 0
            # self._aipi_lite.clean_screen(self._page["background"])
            # self.draw_lines()
        if self._cursor_data_index < self._line_draw_index or self._cursor_data_index >= (self._line_draw_index + self.LINEMAX): 
            self._cursor_draw_index = 0
            self._line_draw_index = self._cursor_data_index
            self._aipi_lite.clean_screen(self._page["background"])
            self.draw_lines()
        self.draw_cursor()
