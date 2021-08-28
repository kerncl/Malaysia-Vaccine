import pandas as pd
from urllib.request import Request, urlopen
import logging
import sys

## logging
mylog = logging.getLogger()
mylog.setLevel(logging.INFO)

stream_fh = logging.StreamHandler(stream=sys.stdout)
stream_fh.setLevel(logging.INFO)

file_fh = logging.FileHandler('temp.log', mode='w')
file_fh.setLevel(logging.INFO)

mylog.addHandler(stream_fh)
mylog.addHandler(file_fh)

MOH_REPO = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/'
MOH_Vaccine = 'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/'

def download_data(source='', sufflix=''):
    if not source or not sufflix:
        raise NotImplementedError('Please provide source/sufflix')
    url = source + sufflix
    mylog.info(f'Downloading data from: {url}')
    req = Request(url=url)
    data = urlopen(req)
    table = pd.read_csv(data)
    mylog.info(f'Done downloading data from: {url}')
    return table


table_list = (('Population', MOH_REPO, 'static/population.csv'),
              ('Malaysia_vaccine', MOH_Vaccine, 'vaccination/vax_malaysia.csv'),
              ('State_vaccine', MOH_Vaccine, 'vaccination/vax_state.csv'))


for table_name, source, suffilx in table_list:
    try:
        # set to __main__
        globals().update({table_name: download_data(source,suffilx)})
    except Exception as ex:
        mylog.error(f'Error while downloading: {url}\n'
                    f'Exception: {ex}')

## close handler
while mylog.handlers:
    fh = mylog.handlers[0]
    fh.close()
    mylog.removeHandler(fh)