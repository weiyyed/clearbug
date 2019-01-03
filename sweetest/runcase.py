from sweetest.autotest import Autotest
import sys

def build (project_name, sheet_name, desired_caps, server_url):
    sweet = Autotest(project_name, sheet_name, desired_caps, server_url)
    sweet.plan()