import pandas as pd
import glob 
import os
import plotly.express as px
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
from  reportlab.graphics.shapes import Drawing
from datetime import datetime
from os import listdir
import sys



def convertFile(fileName, curFileNo, totalJobSize):
    print("Processing " + str(curFileNo) + " of " + str(totalJobSize) + " File name: " + fileName)



    # Read Current .csv file
    df = pd.read_csv(fileName)

    # Calculate basic statistics 
    data_points = len(df.index)
    min = df[["Heart Rate"]].min(axis = 0)
    max = df[["Heart Rate"]].max(axis = 0)
    mean = df[["Heart Rate"]].mean(axis = 0)
    wear_time_hours = int(data_points/60)
    wear_time_minutes = data_points - (wear_time_hours*60)
    wear_time_seconds = "XX"
    # Calculate mins in each range
    hr_range_a = df['Heart Rate'][df['Heart Rate'] < 50].count()
    hr_range_b = df['Heart Rate'][df['Heart Rate'] >= 60].count()-df['Heart Rate'][df['Heart Rate'] >= 50].count()
    hr_range_c = df['Heart Rate'][df['Heart Rate'] >= 70].count()-df['Heart Rate'][df['Heart Rate'] >= 60].count()
    hr_range_d = df['Heart Rate'][df['Heart Rate'] >= 80].count()-df['Heart Rate'][df['Heart Rate'] >= 70].count()
    hr_range_e = df['Heart Rate'][df['Heart Rate'] >= 90].count()-df['Heart Rate'][df['Heart Rate'] >= 80].count()
    hr_range_f = df['Heart Rate'][df['Heart Rate'] >= 100].count()-df['Heart Rate'][df['Heart Rate'] >= 90].count()
    hr_range_g = df['Heart Rate'][df['Heart Rate'] >= 110].count()-df['Heart Rate'][df['Heart Rate'] >= 100].count()
    hr_range_h = df['Heart Rate'][df['Heart Rate'] >= 120].count()-df['Heart Rate'][df['Heart Rate'] >= 110].count()
    hr_range_i = df['Heart Rate'][df['Heart Rate'] >= 130].count()-df['Heart Rate'][df['Heart Rate'] >= 120].count()
    hr_range_j = df['Heart Rate'][df['Heart Rate'] >= 140].count()-df['Heart Rate'][df['Heart Rate'] >= 130].count()
    hr_range_k = df['Heart Rate'][df['Heart Rate'] >= 140].count()


    # Create graph
    fig = px.line(df, x = 'Time', y = 'Heart Rate', title='Heart Rate')
    fig.write_image("fig1.jpg")



    # create pdf
    canvas = Canvas("per_day_pdf_out/"+fileName.replace('.csv','.pdf'), pagesize=LETTER)
    canvas.setFont("Times-Roman", 12)
    # Top portion
    canvas.drawString(1,700,"Batch Convert " + str(curFileNo) + " of " + str(totalJobSize))
    canvas.drawString(200,700,"File name : " + fileName)
    canvas.drawString(350,700,"Date from Filename : "+ fileName.replace(".csv",""))
    canvas.drawString(1,690,"Total data points: " + str(data_points))
    canvas.drawString(200,690,"Approximate wear time HHMM: " + str(wear_time_hours) + ":" + str(wear_time_minutes))
    canvas.drawString(1,680,"Minimum HR: " + str(min).split("\n")[0])
    canvas.drawString(200,680,"Maximum HR: "+ str(max).split("\n")[0])
    canvas.drawString(1,670,"Average HR: "+ str(mean).split("\n")[0])
    canvas.drawString(200,670,"")
    # Bottom Portion
    canvas.drawString(1,390,"Minutes heartrate spent in a given range")

    canvas.drawString(1,380,"M. bpm < 50: " + str(abs(hr_range_a)))
    canvas.drawString(200,380,"M. bpm >50, < 60: "+ str(abs(hr_range_b)))
    canvas.drawString(400,380,"M. bpm >60, < 70: "+ str(abs(hr_range_c)))

    canvas.drawString(1,370,"M. bpm >70, < 80: "+ str(abs(hr_range_d)))
    canvas.drawString(200,370,"M. bpm >80, < 90: "+ str(abs(hr_range_e)))
    canvas.drawString(400,370,"M. bpm >90, < 100: "+ str(abs(hr_range_f)))

    canvas.drawString(1,360,"M. bpm >100, < 110: "+ str(abs(hr_range_g)))
    canvas.drawString(200,360,"M. bpm >110, < 120: "+ str(abs(hr_range_h)))
    canvas.drawString(400,360,"M. bpm >120, < 130: "+ str(abs(hr_range_i)))

    canvas.drawString(1,350,"M. bpm >130, < 140: "+ str(abs(hr_range_j)))
    canvas.drawString(200,350,"M. bpm >140: "+ str(abs(hr_range_k)))

    # Add Graph
    canvas.drawInlineImage("fig1.jpg",150,400,350,250)
    canvas.drawString(1,10,"Report Generated on: " + str(datetime.now().strftime("%B %d, %Y %H:%M:%S")))
    canvas.save()



os.chdir("raw_csv")
curFileNo = 1
totalJobSize = len(glob.glob("*.csv"))

for file in glob.glob("*.csv"):
    convertFile(file, curFileNo, totalJobSize)
    curFileNo += 1

