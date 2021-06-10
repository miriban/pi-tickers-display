import os
import json
import time

from client.firebase_rest_client import Firebase
from client.twelve_data_client import TwelveDataClient
from client.gui import GUI


class Manager:
    TMP_USER_FILENAME = os.getcwd() + "/user.tmp"

    def __init__(self):
        self.user_id = ''
        self.twelve_data_client = TwelveDataClient()
        self.gui = GUI(get_timedata_callback=self.get_time_Date)

    def start(self):
        user = self._get_user()
        while user is None:
            self.user_id = self._ask_user_for_code()
            user = self._get_user()
            if user is None:
                print("code %s was not found!" % (self.user_id,))
                self._remove_user_file_if_exist()
            else:
                self._save_user(user)
        print("Successfully connected!")
        print("Etfs detected => " + ','.join(user['etfs']))

    def watch(self, with_gui=True):
        if with_gui:
            self.gui.run()
        else:
            while 1:
                try:
                    etfs = Firebase.get_user_etfs(self.user_id)
                    time_data = self.twelve_data_client.get_time_series(etfs)
                    for key, value in time_data.items():
                        if 'code' in value:
                            print("error => ", value['message'])
                        else:
                            values = value['values'][0]
                            print("%s => (open: %s, close: %s, datetime: %s)" % (key, values['open'],
                                                                                 values['close'],
                                                                                 values['datetime']))
                    print("---------------------- ******** ----------------------")
                except Exception as e:
                    print("error => " + str(e))
                time.sleep(10)

    def get_time_Date(self):
        etfs = Firebase.get_user_etfs(self.user_id)
        return self.twelve_data_client.get_time_series(etfs)

    def _ask_user_for_code(self):
        if not os.path.exists(Manager.TMP_USER_FILENAME):
            user_id = input("Please enter your connection code (0000000-0000): ")
            with open(Manager.TMP_USER_FILENAME, 'w') as tmp_file:
                json.dump({'code': user_id}, tmp_file)
            return user_id

    def _get_user(self):
        try:
            with open(Manager.TMP_USER_FILENAME, 'r') as tmp_file:
                data = json.load(tmp_file)

            self.user_id = data['code']
            return Firebase.get_user_data(self.user_id)
        except:
            return None

    def _remove_user_file_if_exist(self):
        if os.path.exists(Manager.TMP_USER_FILENAME):
            os.remove(Manager.TMP_USER_FILENAME)

    def _save_user(self, user):
        with open(Manager.TMP_USER_FILENAME, 'w') as tmp_file:
            user.update({'code': self.user_id})
            json.dump(user, tmp_file)
