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
    
    hour = 0

    hour_split_data = []
    while hour < 24:
        if hour < 10:
            hour_S = "0" + str(hour)
        else:
            hour_S = str(hour)
        split_df = df[df['Time'].str.startswith(str(hour_S))]
        split_mean = str(split_df[["Heart Rate"]].mean(axis = 0)).split("\n")[0]
        split_mean = split_mean.split(" ")
        if "NaN" in split_mean:
            hour_split_data.append(hour_S + " : " + "n/a")
        else:
            hour_split_data.append(hour_S + " : " + str(split_mean[5]))
        hour += 1
    canvas.drawString(1,330,"Hour by hour Average")
    canvas.drawString(1,320,hour_split_data[0])
    canvas.drawString(200,320,hour_split_data[1])
    canvas.drawString(400,320,hour_split_data[2])

    canvas.drawString(1,310,hour_split_data[3])
    canvas.drawString(200,310,hour_split_data[4])
    canvas.drawString(400,310,hour_split_data[5])

    canvas.drawString(1,300,hour_split_data[6])
    canvas.drawString(200,300,hour_split_data[7])
    canvas.drawString(400,300,hour_split_data[8])

    canvas.drawString(1,290,hour_split_data[9])
    canvas.drawString(200,290,hour_split_data[10])
    canvas.drawString(400,290,hour_split_data[11])

    canvas.drawString(1,280,hour_split_data[12])
    canvas.drawString(200,280,hour_split_data[13])
    canvas.drawString(400,280,hour_split_data[14])

    canvas.drawString(1,270,hour_split_data[15])
    canvas.drawString(200,270,hour_split_data[16])
    canvas.drawString(400,270,hour_split_data[17])

    canvas.drawString(1,260,hour_split_data[18])
    canvas.drawString(200,260,hour_split_data[19])
    canvas.drawString(400,260,hour_split_data[20])

    canvas.drawString(1,250,hour_split_data[21])
    canvas.drawString(200,250,hour_split_data[22])
    canvas.drawString(400,250,hour_split_data[23])
    canvas.save()

os.chdir("raw_csv")
curFileNo = 1
totalJobSize = len(glob.glob("*.csv"))

for file in glob.glob("*.csv"):
    convertFile(file, curFileNo, totalJobSize)
    curFileNo += 1

