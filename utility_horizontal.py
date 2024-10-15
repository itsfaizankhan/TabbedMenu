from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList  # as OptionL
from textual.widgets import Footer, RichLog, Static
from textual.widgets.option_list import Option

# class OptionList(OptionL):
#
#     BINDINGS = [
#         Binding("j", "cursor_down", "Move down"),
#         Binding("k", "cursor_up", "Move up"),
#         # Binding("right", "focus_next", "Move focus to the next widget"),
#         # Binding("left", "focus_previous", "Move focus to the previous widget"),
#         # Binding("l", "focus_next", "Focus Next", show=False, priority=True),
#         # Binding("h", "focus_previous", "Focus Previous", show=False, priority=True),
#     ]


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
            id=f"{self.menu_id}-menu",
        )


class UtilityContainers(App):
    CSS_PATH = "utility_horizontal.css"

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar(classes="column")
            yield Vertical(id="submenu-container", classes="column")
            yield RichLog(highlight=True, markup=True)
            yield Footer()

    async def on_option_list_option_selected(
        self, event: OptionList.OptionSelected
    ) -> None:
        """Event handler called when an option in OptionList is selected."""
        option_id = event.option.id
        app_log = self.query_one(RichLog)

        if not option_id or len(option_id) >= 2:
            if option_id:
                app_log.write("option_id: " + option_id)
            return

        app_log.write(option_id)
        submenu_container = self.query("#submenu-container").last()

        if submenu_container:
            app_log.write("Before remove: ")
            app_log.write(submenu_container.children)
            if len(submenu_container.children) != 0:
                await submenu_container.remove_children("*")

        submenu_container = self.query("#submenu-container").last()
        app_log.write("After remove & before mount: ")
        app_log.write(submenu_container.children)

        new_id = f"o{option_id}"
        new_submenu = SubMenu(menu_id=new_id, id=new_id)
        await submenu_container.mount(new_submenu)

        new_submenu = submenu_container.query("OptionList").first()
        new_submenu.focus()

        app_log.write("After mount: ")
        app_log.write(submenu_container.children)
        app_log.write(new_submenu)


if __name__ == "__main__":
    app = UtilityContainers()
    app.run()
