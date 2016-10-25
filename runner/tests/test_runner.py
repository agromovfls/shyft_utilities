import unittest
from runner.project_runner import ProjectRunner
from StringIO import StringIO
import sys
import mock


class TestProjectRunner(unittest.TestCase):

    def test_constructor(self):
        pr = ProjectRunner("shyft")

        def throw_exception():
            pr = ProjectRunner("unexistant")
        self.assertRaises(Exception, throw_exception)

        pass

    def test__render_status(self):
        head = "Some test"
        pr = ProjectRunner("shyft")
        out = StringIO()
        sys.stdout = out
        pr._render_header({"title": head})
        self.assertIn(head, out.getvalue().strip())

    def test__render_item(self):
        item_s = {
            "label": "item_s",
            "value": 1
        }
        item_r = {
            "label": "item_r",
            "value": 0,
            "comment": "comment"
        }
        pr = ProjectRunner("shyft")
        out = StringIO()
        sys.stdout = out
        pr._render_item(item_s)

        out_str = out.getvalue().strip()

        self.assertIn(item_s["label"], out_str)
        self.assertIn("OK", out_str[-15:])

        pr._render_item(item_r)
        out_str = out.getvalue().strip()
        self.assertIn(item_r["label"], out_str)
        self.assertIn("FAIL", out_str)
        self.assertIn(item_r["comment"], out_str)

    @mock.patch('runner.project_runner.ProjectRunner.run_etl_step', return_value=None)
    def test_prepare_utility_tables(self, mk_run):
        pr = ProjectRunner("shyft")
        pr.prepare_utility_tables()
        mk_run.assert_called_once_with({
            "folder": "../../utility_skels",
            "label": "Creating utility tables"
        })

    @mock.patch("requests.post")
    def test__run_query(self, mk_post):

        class CorrectReturn:
            text = """
            {
                "status": 2,
                "error": "",
                "message": ""
            }
            """

        class ErrorReturn:
            text = """
            {
                "status": 2,
                "error": "Something gone wrong",
                "message": ""
            }
            """

        pr = ProjectRunner("shyft")

        mk_post.return_value = CorrectReturn()

        res = pr._run_query("SOME PSEUDO QUERY")

        self.assertEquals(res["value"], 1)
        self.assertEquals(res["comment"], "")
        self.assertEquals(res["response"]["status"], 2)

        mk_post.return_value = ErrorReturn()

        res = pr._run_query("SOME PSEUDO QUERY")

        self.assertEquals(res["value"], 0)
        self.assertEquals(res["comment"], "Something gone wrong")
        self.assertEquals(res["response"]["status"], 2)

        pass
