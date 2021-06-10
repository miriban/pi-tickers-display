import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config


class GUI(App):

    def __init__(self, get_timedata_callback, **kwargs):
        super(GUI, self).__init__(**kwargs)
        Config.set('graphics', 'borderless', 1)
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'width', '480')
        Config.set('graphics', 'height', '320')
        self.set_share_screen = 1
        self._load_builder()
        self.screen_manager = ScreenManager()
        self.etfs_screen = EtfsScreen(get_timedata_callback, name='ETFs')
        self.screen_manager.add_widget(self.etfs_screen)

    def build(self):
        self.etfs_screen.update_etfs()
        return self.screen_manager

    def _load_builder(self):
        Builder.load_string('''
# Aufbau des Hauptfenster zur Anzeige der Aktien
<EtfsScreen>:
    # Name und ID definieren
    name: 'ETFs'
    id: screen   
    # Layout und Hintergrundfarbe festlegen
    BoxLayout:   
        orientation: 'vertical'
        canvas:      
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'horizontal'
            height: 40   
            size_hint_y: None
            # Erzeugen eines Labels
            Label:
                # ID zur veraenderung des Textes durch das Programm
                id: label_headline  
                text: 'Aktien Werte'
                # Fettschrift
                bold: True         
                color: 1, 1, 1, 1
                # Schriftgroesse
                font_size: 25     
            Label:
                id: label_time                                                                                          
                text:
                color: 1, 1, 1, 1
                font_size: 25
        BoxLayout:
            orientation: 'horizontal'
            canvas:
                Color:
                    rgba: 0, 0, 1, 0.5
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: Label_1
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_2
                    text:
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_3
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_4
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_5
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: Label_1_2
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_2_2
                    text:
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_3_2
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_4_2
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
                Label:
                    id: Label_5_2
                    text: 
                    color: 1, 1, 1, 1
                    font_size: 25
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            # Hoehe festlegen
            height: 40
            canvas:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                orientation: 'vertical'
                canvas:
                    Color:
                        rgba: 0, 0, 1, 0.5
                    Rectangle:
                        pos: self.pos
                        size: self.size        
            Label:
                id: label_date
                text:
                color: 1, 1, 1, 1
                size_hint_x: None
                # Breite
                width: 100
                font_size: 20
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 20
            Label:
                id: label_footnote
                text: 'Abuiriban, Decker, A. Sammour, M. Sammour'
                size_hint_y: None
                text_size: self.size
                # Ausrichtung des Textes
                halign: 'left'
                font_size: 15
        ''')


class EtfsScreen(BoxLayout, Screen):

    def __init__(self, get_timedata_callback, **kwargs):
        super(EtfsScreen, self).__init__(**kwargs)
        self.get_timedata = get_timedata_callback
        update_time_event = Clock.schedule_interval(self.update_time, 0.5)
        self.bind(x=update_time_event, y=update_time_event)
        update_etfs_event = Clock.schedule_interval(self.update_etfs, 5)
        self.bind(x=update_etfs_event, y=update_etfs_event)

    def update_etfs(self, *kwargs):
        data_to_show = []
        etfs_time_data = self.get_timedata()
        for key, value in etfs_time_data.items():
            if 'code' in value:
                print("error => ", value['message'])
            else:
                symbol = value['meta']['symbol']
                try:
                    if 'currency_base' in value['meta']:
                        currency = ''
                    else:
                        currency = '€' if value['meta']['currency'] == 'EUR' else '$'
                except:
                    currency = '$'
                values = value['values'][0]
                open_value = '%.2f' % float(values['open'])
                data_to_show.append({'name': symbol, 'value': open_value+currency})
        # draw on screen
        for index, etf in enumerate(data_to_show[:5]):
            self.ids["Label_%s" % (index + 1,)].text = etf['name']
            self.ids["Label_%s_2" % (index + 1,)].text = etf['value']

    def update_time(self, *kwargs):
        """
        Update time on screen
        :param kwargs:
        :return:
        """
        self.ids["label_time"].text = (datetime.datetime.now().strftime('%H:%M:%S'))
        self.ids["label_date"].text = (datetime.datetime.now().strftime('%d.%m.%Y'))