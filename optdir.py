import urllib.request
import os
import shutil
import sys
import logging
import datetime
import pandas as pd

logging.basicConfig(filename='optdir_log_{0}.log'.format(datetime.date.today()),
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


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
                    logging.info('number of entries: {0}'.format(len(df)))
                    if len(df) > 325:
                        df.to_csv(fpath, index=False)
                else:
                    df = self.parse_ise_list(penny=True)
                    logging.info('number of entries: {0}'.format(len(df)))
                    if len(df) > 325:
                        df.to_csv(fpath, index=False)

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    if dest_folder:
                        df = self.parse_ise_list(penny=True)
                        logging.info('number of entries: {0}'.format(len(df)))
                        if len(df) > 325:
                            df.to_csv(fpath, index=False)
                    else:
                        df = self.parse_ise_list(penny=True)
                        logging.info('number of entries: {0}'.format(len(df)))
                        if len(df) > 325:
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
                    logging.info('number of entries: {0}'.format(len(df)))
                    if len(df) > 325:
                        df.to_csv(fpath, index=False)
                else:
                    df = self.parse_ise_list()
                    logging.info('number of entries: {0}'.format(len(df)))
                    if len(df) > 325:
                        df.to_csv(fpath, index=False)

            else:
                self.download_ise_csv(dest_folder='temp')
                if self.ppilot_path:
                    if dest_folder:
                        df = self.parse_ise_list()
                        logging.info('number of entries: {0}'.format(len(df)))
                        if len(df) > 325:
                            df.to_csv(fpath, index=False)
                    else:
                        df = self.parse_ise_list()
                        logging.info('number of entries: {0}'.format(len(df)))
                        if len(df) > 325:
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

        iseurl = 'https://www.ise.com/assets/files/products/productstraded/options_product_equityDownload.csv'
        path = 'ppilot_symbs.csv'
        if dest_folder:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            path = os.path.join(dest_folder, path)
        urllib.request.urlretrieve(iseurl, path)
        if os.path.exists(path):
            self.ppilot_path = path
            logging.info('ISE data retrieved')
        else:
            logging.info('ISE data retrieved')
    # # #

    def parse_args(self):
        # supporting func for OptDir.from_cmd
        # parses cmd line arguments for ease of use with automation/bat files
        # defaults can be set in strings below - specifying dest_path will overwrite dest_folder and fname

        dest_folder = ''
        fname = 'pennies.txt'
        ltype = 'penny'

        if len(sys.argv) > 1:
            for item in sys.argv:
                if 'fname=' in item:
                    t = item.split('fname=')
                    fname = t[1]
                    logging.info('... filename specified: {0}'.format(fname))

                if 'dest_folder=' in item:
                    t = item.split('dest_folder=')
                    dest_folder = t[1]
                    logging.info('... destination folder specified: {0}'.format(dest_folder))

                if 'type=' in item:
                    t = item.split('headers=')
                    if t[1].lower() == 'nickel':
                        ltype = 'nickel'
                        logging.info('... list type set to {0}'.format(ltype))
                    elif t[1].lower() == 'penny':
                        ltype = 'penny'
                        logging.info('... list type set to {0}'.format(ltype))

        full_path = os.path.join(dest_folder, fname)
        logging.info('... saving to path: {0}'.format(full_path))
        argd = [dest_folder, fname, ltype, full_path]
        return argd

    def from_cmd(self):

        argd = self.parse_args()
        if argd[2] == 'penny':
            self.create_penny_list(to_txt=True, dest_folder=argd[0], dest_filename=argd[1])
            if os.path.exists(argd[3]):
                logging.info('... complete {0}'.format(argd[3]))
        elif len(argd[2]) == 'nickel':
            self.create_nickel_list(to_txt=True, dest_folder=argd[0], dest_filename=argd[1])
            if os.path.exists(argd[3]):
                logging.info('... complete {0}'.format(argd[3]))


if __name__ == "__main__":
    optlist = OptDirectory()
    optlist.from_cmd()
