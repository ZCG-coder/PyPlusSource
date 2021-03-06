"""Closable ttk.Notebook"""
from src.constants import logger
from src.functions import is_dark_color, lighten_color
from src.modules import tk, ttk, ttkthemes
from src.settings import Settings


class ClosableNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab
    images drawn by me using the mspaint app (the rubbish in many people's opinion)

    Change the layout, makes it look like this:
    +------------+
    | title   [X]|
    +-------------------------"""

    __initialized = False

    def __init__(self, master, cmd):
        self.style = ttkthemes.ThemedStyle()
        self.settings = Settings()
        self.style.set_theme(self.settings.get_settings("theme"))
        self.bg = self.style.lookup("TLabel", "background")
        self.fg = self.style.lookup("TLabel", "foreground")
        if is_dark_color(self.bg):
            self.close_icon = tk.PhotoImage("img_close", file="Images/close.gif")
        else:
            self.close_icon = tk.PhotoImage("img_close", file="Images/close-dark.gif")
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True
        ttk.Notebook.__init__(self, master=master, style="CustomNotebook")
        self.cmd = cmd

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(["pressed"])
            self._active = index
        else:
            self.event_generate("<<Notebook_B1-Down>>", when="tail")
        logger.debug("Close tab start")

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        try:
            if not self.instate(["pressed"]):
                return

            element = self.identify(event.x, event.y)
            index = self.index("@%d,%d" % (event.x, event.y))

            if "close" in element and self._active == index:
                self.cmd()

            self.state(["!pressed"])
            self._active = None
            logger.debug("Close tab end")

        except Exception:
            logger.exception("Error:")

    def __initialize_custom_style(self):
        style = ttk.Style()

        style.element_create("close", "image", "img_close", border=10, sticky="")
        style.configure(
            "CustomNotebook.Tab", background=lighten_color(self.bg, 20, 20, 20)
        )
        style.layout(
            "CustomNotebook",
            [
                (
                    "CustomNotebook.client",
                    {
                        "sticky": "nswe",
                    },
                )
            ],
        )
        style.layout(
            "CustomNotebook.Tab",
            [
                (
                    "CustomNotebook.tab",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "CustomNotebook.padding",
                                {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "CustomNotebook.label",
                                            {"side": "left", "sticky": ""},
                                        ),
                                        (
                                            "CustomNotebook.close",
                                            {"side": "left", "sticky": ""},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        logger.debug("Initialized custom style.")
