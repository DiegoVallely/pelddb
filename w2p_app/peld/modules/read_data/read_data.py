#! -*- coding: utf-8 -*- 
import xlrd
import datetime as dt
import os

path = os.path.abspath("applications/peld/data_samples/")

class ReadTidbit(object):
    """Reads standard tidbit data"""
    def __init__(self, filename):
        super(ReadTidbit, self).__init__()
        self.filename = filename
        f = open(filename)
        self.dates, self.times, self.temps = [], [], []
        for line in f.readlines():
            # date 
            month = int(line.split("/")[0])
            day   = int(line.split("/")[1])
            year  = int(line.split("/")[2][:4])
            date  = dt.datetime(year, month, day)
            # time
            hour   = int(line.split(" ")[2].split(":")[0])
            minute = int(line.split(" ")[2].split(":")[1])
            time   = dt.time(hour, minute)
            # temperature
            temp = line.split(" ")[-1]
            temp = float(temp.split(",")[0] + "." + temp.split(",")[1][0])

            self.dates.append(date)
            self.times.append(time)
            self.temps.append(temp)


class DataSheet1(object):
    """Reads xls datasheet from 1974-1975 project"""
    def __init__(self, filename):
        self.book = xlrd.open_workbook(path+'/enseada.xlsx')
        self.sheet = self.book.sheet_by_name('Plan1')

    def get_data(self):
        date, spot, station, temp, salt = [], [], [], [], [] 
        oxig, fosfate, nitrate, amonium, silicate, chla = [], [], [], [], [], []
        sh = self.sheet

        for row in range(1, sh.nrows):
            d = sh.cell_value(row, 0)
            d = xlrd.xldate_as_tuple(d, self.book.datemode)
            date.append(dt.date(d[0], d[1], d[2]))
            spot.append(sh.cell(row, 1).value)
            station.append(int(sh.cell(row, 2).value))
            temp.append( sh.cell(row, 3).value if sh.cell(row, 3).value else None )
            salt.append( sh.cell(row, 4).value if sh.cell(row, 4).value else None )
            oxig.append( sh.cell(row, 5).value if sh.cell(row, 5).value else None)
            fosfate.append( sh.cell(row, 6).value if sh.cell(row, 6).value else None )
            nitrate.append( sh.cell(row, 7).value if sh.cell(row, 7).value else None ) 
            amonium.append( sh.cell(row, 8).value if sh.cell(row, 8).value else None )
            silicate.append( sh.cell(row, 9).value if sh.cell(row, 9).value else None )
            chla.append( sh.cell(row, 10).value if sh.cell(row, 10).value else None )

        return date, spot, station, temp, salt, oxig, fosfate, nitrate, amonium, silicate, chla