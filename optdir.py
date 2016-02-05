import urllib.request
import os
import shutil
import pandas as pd


class OptDirectory:

    # Data retrieved from:
    # https://www.ise.com/options/regulatory-and-fees/options-penny-pilot/

    def __init__(self):

        self.ppilot_path = ''
        self.cboe_path = ''

    def create_penny_list(self, to_txt=False, dest_folder='', dest_filename=''):

        if to_txt:
            if dest_filename:
                fpath = dest_filename
            else:
                fpath = 'pennies.txt'

            if dest_folder:
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                fpath = os.path.join(dest_folder, fpath)

            if self.ppilot_path:
                if dest_folder:
                    df = self.parse_ise_list(penny=True)
                    df.to_csv(fpath, index=False)
                else:
                    df = self.parse_ise_list(penny=True)
                    df.to_csv(fpath, index=False)

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    if dest_folder:
                        df = self.parse_ise_list(penny=True)
                        df.to_csv(fpath, index=False)
                    else:
                        df = self.parse_ise_list(penny=True)
                        df.to_csv(fpath, index=False)
                shutil.rmtree('temp')
        else:
            if self.ppilot_path:
                df = self.parse_ise_list(penny=True)
                return df.tolist()

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    df = self.parse_ise_list(penny=True)
                    if os.path.isdir('temp'):
                        shutil.rmtree('temp', ignore_errors=True)
                    return df.tolist()

    def create_nickel_list(self, to_txt=False, dest_folder='', dest_filename=''):

        if to_txt:
            if dest_filename:
                fpath = dest_filename
            else:
                fpath = 'nickels.txt'

            if dest_folder:
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                fpath = os.path.join(dest_folder, fpath)

            if self.ppilot_path:
                if dest_folder:
                    df = self.parse_ise_list()
                    df.to_csv(fpath, index=False)
                else:
                    df = self.parse_ise_list()
                    df.to_csv(fpath, index=False)

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    if dest_folder:
                        df = self.parse_ise_list()
                        df.to_csv(fpath, index=False)
                    else:
                        df = self.parse_ise_list()
                        df.to_csv(fpath, index=False)
                shutil.rmtree('temp')
        else:
            if self.ppilot_path:
                df = self.parse_ise_list()
                return df.tolist()

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    df = self.parse_ise_list()
                    if os.path.isdir('temp'):
                        shutil.rmtree('temp')
                    return df.tolist()


# # #

    def parse_ise_list(self, penny=False):

        if penny:
            pennies = pd.read_csv(self.ppilot_path, encoding='iso-8859-1')
            pennies = pennies[pennies['PENNY'] == 'X']
            symb_list = pennies['SYMBOL']
            return symb_list
        else:
            pennies = pd.read_csv(self.ppilot_path, encoding='iso-8859-1')
            pennies = pennies[pennies['PENNY'] != 'X']
            symb_list = pennies['SYMBOL']
            return symb_list

    def download_ise_csv(self, dest_folder=''):

        path = 'ppilot_symbs.csv'
        if dest_folder:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            path = os.path.join(dest_folder, path)
        urllib.request.urlretrieve('https://www.ise.com/assets/files/products/productstraded/options_product_equityDownload.csv', path)
        if os.path.exists(path):
            self.ppilot_path = path
            print('ISE data retrieved')
        else:
            print('ISE data not found')
