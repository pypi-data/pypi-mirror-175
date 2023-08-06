"""
Contains a `ProcessRequest` class to process and get a response
from a given route and requested method. Use to process client requests.
"""

import http_pyparser
from typing import List, Union

from .route import Route
from .status import status
from .server import Client


class ProcessRequest:
    def __init__(self, routes: List[Route]) -> None:
        self._routes = routes

    def process(self, client: Client) -> Union[http_pyparser.Response, bool]:
        """Process and get or create a response to
        specified path and requested method.

        The HTTP message is obtained by `Client`
        class; the `http_pyparser` library parse this
        and return a class with HTTP data.

        :param client: A `Client` instance
        :type client: Client
        :return: Return request response
        :rtype: Union[http_pyparser.Response, bool]
        """

        # get client request
        message = client.get_message()

        if not message:
            client.destroy()
            response = False
        else:
            http_parser = http_pyparser.parser.HTTPParser()
            request = http_parser.parser(message)

            match_route: Route = None

            # checking routes
            for route in self._routes:
                if route.match_route(request.path):
                    match_route = route
                    break

            # make route response
            if match_route:
                if route.accept_method(request.method):
                    response = route.get_route_response(request)
                else:
                    response = http_pyparser.response.Response(
                        body='Method Not Allowed',
                        status=status.method_not_allowed_405
                    )
            else:
                response = http_pyparser.response.Response(
                    body='Not Found',
                    status=status.not_found_404
                )

        return response
