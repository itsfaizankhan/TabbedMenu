from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, RichLog, Static
from textual.widgets.option_list import Option, Separator


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


class MenuContainer(Vertical):
    def compose(self) -> ComposeResult:
        for i in range(10):
            yield OptionList(
                Option(f"Menu {i+1} Option 1"),
                Option(f"Menu {i+1} Option 2"),
                Option(f"Menu {i+1} Option 3"),
                Option(f"Menu {i+1} Option 4"),
                Option(f"Menu {i+1} Option 5"),
                Option(f"Menu {i+1} Option 6"),
                Option(f"Menu {i+1} Option 7"),
                Option(f"Menu {i+1} Option 8"),
                Option(f"Menu {i+1} Option 9"),
                classes="box hidden",
                id=f"o{i+1}-menu",
            )

        # yield OptionList(
        #     Option("Option 1"),
        #     Option("Option 2"),
        #     Option("Option 3"),
        #     Option("Option 4"),
        #     Option("Option 5"),
        #     Option("Option 6"),
        #     Option("Option 7"),
        #     Option("Option 8"),
        #     Option("Option 9"),
        #     classes="box",
        #     id="o2-menu",
        # )


class UtilityContainers(App):
    CSS_PATH = "utility_horizontal.css"

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar(classes="column")
            yield MenuContainer(classes="column")
            yield RichLog(highlight=True, markup=True)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Event handler called when an option in OptionList is selected."""
        option_id = event.option.id
        app_log = self.query_one(RichLog)

        if not option_id or len(option_id) >= 4:
            return

        app_log.write(option_id)
        menus = self.query(OptionList).exclude("#sidebar")

        menu_to_hide = menus.exclude(".hidden")
        for menu in menu_to_hide:
            menu.add_class("hidden")

        menu_to_show = menus.filter(f"#o{option_id}-menu").first()
        menu_to_show.remove_class("hidden")
        menu_to_show.focus()

        app_log.write(menu_to_show)

        # result = self.query_one(f"#o{option_id}-menu")
        # app_log.write(result)
        # result.focus(scroll_visible=True)


if __name__ == "__main__":
    app = UtilityContainers()
    app.run()
