import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from pyhive import hive
from TCLIService.ttypes import TOperationState
import json

app_config = json.load(open("config.json", "r"))


class HiveWebProxy(object):
    def __init__(self, config):
        self.url_map = Map([
            Rule('/', endpoint='index'),
            Rule('/query', endpoint='query')
        ])

        self.cursor = hive.connect(
            host=config["host"],
            port=10000,
            username=config["user"],
            database=config["database"],
            auth="NONE"
        ).cursor()

        pass

    def on_query(self, request):
        out_json = {}
        query = request.form.get("query", None)
        if not query:
            out_json = {
                "error": "No query provided"
            }
        else:
            try:
                self.cursor.execute(query, async=True)
                log = ""
                status = self.cursor.poll().operationState
                while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
                    logs = self.cursor.fetch_logs()
                    for message in logs:
                        log += message

                    # If needed, an asynchronous query can be cancelled at any time with:
                    # cursor.cancel()

                    status = self.cursor.poll().operationState

                out_json["message"] = log
                out_json["status"] = status
                out_json["error"] = ""

                if query.lower().startswith("select "):
                    out_json["result"] = self.cursor.fetchall()
            except Exception as e:
                out_json["error"] = e.message.status.errorMessage

        return Response(json.dumps(out_json), headers={
            "Content-Type": "application/json"
        })

    def on_index(self):
        return Response('Hello World!')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = HiveWebProxy(app_config["hive"])
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple(
        app_config["server"]["bind_address"],
        int(app_config["server"]["port"]),
        app,
        use_debugger=True,
        use_reloader=True
    )
