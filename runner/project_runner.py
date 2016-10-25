import json
import os
import sys
import re
from functools import reduce

from util import file_utils

from colorama import Fore, Style


class ProjectRunner(object):
    def __init__(self, project_name, do_echo=True):
        self.path = os.path.join("skels", project_name)
        config_path = os.path.join(self.path, "config.json")
        if not os.path.exists(config_path):
            raise Exception("Project \"%s\" does not exist" % project_name)
        self.config = json.load(open(config_path))
        self.echo = do_echo
        pass

    def run(self):
        check = self.pre_run_checks()
        if not self.echo:
            self._render_check_status(check)
        if not check["value"]:
            print "Aborting"

            return

        check = self.prepare_utility_tables()
        if not self.echo:
            self._render_check_status(check)
        if not check["value"]:
            print "Aborting"

            return

        for step in self.config["steps"]:
            check = self.run_etl_step(step) if step["type"] == "etl" else self.run_test_step(step)
            pass

    @staticmethod
    def _render_check_status(status):
        ProjectRunner._render_header(status)
        [ProjectRunner._render_item(item) for item in status["results"]]

    @staticmethod
    def _render_header(status):
        print Style.BRIGHT + status["title"] + Style.RESET_ALL

    @staticmethod
    def _render_item(item):
        columns = 80
        item["label"] = item["label"].strip()
        item["label"] = re.sub('\s+', ' ', item["label"])

        pts = columns - 10 - len(item["label"])
        print item["label"] + ("." * pts) + "[" + \
              ((Fore.GREEN + "  OK  ") if item["value"] else (Fore.RED + " FAIL ")) \
              + Style.RESET_ALL + "]"
        if not item["value"] and "comment" in item and item["comment"]:
            print Fore.RED + item["comment"] + Style.RESET_ALL

    def prepare_utility_tables(self):

        return self.run_etl_step({
            "folder": "../../utility_skels",
            "label": "Creating utility tables"
        })

    def run_etl_step(self, step):
        output = {
            "title": step["label"],
            "results": []
        }

        if self.echo:
            self._render_header(output)

        folder = os.path.join(self.path, step["folder"])
        file_list = file_utils.get_files(folder)

        state = True
        for f in file_list:
            if self.echo:
                self._render_header({
                    "title": "-->Executing %s" % f
                })

            content = file_utils.readall(folder, f)
            result = self.run_sql_file(content)
            state = reduce((lambda x, y: bool(x) and bool(y["value"])), result)
            output["results"].append({
                "label": "Executing %s" % f,
                "value": state
            })

            output["results"] += result
            if not state:
                break

        output["value"] = state
        return output

    def run_sql_file(self, content):
        queries = re.split(";$", content, flags=re.MULTILINE)
        output = []
        for q in queries:
            q = q.strip()
            if not q:
                continue
            res = self._run_query(q)
            output.append(res)
            if self.echo:
                self._render_item(res)
            if not res["value"]:
                break

        return output

    def run_test_step(self, step):
        output = {
            "title": step["label"],
            "results": []
        }

        if self.echo:
            self._render_header(output)

        if self.echo:
            self._render_header({
                "title": "Tests calculation"
            })

        folder = os.path.join(self.path, step["folder"])
        file_list = file_utils.get_files(folder)
        state = True
        for f in file_list:
            if self.echo:
                self._render_header({
                    "title": "-->Executing %s" % f
                })
            content = file_utils.readall(folder, f)
            result = self.run_sql_file(content)
            state = reduce((lambda x, y: bool(x) and bool(y["value"])), result)
            output["results"].append({
                "label": "Executing %s" % f,
                "value": state
            })

            output["results"] += result
            if not state:
                break

        output["value"] = state

        if self.echo:
            self._render_header({
                "title": "Tests calculation"
            })

        query = self._run_query("SELECT * FROM unittest_status WHERE step='%s'" % step["folder"])

        for test in query["response"]["result"]:
            self._render_item({
                "label": "----->" + test[1],
                "value": bool(test[2]),
                "comment": test[3]

            })
            pass

        return output

    def pre_run_checks(self):
        result = True
        output = {
            "title": "Integrity checks",
            "results": []
        }
        if self.echo:
            self._render_header(output)
        steps = self.config["steps"]
        for step in steps:
            item = {
                "label": "Checking folder %s" % step["folder"],
                "comment": "",
                "value": os.path.exists(os.path.join(self.path, step["folder"]))
            }
            output["results"].append(item)
            if self.echo:
                self._render_item(item)

            result = result and item["value"]

        output["value"] = result
        return output

    def _run_query(self, query):
        import requests

        r = requests.post("http://%s:%s/query" % (self.config["server"]["host"], self.config["server"]["port"]), data={
            "query": query
        })

        resp = json.loads(r.text)

        return {
            "label": "----->%s" % query.lstrip()[:30],
            "value": False if resp["error"] else True,
            "comment": resp["error"],
            "response": resp
        }
