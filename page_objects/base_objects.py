from time import sleep


class BasePage():

    def __init__(self, driver):
        self.driver = driver
        self.locator = BaseLocator()

    def click(self, location: [str, tuple]):
        """
        click ui element
            :param location: location method，it can be either the param name in locator or the exact value in the locator(tuple)
        """
        if type(location) == str:
            method, element_location = self.locator.get(location)
        elif type(location) == tuple:
            method, element_location = location
        element = self.__get_element(method, element_location)
        element.click()
        sleep(0.3)

    def input(self, text, location: [str, tuple]):
        """
        input text in ui element
            :param location: location method，it can be either the param name in locator or the exact value in the locator(tuple)
        """
        if type(location) == str:
            method, element_location = self.locator.get(location)
        elif type(location) == tuple:
            method, element_location = location
        element = self.__get_element(method, element_location)
        element.set_text(text)

    def swipe(self, location: [str, tuple], direction: str):
        """
        swipe ui element
            :param direction: swipe direction [up, down, left, right]
            :param location: location method，it can be either the param name in locator or the exact value in the locator(tuple)
        """
        if type(location) == str:
            method, element_location = self.locator.get(location)
        elif type(location) == tuple:
            method, element_location = location
        element = self.__get_element(method, element_location)
        element.swipe(direction)
        sleep(1)

    def is_exist(self, location) -> bool:
        """
        check if element exists
            :param location: location method，it can be either the param name in locator or the exact value in the locator(tuple)
        """
        if type(location) == str:
            method, element_location = self.locator.get(location)
        elif type(location) == tuple:
            method, element_location = location
        return self.__get_element(method, element_location).wait(2.0)

    def get_element(self, location):
        """
        get element
            :param location: location method，it can be either the param name in locator or the exact value in the locator(tuple)
        """
        if type(location) == str:
            method, element_location = self.locator.get(location)
        elif type(location) == tuple:
            method, element_location = location
        return self.__get_element(method, element_location)

    def __get_element(self, method, location):
        """
        get element by location and method
            :param method: location method, text, resouce_id, xpath, class_name only
            :param location: the value matches the method 
        """
        if method == "text":
            element = self.driver(text=location)
        elif method == 'resource_id' or method == 'resourceid' or method == 'resourceId':
            element = self.driver(resourceId=location)
        elif method == "xpath":
            element = self.driver.xpath(location)
        elif method == "class_name" or method == 'classname' or method == 'className':
            element = self.driver(className=location)
        else:
            raise Exception(
                "only support 'text, resouce_id, xpath, class_name'")
        return element


class BaseLocator():
    def get(self, name):
        return self.__getattribute__(name)


class BasePageCreator():

    def __init__(self, driver):
        self.driver = driver

    def get(self, name):
        if name in self.name_page_rel_dict.keys():
            return self.name_page_rel_dict.get(name)(self.driver)
        else:
            raise Exception(f"{name} is not defined")
