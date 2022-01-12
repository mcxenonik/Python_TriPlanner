from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# from kivy.uix.tabbedpanel import TabbedPanel
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.lang import Builder
# from kivy.app import App

from kivymd.app import MDApp
from kivymd.uix.list import ILeftBody, OneLineListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime, timedelta

import Model

import sqlite3

items_list = {}
control_ids = []

# Define different screens
class MenuScreen(Screen):
    def on_button_press(self, instance):
        print('The button <%s> is being pressed' % instance.text)


class NewTripScreen(Screen):
    def on_save(self, instance, value, data_range):
        print(str(data_range[0]), str(data_range[-1]))
        self.ids.dataRangeLabel.text = f'{data_range[0]}'
        self.ids.dataRangeLabelEnd.text = f'{data_range[-1]}'
        trip_length = (data_range[-1] - data_range[0]).days
        print(trip_length)

        start_day = (data_range[0] - datetime.today().date()).days
        print(start_day)

    def on_cancel(self, instance, value):
        pass

    def on_date_button_press(self):
        min_date = datetime.today().date()
        max_date = min_date + timedelta(days=7)
        date_dialog = MDDatePicker(mode="range",min_date=min_date, max_date=max_date)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_button_prepare_list_press(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        data = {
            "accomodation_type": "",
            "trip_length": 0,
            "start_day": 0,
            "attracts": []
            }

        days_of_week = {
            "Poniedziałek": 0,
            "Wtorek": 1,
            "Środa": 2,
            "Czwartek": 3,
            "Piątek": 4,
            "Sobota": 5,
            "Niedziela": 6
            }
        
        data["dataX"] = float(self.ids.cityX.text)
        data["dataY"] = float(self.ids.cityY.text)

        today = datetime.today()
        start_date = datetime.strptime(self.ids.dataRangeLabel.text, '%Y-%m-%d')
        end_date = datetime.strptime(self.ids.dataRangeLabelEnd.text, '%Y-%m-%d')


        data["trip_length"] = (end_date - start_date).days
        data["accomodation_type"] = self.ids.accomodation_type.text
        data["start_day"] = (start_date - today).days + 1

        if( self.ids.chck0.active == True):
            data["attracts"].append(self.ids.lbl0.text)

        if( self.ids.chck1.active == True):
            data["attracts"].append(self.ids.lbl1.text)

        if( self.ids.chck2.active == True):
            data["attracts"].append(self.ids.lbl2.text)

        if( self.ids.chck3.active == True):
            data["attracts"].append(self.ids.lbl3.text)

        if( self.ids.chck4.active == True):
            data["attracts"].append(self.ids.lbl4.text)

        if( self.ids.chck5.active == True):
            data["attracts"].append(self.ids.lbl5.text)

        print(data)

        global items_list
        items_list = Model.prepare_items_list((data["dataY"], data["dataX"]), data["start_day"], data["trip_length"], data["accomodation_type"], data["attracts"])
        



class MyTripsScreen(Screen):
    def on_button_press(self, instance):
        print('The button <%s> is being pressed' % instance.text)


class WorldMapScreen(Screen):
    def on_release_button(self, instance):
        if(self.ids.place_name.text != ""):
            city_name = self.ids.place_name.text
            city_cords = Model.get_city_cords_by_city_name(city_name)

            if(city_cords is not None):

                self.ids.mapview.center_on(city_cords[0], city_cords[1])

                self.ids.place_lat.text = ""
                self.ids.place_lon.text = ""
                self.ids.mapview.zoom = 10

        elif(self.ids.place_lat.text != "" and self.ids.place_lat.text != ""):
            self.ids.mapview.center_on(int(self.ids.place_lat.text), int(self.ids.place_lon.text))

            self.ids.place_lat.text = ""
            self.ids.place_lon.text = ""
            self.ids.mapview.zoom = 10

    def on_text_val(self, instance, value):
        print('The widget', instance, 'have:', value)


class Content(BoxLayout):
    # pass
    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)

        # items_list = Model.get_items_list()
        global control_ids
        da = items_list[category]
        
        if(type(da) == int):
            HB = BoxLayout(orientation='horizontal')
            line = OneLineListItem(text=f'Ilość: ', size_hint=(.5, None), height = 30, font_style='Caption')
            HB.add_widget(line)
            txtInput = TextInput(text = f'{items_list[category]}', size_hint=(.5, None), height = 30)
            HB.add_widget(txtInput)
            self.add_widget(HB)

        if(type(da) == dict):
            for d in da:
                HB = BoxLayout(orientation='horizontal')
                line = OneLineListItem(text=f'{d}', size_hint=(.5, None), height = 30, font_style='Caption')
                HB.add_widget(line)
                txtInput = TextInput(text = f'{da[d]}', size_hint=(.5, None), height = 30)
                HB.add_widget(txtInput)
                self.add_widget(HB)

        if(type(da) == list):
            for d in da:
                HB = BoxLayout(orientation='horizontal', size_hint=(1, 1))
                line = OneLineListItem(size_hint=(.8, None), height = 30, font_style='Caption')
                chckBox = CheckBox(size_hint=(.5, None), height = 30, color = [0,1,164/255,1])
                HB.add_widget(line)
                HB.add_widget(chckBox)
                self.add_widget(HB)


class ItemsListScreen(Screen):
    def on_button_press(self):
        # Create Database or Connect to One
        conn = sqlite3.connect('first_db.db')

        # Create A Cursor
        c = conn.cursor()

        da = items_list[category]
        
        

        # Add A Record
        c.execute("INSERT INTO trips VALUES (:first)",
            {
                'first': "self.ids.word_input.text",
                'second':" self.ids.word_input.text",
                'third': " self.ids.word_input.text",
            })

        # Commit our changes
        conn.commit()

        # Close connections
        conn.close()

    def on_pre_enter(self, *args):
        print(items_list)
        for cat in items_list:
            panel = MDExpansionPanel(content=Content(cat), panel_cls=MDExpansionPanelOneLine(text=cat))

            self.ids.itemsList.add_widget(panel)

        return super().on_pre_enter(*args)


class ScreensManager(ScreenManager):
    pass


class TriPlannerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        

        # Designate .kv design file
        # kv = Builder.load_file("triplanner.kv")

        # return kv
        # Create Database or Connect to One
        conn = sqlite3.connect('first_db.db')

        # Create Cursor
        c = conn.cursor()

        # Creat Table
        c.execute("""CREATE TABLE if not exists trips(
            name text)
        """)

        # Commitchanges
        conn.commit()

        # Close connections
        conn.close()

        sm = ScreenManager()
        sm.add_widget(MenuScreen())
        sm.add_widget(NewTripScreen())
        sm.add_widget(MyTripsScreen())
        sm.add_widget(WorldMapScreen())
        sm.add_widget(ItemsListScreen())

        return sm


if __name__ == '__main__':
    TriPlannerApp().run()
