class TC:
    """usage: print(f"{TC('sfsf').fg_green.bg_orange} xxxx {TC('sfsfsfds').bold.fg_black.strikethrough.underline.bg_red}")
        print(f"{TC('sfsf').fg_green.bg_orange.bold}{TC('sfsfsfds').fg_orange}")"""

    def __init__(self, text):
        self.text = str(text)
        self.c_reset = "\033[0m"
        self.c_bold = "\033[1m"
        self.c_underline = "\033[4m"
        self.c_reverse = "\033[7m"
        self.c_strikethrough = "\033[9m"
        self.c_invisible = "\033[8m"
        self.c_fg_black = "\033[30m"
        self.c_fg_red = "\033[31m"
        self.c_fg_green = "\033[32m"
        self.c_fg_orange = "\033[33m"
        self.c_fg_blue = "\033[34m"
        self.c_fg_purple = "\033[35m"
        self.c_fg_cyan = "\033[36m"
        self.c_fg_lightgrey = "\033[37m"
        self.c_fg_darkgrey = "\033[90m"
        self.c_fg_lightred = "\033[91m"
        self.c_fg_lightgreen = "\033[92m"
        self.c_fg_yellow = "\033[93m"
        self.c_fg_lightblue = "\033[94m"
        self.c_fg_pink = "\033[95m"
        self.c_fg_lightcyan = "\033[96m"
        self.c_bg_black = "\033[40m"
        self.c_bg_red = "\033[41m"
        self.c_bg_green = "\033[42m"
        self.c_bg_orange = "\033[43m"
        self.c_bg_blue = "\033[44m"
        self.c_bg_purple = "\033[45m"
        self.c_bg_cyan = "\033[46m"
        self.c_bg_lightgrey = "\033[47m"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.text = f"{self.text}{self.c_reset}"
        return self.text

    @property
    def bold(self):
        self.text = f"{self.c_bold}{self.text}"
        return self

    @property
    def underline(self):
        self.text = f"{self.c_underline}{self.text}"
        return self

    @property
    def reverse(self):
        self.text = f"{self.c_reverse}{self.text}"
        return self

    @property
    def strikethrough(self):
        self.text = f"{self.c_strikethrough}{self.text}"
        return self

    @property
    def invisible(self):
        self.text = f"{self.c_invisible}{self.text}"
        return self

    @property
    def fg_black(self):
        self.text = f"{self.c_fg_black}{self.text}"
        return self

    @property
    def fg_red(self):
        self.text = f"{self.c_fg_red}{self.text}"
        return self

    @property
    def fg_green(self):
        self.text = f"{self.c_fg_green}{self.text}"
        return self

    @property
    def fg_orange(self):
        self.text = f"{self.c_fg_orange}{self.text}"
        return self

    @property
    def fg_blue(self):
        self.text = f"{self.c_fg_blue}{self.text}"
        return self

    @property
    def fg_purple(self):
        self.text = f"{self.c_fg_purple}{self.text}"
        return self

    @property
    def fg_cyan(self):
        self.text = f"{self.c_fg_cyan}{self.text}"
        return self

    @property
    def fg_lightgrey(self):
        self.text = f"{self.c_fg_lightgrey}{self.text}"
        return self

    @property
    def fg_darkgrey(self):
        self.text = f"{self.c_fg_darkgrey}{self.text}"
        return self

    @property
    def fg_lightred(self):
        self.text = f"{self.c_fg_lightred}{self.text}"
        return self

    @property
    def fg_lightgreen(self):
        self.text = f"{self.c_fg_lightgreen}{self.text}"
        return self

    @property
    def fg_yellow(self):
        self.text = f"{self.c_fg_yellow}{self.text}"
        return self

    @property
    def fg_lightblue(self):
        self.text = f"{self.c_fg_lightblue}{self.text}"
        return self

    @property
    def fg_pink(self):
        self.text = f"{self.c_fg_pink}{self.text}"
        return self

    @property
    def fg_lightcyan(self):
        self.text = f"{self.c_fg_lightcyan}{self.text}"
        return self

    @property
    def bg_black(self):
        self.text = f"{self.c_bg_black}{self.text}"
        return self

    @property
    def bg_red(self):
        self.text = f"{self.c_bg_red}{self.text}"
        return self

    @property
    def bg_green(self):
        self.text = f"{self.c_bg_green}{self.text}"
        return self

    @property
    def bg_orange(self):
        self.text = f"{self.c_bg_orange}{self.text}"
        return self

    @property
    def bg_blue(self):
        self.text = f"{self.c_bg_blue}{self.text}"
        return self

    @property
    def bg_purple(self):
        self.text = f"{self.c_bg_purple}{self.text}"
        return self

    @property
    def bg_cyan(self):
        self.text = f"{self.c_bg_cyan}{self.text}"
        return self

    @property
    def bg_lightgrey(self):
        self.text = f"{self.c_bg_lightgrey}{self.text}"
        return self


# print(f"{TC('sfsf').fg_green.bg_orange} xxxx {TC('sfsfsfds').bold.fg_black.strikethrough.underline.bg_red}")
# print(f"{TC('sfsf').fg_green.bg_orange.bold}{TC('sfsfsfds').fg_orange}")
