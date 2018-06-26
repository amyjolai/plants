from django.shortcuts import render

import pandas as pd
import random as rd
import os
import numpy as np

def convert_L(val):
    return (8000*np.mean([int(i) for i in val.split('-')])) - 7800

def convert_T(val):
    return (5.5*np.mean([int(i) for i in val.split('-')])) + 12

def convert_H(val):
    return (27.5*np.mean([int(i) for i in val.split('-')])) -16.

def convert_W(val):
    return (0.5*np.mean([int(i) for i in val.split('-')])) -0.5

def create_color(happiness):
    return ','.join([str(-2.55*float(happiness)+255), str(2.55*float(happiness)),  '0'])

def create_happiness_index(data, vals):
    data['Ldiff'] = data['L'].apply(convert_L)
    data['Tdiff'] = data['T'].apply(convert_T)
    data['Hdiff'] = data['H'].apply(convert_H)
    data['Wdiff'] = data['W'].apply(convert_W)

    weights = {'L':1,
            'T':0.0,
            'H':0.0,
            'W':0.0,}

    data['happiness_index'] = 0.0
    for i in ['L','T','H','W']:
        data['%sdiff'%i] = np.abs(weights[i]*(data["%sdiff"%i]-vals[i]))
        max_val, min_val = np.max(data['%sdiff'%i]), np.min(data['%sdiff'%i])
        if max_val > 0 and min_val < max_val:
            data['%sdiff'%i] = ( data['%sdiff'%i]-min_val )/(max_val- min_val)
        data['happiness_index'] += data['%sdiff'%i]
    data['happiness_index'] /= sum(weights.values())
    data['happiness_index'] = 1-data['happiness_index']

    return data

def index(request):
    form = request.POST #Parse info from the webpage form
    plant_selected = form.get("which_plant")

    in_vals = takeReading()

    data = pd.read_csv("/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plant_data_with_webpages.csv")
    data = data.sort_values("Common Name").drop_duplicates("Common Name")
    context = {'plant_names':data['Common Name']}
    # print(context)
    context['plant_selected'] = False
    if plant_selected != None:
        context['plant_selected'] = plant_selected
        data = create_happiness_index(data, in_vals)
        plant_data = data[data['Common Name'] == plant_selected]
        vals = convert_to_human_readable({i:plant_data[i].iloc[0] for i in ['L','T','H','W']})
        context['Light_Level'] = vals['L']
        context['Temp'] = vals['T']
        context['Humidity'] = vals['H']
        context['Soil'] = plant_data['S'].iloc[0]
        randint = rd.randint(0,10)
        context['plant_to_get'] = data.sort_values('happiness_index').iloc[randint]['Common Name']
        context['plant_hap'] = "%.0f"%(data['happiness_index'].iloc[0]*100)
        context['plant_hap_dec'] = data['happiness_index'].iloc[0]
        context['plant_hap_tanh'] = np.tanh((data['happiness_index'].iloc[0]-0.5)*5)*0.5 + 0.5
        context['imgs'] = ['img/'+i for i in os.listdir('/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/img') if plant_selected.replace(' ','_').replace('’','') in i][:4]
        context['plant_to_get_imgs'] = ['img/'+i for i in os.listdir('/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/img') if context['plant_to_get'].replace(' ','_').replace('’','') in i][:4]
        context['col'] = create_color(context['plant_hap'])
    context['curr_temp'],context['curr_humid'],context['curr_light'] = in_vals['T'], in_vals['H'],in_vals['L']

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
    return {'T': rd.randint(18,30),
            'H': rd.randint(20,90),
            'L': rd.randint(10,10000),
            'W': rd.randint(0,10)/10.,}
