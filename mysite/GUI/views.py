from django.shortcuts import render

import pandas as pd
import random as rd
import os
# Create your views here.

def index(request):
    form = request.POST #Parse info from the webpage form
    plant_selected = form.get("which_plant")

    data = pd.read_csv("/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plant_data_with_webpages.csv")
    data = data.sort_values("Common Name")
    context = {'plant_names':data['Common Name']}
    # print(context)
    context['plant_selected'] = False
    if plant_selected != None:
        context['plant_selected'] = plant_selected
        plant_data = data[data['Common Name'] == plant_selected]
        vals = convert_to_human_readable({i:plant_data[i].iloc[0] for i in ['L','T','H','W']})
        print(vals)
        context['Light_Level'] = vals['L']
        context['Temp'] = vals['T']
        context['Humidity'] = vals['H']
        context['Soil'] = plant_data['S'].iloc[0]
        context['imgs'] = ['img/'+i for i in os.listdir('/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/img') if plant_selected.replace(' ','_').replace('’','') in i][:4]
    context['curr_temp'],context['curr_humid'],context['curr_light'] = takeReading()
    if context['plant_selected'] == False:
        context['plant_selected'] = data.iloc[0]['Common Name']
    context['plant_hap'] = 77
    return render(request, "GUI/index.html",context)

def convert_to_human_readable(vals):
    vals = {i:vals[i].replace("-"," to ") for i in vals}
    vals['L'] = vals['L'].replace('1', '4 hrs direct sun')
    vals['L'] = vals['L'].replace('2', '<1hr direct sun')
    vals['L'] = vals['L'].replace('3', 'Partial Shade')
    vals['L'] = vals['L'].replace('3', 'Shade')

    vals['T'] = vals['T'].replace('1', 'Cool ~18 <sup>o</sup>1C')
    vals['T'] = vals['T'].replace("2", "Normal Room Temp ~$RT <sup>o</sup>C")
    vals['T'] = vals['T'].replace("3", "Warm ~29 <sup>o</sup>C")
    vals['T'] = vals['T'].replace("$RT", "23")

    vals['H'] = vals['H'].replace("1", "High >50%")
    vals['H'] = vals['H'].replace("2", "Medium 25% to 50%")
    vals['H'] = vals['H'].replace("3", "Low <25%")

    vals['W'] = vals['W'].replace('1', 'Moist Soil')
    vals['W'] = vals['W'].replace('2', 'Should be dry(ish) before watering')
    vals['W'] = vals['W'].replace('3', 'Should be dry before watering')
    return vals

def takeReading():
    Temp, Humid, Light = rd.randint(18,30), rd.randint(20,90), rd.randint(10,10000)
    return Temp, Humid, Light
