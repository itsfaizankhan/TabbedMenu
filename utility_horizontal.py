from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, RichLog, Static
from textual.widgets.option_list import Option


class Sidebar(Vertical):
    """Side dock containing main list."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("Menu 1", id="1"),
            Option("Menu 2", id="2"),
            Option("Menu 3", id="3"),
            Option("Menu 4", id="4"),
            Option("Menu 5", id="5"),
            Option("Menu 6", id="6"),
            Option("Menu 7", id="7"),
            Option("Menu 8", id="8"),
            Option("Menu 9", id="9"),
            classes="box",
            id="sidebar",
        )


class SubMenu(Static):
    def __init__(self, menu_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_id = menu_id
        self._contents = [
            Option(f"Menu {self._id} Option 1"),
            Option(f"Menu {self._id} Option 2"),
            Option(f"Menu {self._id} Option 3"),
            Option(f"Menu {self._id} Option 4"),
            Option(f"Menu {self._id} Option 5"),
            Option(f"Menu {self._id} Option 6"),
            Option(f"Menu {self._id} Option 7"),
            Option(f"Menu {self._id} Option 8"),
            Option(f"Menu {self._id} Option 9"),
        ]

        self.render()
        # if self.menu_id:
        #     self.add_options(
        #         [
        #             Option(f"Menu {self.menu_id} Option 1"),
        #             Option(f"Menu {self.menu_id} Option 2"),
        #             Option(f"Menu {self.menu_id} Option 3"),
        #             Option(f"Menu {self.menu_id} Option 4"),
        #             Option(f"Menu {self.menu_id} Option 5"),
        #             Option(f"Menu {self.menu_id} Option 6"),
        #             Option(f"Menu {self.menu_id} Option 7"),
        #             Option(f"Menu {self.menu_id} Option 8"),
        #             Option(f"Menu {self.menu_id} Option 9"),
        #         ]
        #     )

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option(f"Menu {self.menu_id} Option 1"),
            Option(f"Menu {self.menu_id} Option 2"),
            Option(f"Menu {self.menu_id} Option 3"),
            Option(f"Menu {self.menu_id} Option 4"),
            Option(f"Menu {self.menu_id} Option 5"),
            Option(f"Menu {self.menu_id} Option 6"),
            Option(f"Menu {self.menu_id} Option 7"),
            Option(f"Menu {self.menu_id} Option 8"),
            Option(f"Menu {self.menu_id} Option 9"),
            classes="box",
            id=f"o{self.menu_id}-menu",
        )


# class SubMenuContainer(Vertical):
#     def compose(self) -> ComposeResult:
#         # yield ScrollableContainer(Static(), id="dynamic-submenus")
#         yield SubMenu(id="submenu")
#
#     def mount_submenu(self):
#         pass


class UtilityContainers(App):
    CSS_PATH = "utility_horizontal.css"

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar(classes="column")
            # yield SubMenuContainer(classes="column")
            yield Vertical(id="submenu-container", classes="column")
            yield RichLog(highlight=True, markup=True)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Event handler called when an option in OptionList is selected."""
        option_id = event.option.id
        app_log = self.query_one(RichLog)
        prev_submenu = None
        # curr_submenu = None

        if not option_id or len(option_id) >= 2:
            if option_id:
                app_log.write("option_id: " + option_id)
            return

        app_log.write(option_id)
        submenu_container = self.query("#submenu-container").last()

        if submenu_container:
            app_log.write("Before: ")
            app_log.write(submenu_container.children)
            if len(submenu_container.children) != 0:
                app_log.write("First child before clearing node:")
                prev_submenu = submenu_container.children[0]
                # app_log.write(prev_submenu._id)
                submenu_container.remove_children("*")

        submenu_container = self.query("#submenu-container").last()
        # new_submenu = SubMenu(menu_id=f"o{option_id}")
        submenu_container.mount(SubMenu(menu_id=f"o{option_id}", id=f"o{option_id}"))

        app_log.write("After: ")
        app_log.write(submenu_container.children)

        app_log.write("-----")
        if submenu_container:
            app_log.write("Post children: ")
            app_log.write(submenu_container.children)
            app_log.write("First child: ")
            if len(submenu_container.children) != 0:
                prev_submenu = submenu_container.children[0]
                app_log.write(prev_submenu)

        # if submenu_container.first().id != option_id:
        #     pass

        # menus = self.query(OptionList).exclude("#sidebar")
        #
        # menu_to_hide = menus.exclude(".hidden")
        # for menu in menu_to_hide:
        #     menu.add_class("hidden")
        #
        # menu_to_show = menus.filter(f"#o{option_id}-menu").first()
        # menu_to_show.remove_class("hidden")
        # menu_to_show.focus()
        #
        # app_log.write(menu_to_show)


if __name__ == "__main__":
    app = UtilityContainers()
    app.run()
