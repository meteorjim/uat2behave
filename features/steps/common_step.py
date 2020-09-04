import uiautomator2
from time import sleep
from behave import Given, Then, When

@Given("start record steps")
def steps_recorder_start(context):
    context.steps_recorder_switch = True


@Given("save above steps as {step_commands}")
def steps_recorder_stop(context, step_commands):
    context.steps_recorder_switch = False
    context.steps_recorder[step_commands] = context.temp_steps
    context.temp_steps = []


@Given("started application")
def start_app(context):
    __import__("features.steps", "{}_step".format(context.project_name))
    context.driver.app_start(context.package_name)


@Given("replay {step_commands}")
def replay_user_commands(context, step_commands):
    for one_step in context.steps_recorder[step_commands]:
        context.execute_steps(one_step)


@Then("it is {page_name}")
def check_current_page(context, page_name):
    page_name = page_name.replace(" ", "_")
    context.current_page = context.page_creator.get(page_name)


@When("click {something}")
def common_click(context, something):
    new_page = context.current_page.click(something)
    if new_page:
        context.current_page = new_page


@When("input {somewords} into {somewhere}")
def common_input(context, somewords, somewhere):
    context.current_page.input(somewords, somewhere)


@When("swipe {something} {direction}")
def common_swipe(context, something, direction):
    context.current_page.swipe(something, direction)


@When("I {page_method}")
def exec_page_obj_method(context, page_method):
    method_name = page_method.replace(" ", "_")
    new_page = context.current_page.__getattribute__(method_name)()
    if new_page:
        context.current_page = new_page


@When("go back")
def go_back(context):
    context.driver.press("back")
    sleep(1)


@Then("{location_name} should be {something}")
def element_check(context, location_name, something):
    element = context.current_page.get_element(location_name)
    assert(str(element.info["text"]) == something)


@Then("{location_name} should not be {something}")
def element_check_not(context, location_name, something):
    element = context.current_page.get_element(location_name)
    assert(str(element.info["text"]) != something)


@When("save {locator_name} text into {param_name}")
def save_param_from_ui(context, locator_name, param_name):
    context.custom_param_dict[param_name] = context.current_page.get_element(locator_name).info["text"]


@When("define {param_name} = {value}")
def define_custom_param(context, param_name, value):
    context.custom_param_dict[param_name] = value
