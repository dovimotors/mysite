from dbfpy import dbf
import csv
import pandas as pd
import numpy as np


class AdamImport:
    def DBFConverter(self, ifile, ofile, conv_type):
        # create the DBF reader object
        db = dbf.Dbf(ifile)
        # create the file to output CSV data to
        fpath = ofile
        f = open(fpath,'w')
        # initiat the header container and CSV writer
        hdr = []
        c = csv.writer(f)

        # loop through all the field names and create the header row
        for fieldName in db.fieldNames:
            hdr += [fieldName]

        # write the head to the CSV file
        c.writerow(hdr)

        # loop through all the records and write each line to the CSV file
        for rec in db:
            # using asList makes a list as opposed to asDict
            c.writerow(rec.asList())

        if conv_type in ['pandas']:
            # take the csv file and open it as a pandas dataframe
            from_csv = pd.read_csv(fpath)
            # return a dataframe object
            return from_csv

        if conv_type in ['csvfileobject']:
            return f
        # close the CSV file
        f.close()
        db.close()

    def GetColNames(self, ifile):
        db = dbf.Dbf(ifile)
        # initiat the header container and CSV writer
        hdr = []

        # loop through all the field names and create the header row
        for fieldName in db.fieldNames:
            hdr += [fieldName]
        db.close()
        return hdr

    def GetColNamesAndTypes(self,ifile):
        db = dbf.Dbf(ifile)
        dict = {}
        df = db.fieldDefs
        for rec in db[0:1]:
            for fldName in db.fieldNames:
                dict[fldName] = type(rec[fldName]).__name__

        # print db.__repr__
        # print dict
        # print df
        return dict
        db.close()
