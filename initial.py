import os
import sys
import argparse
import configparser


if __name__ == "__main__":
    if not os.path.exists("features") or not os.path.exists("page_objects"):
        raise Exception("please change dir to uat2 program root to run the command")
    parser = argparse.ArgumentParser(description='init new autotest project')
    parser.add_argument("-n", "--name", help="application name(short name recommended) eg: ytb", required=True)
    parser.add_argument("-p", "--package", help="application package eg:com.google.youtube", required=True)
    args = parser.parse_args()
    package_name = args.package
    sname = args.name.lower()
    class_name = sname[0].upper()+sname[1:]
    # check if features/steps/sname_step.py exists
    if os.path.exists("features/steps/{}_step.py".format(sname)):
        raise Exception("features/steps/{}_step.py, exists, please use it or delete it and retry".format(sname))
    # check if page_objects/sname exists
    if os.path.exists("page_objects/{}".format(sname)):
        raise Exception("page_objects/{} exists, please use it or delete it and retry".format(sname))

    # create sname_step.py in  features/steps
    with open("features/steps/{}_step.py".format(sname), "w", encoding="utf8") as f:
        f.write("from behave import Given, Then, When")
    # create folder "sname" in page_objects, create locators.py(import *), pages.py, __init__.py in sname folder
    os.makedirs("page_objects/{}".format(sname))

    with open("page_objects/{}/locators.py".format(sname), "w", encoding="utf8") as f:
        f.write('from page_objects.base_objects import BaseLocator\n\n\nclass SampleLocator(BaseLocator):\n    btn_sample = "resourceId", "com.google.btn:id/login"')

    with open("page_objects/{}/pages.py".format(sname), "w", encoding="utf8") as f:
        f.write("""from time import sleep\nfrom page_objects.base_objects import BasePage\nfrom page_objects.{}.locators import *\n\n\nclass SamplePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = SampleLocator()
        """.format(sname))
    with open("page_objects/{}/__init__.py".format(sname), "w", encoding="utf8") as f:
        f.write("""from page_objects.{}.pages import *
from page_objects.base_objects import BasePageCreator


class {}PageCreator(BasePageCreator):
    name_page_rel_dict = {{"sample page": SamplePage}}
        """.format(sname, class_name))
    # change package_name as package_name and project_name as sname in uat2.conf ,
    conf = configparser.ConfigParser()
    conf.sections()
    conf.read("uat2.conf", encoding="utf8")
    conf["project_conf"]["project_name"] = sname
    conf["project_conf"]["package_name"] = package_name
    with open("uat2.conf","w") as f:
        conf.write(f)