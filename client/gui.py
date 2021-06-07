import kivy             # Paket fuer die GUI
import time
import datetime
import os
import requests

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock
from kivy.config import Config


class GUI:

    def __init__(self):
        Config.set('graphics', 'borderless', 1)
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'width', '480')
        Config.set('graphics', 'height', '320')

    def update(self, time_data):
        """
        :param dict time_data: (time_data is received as a dict the same as in timedata.example.json)
        :return:
        """
        pass