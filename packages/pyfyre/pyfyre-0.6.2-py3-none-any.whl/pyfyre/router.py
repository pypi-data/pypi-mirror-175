from settings import ROUTES
from typing import Dict, Callable, Optional
from browser import document, window, DOMEvent
from pyfyre.events import window_event_listener
from pyfyre.nodes import Node, Element, TextNode


class RouteManager:
    """A static class that enables navigation between various views in a PyFyre application."""

    _routes_builder: Dict[str, Callable[[], Node]] = {}
    _routes: Dict[str, Optional[Node]] = {}
    _root_node = document.select_one("#root")

    @staticmethod
    def initialize(routes: Dict[str, Callable[[], Node]]) -> None:
        """:meta private:"""
        RouteManager._routes_builder = routes

        @window_event_listener("popstate")
        def onpopstate(event: DOMEvent) -> None:
            RouteManager.change_route(window.location.pathname)

    @staticmethod
    def parse_route(route_name: str) -> str:
        """Parse the ``route_name`` to turn it into a valid route name.

        Examples:
            | ``home`` -> ``/home``
            | ``contact/`` -> ``/contact``
            | ``about/this`` -> ``/about/this``
            | ``https://pyfyre.app/`` -> ``/``
            | ``https://pyfyre.app/about`` -> ``/about``
        """

        el = document.createElement("a")
        el.href = route_name
        route_name = str(el.pathname)

        if route_name == "/":
            return route_name

        return str(el.pathname).rstrip("/")

    @staticmethod
    def get_node(route_name: str, *, parse_route: bool = True) -> Node:
        """Get the corresponding ``Node`` of the ``route_name``.

        Args:
            parse_route: Whether to call the
                ``RouteManager.parse_route`` method on the ``route_name``.

        Returns:
            The corresponding ``Node`` of the ``route_name``.
            If the route doesn't exist, the default will be returned
            which has a 404 message.
        """

        if parse_route:
            route = RouteManager.parse_route(route_name)

        node = RouteManager._routes.get(route)

        if node is None:
            route_builder = RouteManager._routes_builder.get(route)
            node = route_builder() if route_builder else None
            RouteManager._routes[route] = node

            if isinstance(node, Element):
                node.build_children()

        return node or Element("p", lambda: [TextNode("404: Page Not Found :(")])

    @staticmethod
    def render_route(route_name: str) -> None:
        """:meta private:"""
        node = RouteManager.get_node(route_name)
        RouteManager._root_node.clear()
        RouteManager._root_node.attach(node.dom)

    @staticmethod
    def change_route(route_name: str) -> None:
        """Change the current route to ``route_name``.

        This method is typically not used directly.
        Use the ``pyfyre.nodes.RouterLink`` instead.
        """
        route = RouteManager.parse_route(route_name)
        route_data = ROUTES.get(route) or {"title": "404: Page Not Found :("}

        document.title = route_data.get("title")
        RouteManager.render_route(route)
