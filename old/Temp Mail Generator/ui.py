from os import get_terminal_size as _terminal_size

class Center:
    @staticmethod
    def _xspaces(text: str):
        try:
            col = _terminal_size().columns
        except OSError:
            return 0
        ntext = max(len(line.strip()) for line in text.splitlines())
        return (col - ntext) // 2

    def XCenter(text: str, spaces: int = None):
        if spaces is None:
            spaces = Center._xspaces(text=text)
        return "\n".join(f"{' ' * spaces}{line}" for line in text.splitlines())


class Colors:
    black_to_white = ["m;m;m"]
    black_to_red = ["m;0;0"]
    black_to_green = ["0;m;0"]
    black_to_blue = ["0;0;m"]

    white_to_black = ["n;n;n"]
    white_to_red = ["255;n;n"]
    white_to_green = ["n;255;n"]
    white_to_blue = ["n;n;255"]

    red_to_black = ["n;0;0"]
    red_to_white = ["255;m;m"]
    red_to_yellow = ["255;m;0"]
    red_to_purple = ["255;0;m"]

    green_to_black = ["0;n;0"]
    green_to_white = ["m;255;m"]
    green_to_yellow = ["m;255;0"]
    green_to_cyan = ["0;255;m"]

    blue_to_black = ["0;0;n"]
    blue_to_white = ["m;m;255"]
    blue_to_cyan = ["0;m;255"]
    blue_to_purple = ["m;0;255"]

    yellow_to_red = ["255;n;0"]
    yellow_to_green = ["n;255;0"]

    purple_to_red = ["255;0;n"]
    purple_to_blue = ["n;0;255"]

    cyan_to_green = ["0;255;n"]
    cyan_to_blue = ["0;n;255"]


    dynamic_colors = [
        black_to_white, black_to_red, black_to_green, black_to_blue,
        white_to_black, white_to_red, white_to_green, white_to_blue,

        red_to_black, red_to_white, red_to_yellow, red_to_purple,
        green_to_black, green_to_white, green_to_yellow, green_to_cyan,
        blue_to_black, blue_to_white, blue_to_cyan, blue_to_purple,

        yellow_to_red, yellow_to_green,
        purple_to_red, purple_to_blue,
        cyan_to_green, cyan_to_blue
    ]

    for color in dynamic_colors:
        _col = 20
        reversed_col = 220

        dbl_col = 20
        dbl_reversed_col = 220

        content = color[0]
        color.pop(0)

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(reversed_col))
                color.append(result)

            _col += 20
            reversed_col -= 20

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(dbl_reversed_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(dbl_col))
                color.append(result)

            dbl_col += 20
            dbl_reversed_col -= 20


class _MakeColors:
    @staticmethod
    def _makeansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"

    @staticmethod
    def _getspaces(text: str) -> int:
        return len(text) - len(text.lstrip())


class Colorate:
    @staticmethod
    def Color(color: str, text: str) -> str:
        return _MakeColors._makeansi(color=color, text=text)

    @staticmethod
    def Horizontal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = []

        for line in lines:
            color_n = 0
            for car in line:
                colorR = color[color_n]
                result.append(f"{' ' * _MakeColors._getspaces(car)}{_MakeColors._makeansi(colorR, car.strip())}")
                color_n = (color_n + speed) % len(color)

            result.append("\n")

        return ''.join(result).rstrip()

    @staticmethod
    def Diagonal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = []
        color_len = len(color)
        color_n = 0

        for line in lines:
            for i, car in enumerate(line):
                colorR = color[color_n]
                result.append(f"{' ' * _MakeColors._getspaces(car)}{_MakeColors._makeansi(colorR, car.strip())}")
                color_n = (color_n + speed) % color_len if i % 2 == 0 else color_n

            result.append("\n")

        return ''.join(result).rstrip()
