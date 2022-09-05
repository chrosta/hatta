# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from services.libs.core.Service import Service
#-------------------------------------------------------------------------------


class MyExample(Service):

    def __init__(self):
        super(Example, self).__init__()
        self.__service_params = {}
        self.__service_name = "my_example"
        self.__json_result = {};
        
    def service_name(self):
        return self.__service_name

    def get_result(self):
        return self.__json_resut
