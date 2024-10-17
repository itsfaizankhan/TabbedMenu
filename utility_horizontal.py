from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer
from textual.widgets import OptionList as OptionL
from textual.widgets import RichLog, Static
from textual.widgets.option_list import Option

SIDEBAR_OPTIONS = [Option(f"Menu {i}", id=str(i)) for i in range(1, 10)]


class OptionList(OptionL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    BINDINGS = [
        Binding("k", "cursor_up", "Move up"),
        Binding("j", "cursor_down", "Move down"),
    ]


class Sidebar(Vertical):
    """Side dock containing main list."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            *SIDEBAR_OPTIONS,
            classes="box",
            id="sidebar",
        )


class SubMenu(Static):
    def __init__(self, menu_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_id = menu_id

        self.SUBMENU_OPTIONS = [
            Option(f"Menu {self.menu_id} Option {str(i)}") for i in range(1, 10)
        ]

    def compose(self) -> ComposeResult:
        yield OptionList(
            *self.SUBMENU_OPTIONS,
            classes="box",
            id=f"{self.menu_id}-menu",
        )


class UtilityContainers(App):
    CSS_PATH = "utility_horizontal.css"

    BINDINGS = [
        Binding("left", "focus_previous('*')", "Move back"),
        Binding("backspace", "focus_previous('box')", "Go to previous menu", show=True),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar(classes="column")
            yield Vertical(
                SubMenu(menu_id="o1", id="o1"),
                id="submenu-container",
                classes="column",
            )
            yield RichLog(highlight=True, markup=True)
            yield Footer()

    async def on_option_list_option_selected(
        self, event: OptionList.OptionSelected
    ) -> None:
        """Event handler called when an option in OptionList is selected."""
        option_id = event.option.id
        # app_log = self.query_one(RichLog).write

        # NOTE: The condition `or len(option_id) >= 4` can be used below condition to handle nested
        # submenus, where the length of `option_id` increases with each deeper submenu level.
        # The value compared with `option_id` length should correspond to the number of
        # submenu levels to prevent empty submenus. Though not thoroughly tested, this has
        # been observed to cause empty submenus when a great number of menus are created on the same level.
        if not option_id:
            return

        # app_log(option_id)

        # ==== Handeling mount and removal of SubMenu. ====
        submenu_container = self.query("#submenu-container").last()

        # Remove any submenu widget in the Vertical widget.
        if submenu_container:
            # app_log("Before remove: ")
            # app_log(submenu_container.children)
            if len(submenu_container.children) != 0:
                await submenu_container.remove_children("*")

        submenu_container = self.query("#submenu-container").last()
        # app_log("Before mount: ")
        # app_log(submenu_container.children)

        # Mount (add) the submenu corresponding to the selected sidebar option.
        try:
            selected_option_name = (
                self.query("#sidebar").last().get_option(option_id).prompt
            )
            # app_log("Selected option was:")
            # app_log(selected_option_name)
        except Exception as e:
            self.notify(e.__str__(), severity="error")

        new_id = f"o{option_id}"
        new_submenu = SubMenu(menu_id=new_id, id=new_id)
        if selected_option_name:
            new_submenu.border_title = selected_option_name

        await submenu_container.mount(new_submenu)

        # Change focus from sidebar OptionList to the newly mounted submenu.
        new_submenu = submenu_container.query("OptionList").first()
        new_submenu.focus()

        # app_log("After mount: ")
        # app_log(submenu_container.children)
        # app_log(new_submenu)


if __name__ == "__main__":
    app = UtilityContainers()
    app.run()
