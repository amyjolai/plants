from django.shortcuts import render

import pandas as pd
import random as rd
import os
import numpy as np

def convert_L(val):
    fit = [-616.66666667,6200.,-21283.33333333,25700.]
    return np.polyval(fit, np.mean([int(i) for i in val.split('-')]))

def convert_T(val):
    return (5.5*np.mean([int(i) for i in val.split('-')])) + 12

def convert_H(val):
    return (27.5*np.mean([int(i) for i in val.split('-')])) -16.

def convert_W(val):
    return (0.5*np.mean([int(i) for i in val.split('-')])) -0.5

def create_color(happiness):
    r = 255-127*(np.tanh((float(happiness)-65)*0.05) +1)
    g = 127*(np.tanh((float(happiness)-35)*0.05) +1)
    return ','.join([str(r), str(g),  '0'])

def create_happiness_index(data, vals):
    data['Ltmp'] = data['L'].apply(convert_L)
    print(data['Ltmp'].apply(str)+'  -  '+data['L'])
    data['Ttmp'] = data['T'].apply(convert_T)
    data['Htmp'] = data['H'].apply(convert_H)
    data['Wtmp'] = data['W'].apply(convert_W)
    data['LL'] = data['Ltmp'][:]

    weights = {'L':1,
            'T':0.9,
            'H':0.4,
            'W':0.9,}

    data['happiness_index'] = 0.0
    for i in ['L','T','H','W']:
        data['%stmp'%i] = np.abs(data['%stmp'%i] - vals[i])
        data['%stmp'%i] = data['%stmp'%i] - np.min(data['%stmp'%i])
        data['%stmp'%i] = 1- (data['%stmp'%i]/np.max(data['%stmp'%i]))
        data['happiness_index'] += data['%stmp'%i]*weights[i]
    data['happiness_index'] = data['happiness_index'] - np.min(data['happiness_index'])
    data['happiness_index'] /= np.max(data['happiness_index'])
    return data

def index(request):
    form = request.POST #Parse info from the webpage form
    plant_selected = form.get("which_plant")
    print(plant_selected)
    if plant_selected == None or 'Select' in plant_selected:
        plant_selected = False

    in_vals = takeReading()

    data = pd.read_csv("/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plant_data_with_webpages.csv")
    data = data.sort_values("Common Name").drop_duplicates("Common Name")
    context = {'plant_names':data['Common Name']}
    # print(context)
    context['plant_selected'] = False
    data = create_happiness_index(data, in_vals)
    if plant_selected != False:
        context['plant_selected'] = plant_selected
        plant_data = data[data['Common Name'] == plant_selected]
        vals = convert_to_human_readable({i:plant_data[i].iloc[0] for i in ['L','T','H','W']})
        context['Light_Level'] = vals['L']
        context['Temp'] = vals['T']
        context['Humidity'] = vals['H']
        context['Soil'] = plant_data['S'].iloc[0]
        context['plant_hap'] = "%.0f"%(plant_data['happiness_index'].iloc[0]*100)
        context['plant_hap_dec'] = plant_data['happiness_index'].iloc[0]
        context['plant_hap_tanh'] = np.tanh((plant_data['happiness_index'].iloc[0]-0.5)*5)*0.5 + 0.5
        context['imgs'] = ['img/'+i for i in os.listdir('/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/img') if plant_selected.replace(' ','_').replace('’','') in i][:2]
        context['col'] = create_color(context['plant_hap'])

    randint = rd.randint(0,10)

    context['plant_to_get'] = data.sort_values('happiness_index', ascending=False).iloc[randint]['Common Name']
    context['plant_to_get_imgs'] = ['img/'+i for i in os.listdir('/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/img') if context['plant_to_get'].replace(' ','_').replace('’','') in i][:4]
    context['curr_temp'],context['curr_humid'],context['curr_light'] = in_vals['T'], in_vals['H'],in_vals['L']

    return render(request, "GUI/index.html",context)

def convert_to_human_readable(vals):
    vals = {i:vals[i].replace("-"," to ") for i in vals}
    vals['L'] = vals['L'].replace('1', '$FOUR hrs direct sun')
    vals['L'] = vals['L'].replace('2', '<1hr direct sun')
    vals['L'] = vals['L'].replace('3', 'Partial Shade')
    vals['L'] = vals['L'].replace('4', 'Shade')
    vals['L'] = vals['L'].replace("$FOUR", "4")

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
    data = pd.read_csv("/home/oem/Documents/Other/Code/Hackathon-UCL-2018/plants/mysite/GUI/static/full_data.csv")
    randint = rd.randint(0,len(data)-1)
    data = data.iloc[randint]
    return {'T': data['T'],
            'H': data['H'],
            'L': data['L'],
            'W': data['W'],}
