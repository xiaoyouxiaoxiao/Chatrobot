from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class MyCryptConfig(AppConfig):
    name = 'my_crypt'

    # def ready(self):
    #     autodiscover_modules('FAQrobot.py')