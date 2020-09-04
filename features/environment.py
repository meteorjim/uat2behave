import datetime
import os
from time import sleep
from configparser import ConfigParser

import uiautomator2

import page_objects

def before_feature(context, feature):
    conf = ConfigParser()
    conf.sections()
    conf.read("uat2.conf", encoding="utf8")
    if conf["base_conf"]["connect_method"] == "usb":
        context.driver = uiautomator2.connect_usb()
    elif conf["base_conf"]["connect_method"] == "wifi":
        context.driver = uiautomator2.connect_wifi(conf["base_conf"]["wifi_address"])
    else:
        raise Exception("wifi and usb only")
    context.need_screen_shot = True if conf["base_conf"]["screen_shot_switch"] == "on" else False
    context.package_name = conf["project_conf"]["package_name"]
    context.project_name = conf["project_conf"]["project_name"]
    context.feature_name = feature.name
    context.page_creator = getattr(page_objects, context.project_name[0].upper() + context.project_name[1:] + "PageCreator")(context.driver)
    context.driver.implicitly_wait(5)
    context.test_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    context.custom_param_dict = {}
    context.steps_recorder = {}
    context.steps_recorder_switch = False
    context.temp_steps = []


def before_scenario(context, scenario):
    context.scenario_name = scenario.name
    pass


def after_feature(context, feature):
    context.driver.app_stop(context.package_name)


def after_step(context, step):
    if context.steps_recorder_switch and step.name != "start record steps":
        context.temp_steps.append("{} {}".format(step.step_type, step.name))
    if context.need_screen_shot and "save above steps as" not in step.name  and "start record steps" not in step.name:
        sleep(0.3)
        screen_shot = context.driver.screenshot()
        w, h = screen_shot.size
        screenshot_dir = f"screenshots/[{context.test_time}]{context.feature_name}/{context.scenario_name}"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        file_name = str(step.line) + "_" + step.name.replace(" ", "_")
        screen_shot.resize((int(w/4), int(h/4))).save(screenshot_dir+f"/{file_name}.jpg")
    else:
        pass
