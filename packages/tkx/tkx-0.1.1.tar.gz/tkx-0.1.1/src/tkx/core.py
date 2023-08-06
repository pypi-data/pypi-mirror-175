from __future__ import annotations
from tkinter import Widget
from typing import Any, Callable, Literal
from tkx.constants import (
    CSS_PROPERTY_NAME_TRANSLATIONS,
    INHERITED_PROPERTIES,
    NON_STYLE_CONFIG_OPTIONS,
)
from tkx.error import InvalidDisplayError
import re


translate_css = lambda x: CSS_PROPERTY_NAME_TRANSLATIONS.get(x)


class TkxElement:
    def __init__(self):
        super().__init__()
        self.__display: Literal["block", "flex", "grid", "none"] = "block"
        self.__parent: TkxElement | None = None
        self.__style: dict[str, str] | None = None
        self.__widget: Widget | None = None

    def add(self, widget: Widget, **kwargs):
        """
        Creates a new `Element` with the provided keyword arguments and
        adds it as a child of the caller. Returns the added `Element`.

        Parameters
        - widget: `tkinter.Widget` - Type of widget to be created.
        - `**kwargs` - Keyword arguments to use when creating the widget.

        The following CSS values can be passed as keyword arguments:
            * `color=...`
            * `width` / `height` `= "...%"`

        Under normal circumstances, tkinter's `Frame` widget does not
        accept the `fg` keyword argument. This is handled instead by tkx
        such that a container may define the default font color of Label
        widgets it contains.
        """
        from tkx.element import Element

        if self.elements is None:
            self.elements = []

        kwargs = parse_css_kwargs(self, **kwargs)
        element = Element(widget, self, **kwargs)
        self.elements.append(element)

        self.add_element(element)

        return element

    def add_element(self, element):
        if self.display == "block":
            element.widget.pack(fill="x")
            return

        if self.display == "flex":
            element.widget.grid(row=0, column=len(self.elements))
            return

        raise NotImplementedError()

    def get_style_of(self, name: str, fallback: str | None = None) -> dict[str, str] | None:
        """
        Returns the style dictionary associated with the given name if it
        can be found in the root window's stylesheet. Accepts an optional
        fallback name in case the former is not found.

        Parameters
        - name: `str` - The name to search for in the stylesheet.
        - fallback: `str | None` - Alternate style to search for if `name` isn't found.

        Returns `None` if no style is found.
        """
        if self.parent is not None:
            return self.parent.get_style_of(name) or self.parent.get_style_of(fallback) or None

        if self.stylesheet is None:
            return None

        if self.stylesheet.get(name) is None:
            return None

        # Return a copy of the style dictionary.
        return dict(self.stylesheet.get(name))

    def inherit_style(self) -> None:
        for p in INHERITED_PROPERTIES:
            if self.style.get(translate_css(p)) is None:
                if self.parent.style.get(translate_css(p)) is None:
                    continue

                self.style[translate_css(p)] = self.parent.style.get(translate_css(p))

    @property
    def display(self) -> Literal["block", "flex", "grid", "none"]:
        return self.__display

    @display.setter
    def display(self, value: Literal["block", "flex", "grid", "none"]) -> None:
        if value not in {"block", "flex", "grid", "none"}:
            raise InvalidDisplayError(
                f'"{value}" is not a valid value. Expected one of ("block", "flex", "grid", or "none")'
            )

        self.__display = value

    @property
    def parent(self) -> TkxElement:
        return self.__parent

    @parent.setter
    def parent(self, value: TkxElement) -> None:
        self.__parent = value

    @property
    def root(self):
        """Returns the root window."""
        if self.parent is None:
            return self
        return self.parent.root

    @property
    def style(self) -> dict[str, str] | None:
        """
        Returns the style dictionary associated with this object or
        creates a new `dict` and returns it.
        """
        # Create self.style if it doesn't already exist.
        if self.__style is None:
            self.__style = dict()
        return self.__style

    @style.setter
    def style(self, value: dict[str, str] | None) -> None:
        self.__style = value

    @property
    def widget(self) -> Widget | None:
        """Returns the widget associated with this object or `None`."""
        return self.__widget

    @widget.setter
    def widget(self, value: Widget) -> None:
        self.__widget = value

    @property
    def widget_name(self) -> str | None:
        """Returns the lowercase name of this object's widget or `None`."""
        if self.widget is not None:
            return re.search(r"\w+", str(self.widget).split(".")[-1])[0]
        return None

    def __getattr__(self, attr: str) -> Any | None:
        # If no attribute is found in self, check self.widget.
        if self[attr] is None and self.widget is not None:
            return getattr(self.widget, attr)
        return self[attr]

    def __getitem__(self, attr: str) -> Any | None:
        return self.__dict__.get(attr)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value


def parse_css_kwargs(obj, **kwargs) -> dict[str, str]:
    """
    Parse a set of keyword arguments as though they were
    CSS variables. Possible values include:
    * Percent values (`width: 50%` -> `width={self.parent|root}.width / 2`)
    """
    for k, v in kwargs.items():
        if "%" in str(v):
            percent = float(v.replace("%", ""))

            if obj.parent is not None:
                target = obj.parent

            else:
                target = obj.root

            amount = float(target.style[k])
            total = float(amount / 100) * percent
            kwargs[k] = str(int(total))

    return obj.root.stylesheet.format_properties(kwargs)


def update_style(fn):
    """
    Decorates the `configure` method of a class which inherits from
    `TkxElement`.

    Takes a style dictionary and/or keyword arguments, then parses
    the given values as CSS before configuring the widget wrapped by
    the caller. Dictionary values are overwritten by keyword arguments.

    #### The following examples require `--red` to be defined in the stylesheet.
    ### Example 1

    ```python
    my_element.configure(color="var(--red)")
    ```

    becomes `my_element.configure(fg="#f00")`

    ### Example 2

    ```python
    my_style = {"color": "var(--red)"}
    my_element.configure(my_style)
    ```

    becomes `my_element.configure(fg="#f00")`

    ### Example 3

    ```python
    my_style = {"color": "var(--red)"}
    my_element.configure(my_style, width=50)
    ```

    becomes `my_element.configure(fg="#f00", width=50)`
    """

    def func(self, args: dict[str, Any] | None = None, **kwargs) -> Callable:
        # If both a positional dictionary and keyword arguments
        # are provided, update the dictionary with the provided
        # keyword arguments.
        if args is not None:
            args.update(kwargs)
            kwargs = args

        # If there is no stylesheet or if no arguments exist, exit.
        if self.root.stylesheet is None or not any((args, kwargs)):
            return

        kwargs = parse_css_kwargs(self, **kwargs)

        self.style.update(kwargs)

        # Remove keys not associated with style.
        self.style = dict(filter(lambda i: i[0] not in NON_STYLE_CONFIG_OPTIONS, self.style.items()))

        # Call the original configure method.
        fn(self, **kwargs)

    return func
