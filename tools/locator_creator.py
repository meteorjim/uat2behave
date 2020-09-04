import re

all_locations = """
d(resourceId="com.foo.bar:id/et_hello")
d(resourceId="com.foo.bar:id/txt_bar")
d(resourceId="com.foo.bar:id/btn_foo")
"""
def find_resource(string):
    url = re.findall('(?:[a-zA-Z0-9-\w:\/\ .])+', string)
    return url

for one_location in all_locations.split("\n"):
    if len(one_location) < 5:
        continue
    if "xpath" in one_location:
        print('     = "xpath", "{}"'.format(one_location.split("'")[1]))
    elif "=" in one_location:
        _, locate_method, location = find_resource(one_location)
        print('     = "{}", "{}"'.format(locate_method, location))
