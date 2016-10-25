import argparse
from project_runner import ProjectRunner

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('project', type=str, metavar='m')
args = parser.parse_args()
pr = ProjectRunner(args.project)
pr.run()
