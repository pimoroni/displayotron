"""
Stocks plugin, ported from Facelessloser's Atmega_screen
https://github.com/facelessloser/Atmega_screen/blob/master/arduino_python_files/stock-ticker/atmega_screen_stock_ticker.py
"""

import json
import threading
import urllib

from dot3k.menu import MenuOption


class Stocks(MenuOption):
    def __init__(self):
        self.companies = ['GOOG', 'AAPL', 'TWTR', 'FB']
        self.data = {}
        self.company = 0

        self.last_update = 0
        self.last_event = 0

        MenuOption.__init__(self)

        self.is_setup = False

    def input_prompt(self):
        """
        Returns the prompt/title for the input plugin
        """
        return 'Stock code:'

    def receive_input(self, value):
        """
        The value we get back when text input finishes
        """
        self.companies.append(value)
        self.get_stock_data(True)
        self.update_options()

    def begin(self):
        self.reset_timeout()

    def add_new(self):
        self.request_input()

    def reset_timeout(self):
        self.last_event = self.millis()

    def setup(self, config):
        MenuOption.setup(self, config)
        self.load_options()

    def update_options(self):
        self.set_option('Stocks', 'companies', ','.join(self.companies))
        pass

    def load_options(self):
        self.companies = self.get_option('Stocks', 'companies', ','.join(self.companies)).split(',')
        pass

    def cleanup(self):
        self.is_setup = False

    def select(self):
        self.add_new()
        return False

    def left(self):
        self.reset_timeout()
        return False

    def right(self):
        self.reset_timeout()
        return True

    def up(self):
        self.reset_timeout()
        self.company = (self.company - 1) % len(self.companies)
        return True

    def down(self):
        self.reset_timeout()
        self.company = (self.company + 1) % len(self.companies)
        return True

    def get_stock_data(self, force=False):
        # Update only once every 60 seconds
        if self.millis() - self.last_update < 6 * 1000 * 60 and not force:
            return False

        update = threading.Thread(None, self.do_update)
        update.daemon = True
        update.start()

    def do_update(self):
        self.last_update = self.millis()

        base_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{STOCK}%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json'

        for company in self.companies:
            url_open = urllib.urlopen(base_url.replace('{STOCK}', company))
            url_read = url_open.read()
            parsed_json = json.loads(url_read)
            self.data[company] = (
                float(parsed_json['query']['results']['quote']['LastTradePriceOnly']),
                float(parsed_json['query']['results']['quote']['PercentChange'].replace('%', '')),
                float(parsed_json['query']['results']['quote']['MarketCapitalization'].replace('B', ''))
            )

    def redraw(self, menu):
        self.get_stock_data()

        if self.millis() - self.last_event >= 6 * 1000 * 5:
            self.company = (self.millis() / 5000) % len(self.companies)

        if not self.is_setup:
            menu.lcd.create_char(0, [0, 0, 0, 14, 17, 17, 14, 0])
            menu.lcd.create_char(1, [0, 0, 0, 14, 31, 31, 14, 0])
            menu.lcd.create_char(2, [0, 14, 17, 17, 17, 14, 0, 0])
            menu.lcd.create_char(3, [0, 14, 31, 31, 31, 14, 0, 0])
            menu.lcd.create_char(4, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            menu.lcd.create_char(5, [0, 0, 10, 27, 10, 0, 0, 0])  # Left right arrow
            self.is_setup = True

        current_company = self.companies[self.company]

        menu.write_row(0, current_company)
        if current_company in self.data.keys():
            data = self.data[current_company]
            menu.write_row(1, str(data[0]) + ' ' + chr(4) + str(data[1]) + '%')
            menu.write_row(2, 'Cap:' + str(data[2]) + 'B')
        else:
            menu.write_row(1, 'No Data Available')
            menu.write_row(2, '')
