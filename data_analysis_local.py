import csv
import os
from datetime import datetime
import pathlib
import matplotlib.pyplot as plt
import numpy as np

from dictionaries.data_representatives_dictonary import representatives_dico
from dictionaries.data_topics_dictionary import topics_dico
from dictionaries.data_topics_dictionary import subtopics_dico
from dictionaries.data_types_dictionary import types_dico
from dictionaries.data_types_dictionary import subtypes_dico

import gspread
from google.oauth2.service_account import Credentials

import matplotlib.colors as mcolors

print("\n#####################################")
print("# Welcome to the data analysis code #")
print("#####################################\n")
print("This code enable the user to tranform online google-sheet file from https://docs.google.com/forms/d/e/1FAIpQLSckjdwv7daQZ8jv7D1wwx6mKeZo2Hp4hLGGmV8FT0VTthvOUg/viewform")
print("To produces data plots of articles already uploaded on the website")
print("In case of problem, don't hesitate to contact Claire.Adam.Bourdarios [at] cern.ch\n")

csv_filename = input("> Enter the csv file name without the extension .csv: ")+".csv"
print(f'The input file is : {pathlib.Path().resolve()}/{csv_filename}\n')
    
with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    data = csv.reader(csvfile)
    headers = next(data)  # Read the first row as headers

    #########################################################
    # Count the representation of types, topics and members #
    #########################################################

    #print(data[0])

    for row in data: 
        if not row:
            continue  # Skip empty rows
        
        if row[23]!="Online":
            continue #Skip not "Online" status
        
        for topic_i in row[16].split(', '):
            if topic_i != "":
                    topics_dico[topic_i] += 1
        
        for type_i in row[15].split(', '):
            if type_i != "":
                    types_dico[type_i] += 1
        
        for subtype_i in row[20].split(', '):
            if subtype_i != "":
                    subtypes_dico[subtype_i] += 1
        
        for subtopic_i in row[21].split(', '):
            if subtopic_i != "":
                    subtopics_dico[subtopic_i] += 1
        
        for representative_i in row[19].split(', '):
            if representative_i != "":
                    representatives_dico[representative_i] += 1

################################################################
# Function to remove the empty tags and members from the plots #
################################################################

def remove_empty(label, value, color=None):
    max_i = len(value)
    i=0
    no_data="No data for:"

    while i < max_i:
        if value[i] == 0:
            no_data += f"\n - {label[i]}"
            label.pop(i)
            value.pop(i)
            
            if color != None:
                color.pop(i)
            max_i-=1
            i-=1
        i+=1

    return label, value, color, no_data

###################################
# Function that format the legend #
###################################

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct,v=val)
    return my_autopct

##########################
# Generate a color table #
##########################

# Get base tab10 colors
base_colors = [mcolors.to_rgb(plt.get_cmap('tab10')(i)) for i in range(10)]

# Generate 10 light-to-dark variations per color
all_colors = [
    np.array(c) * (0.3 + 0.7 * i / 9) + (1 - (0.3 + 0.7 * i / 9)) * np.ones(3)
    for c in base_colors for i in range(10)
]

################################
# Generate IPPOG members plot #
################################

representatives_label = list(representatives_dico.keys())
representatives_value = list(representatives_dico.values())
representatives_label = [representatives_label[i] + f" ({str(representatives_value[i])})" for i in range (len(representatives_label))]
representatives_label, representatives_value, dunmp, representatives_no_data = remove_empty(representatives_label, representatives_value)

fig, ax = plt.subplots()

size = 0.3

explode = np.ones(len(representatives_value))*.05
ax.pie(representatives_value, radius=1, labeldistance=1.1, rotatelabels=True, explode=explode, labels=representatives_label, wedgeprops=dict(width=size))
ax.legend(title = "Related members:",loc = 'upper right',bbox_to_anchor=(1.7, 0, 0.5, 1))

ax.text(1, -3.5, representatives_no_data, bbox=dict(facecolor='white', alpha=0.3))
ax.text(2.5, -3.5, f"updated {datetime.today().strftime('%Y-%m-%d')}", bbox=dict(facecolor='white', alpha=0.3))
plt.savefig("media/data/Related_members.svg",bbox_inches='tight')
print("Saving SVG file: \"Related_members.svg\" plot in directory: media/data/ ")
#plt.show()

#######################
# Generate Types plot #
#######################

# Renormalization
tot_Book_Publication = (subtypes_dico ["Book"] + subtypes_dico ["Comic book"] + subtypes_dico ["Magazine"] + subtypes_dico ["Children book"]) / types_dico ['Book & Publication']
tot_Festival_Temporary_event = (subtypes_dico ["Festival"] + subtypes_dico ["Temporary exhibition"] + subtypes_dico ["HEP Conference"] + subtypes_dico ["Science show"]) / types_dico ['Festival & Temporary event']
tot_Game = (subtypes_dico ["Board game"] + subtypes_dico ["Video game"] + subtypes_dico ["Escape game"]) / types_dico ['Game']
tot_Handson_Activity = (subtypes_dico ["Activity"] + subtypes_dico ["Training & School project"]) / types_dico ['Hands-on Activity']
tot_Lab_Visitor_center = (subtypes_dico ["Exhibit item"] + subtypes_dico ["Permanent exhibition"] + subtypes_dico ["Visit"] + subtypes_dico ["Laboratory"] + subtypes_dico ["Experiment"]) / types_dico ['Lab & Visitor center']
tot_Online_resource = (subtypes_dico ["Visual resource"] + subtypes_dico ["Content creator"] + subtypes_dico ["Educational material"] + subtypes_dico ["Animation"] + subtypes_dico ["Coping with COVID"]) / types_dico ['Online resource']
tot_Open_science = (subtypes_dico ["Participatory science"] + subtypes_dico ["Impact study"] + subtypes_dico ["Open data"]) / types_dico ['Open science']

subtypes_value_init = list(subtypes_dico.values())
subtypes_dico ["Book"] /= tot_Book_Publication
subtypes_dico ["Comic book"] /= tot_Book_Publication
subtypes_dico ["Magazine"] /= tot_Book_Publication
subtypes_dico ["Children book"] /= tot_Book_Publication
subtypes_dico ["Festival"] /= tot_Festival_Temporary_event
subtypes_dico ["Temporary exhibition"] /= tot_Festival_Temporary_event
subtypes_dico ["HEP Conference"] /= tot_Festival_Temporary_event
subtypes_dico ["Science show"] /= tot_Festival_Temporary_event
subtypes_dico ["Board game"] /= tot_Game
subtypes_dico ["Video game"] /= tot_Game
subtypes_dico ["Escape game"] /= tot_Game
subtypes_dico ["Activity"] /= tot_Handson_Activity
subtypes_dico ["Training & School project"] /= tot_Handson_Activity
subtypes_dico ["National outreach program"] = types_dico ["National Outreach program"]
subtypes_dico ["Exhibit item"] /= tot_Lab_Visitor_center
subtypes_dico ["Permanent exhibition"] /= tot_Lab_Visitor_center
subtypes_dico ["Visit"] /= tot_Lab_Visitor_center
subtypes_dico ["Laboratory"] /= tot_Lab_Visitor_center
subtypes_dico ["Experiment"] /= tot_Lab_Visitor_center
subtypes_dico ["Visual resource"] /= tot_Online_resource
subtypes_dico ["Content creator"] /= tot_Online_resource
subtypes_dico ["Educational material"] /= tot_Online_resource
subtypes_dico ["Animation"] /= tot_Online_resource
subtypes_dico ["Coping with COVID"] /= tot_Online_resource
subtypes_dico ["Participatory science"] /= tot_Open_science
subtypes_dico ["Impact study"] /= tot_Open_science
subtypes_dico ["Open data"] /= tot_Open_science

# Types
types_label = list(types_dico.keys())
types_value = list(types_dico.values())
types_label = [types_label[i] + f" ({str(types_value[i])})" for i in range (len(types_label))]
types_color = list( all_colors[i] for i in [9, 19, 29, 39, 49, 59, 69, 79] )

#Sub-Types
subtypes_label = list(subtypes_dico.keys())
subtypes_value = list(subtypes_dico.values())
subtypes_label = [subtypes_label[i] + f" ({str(subtypes_value_init[i])})" for i in range (len(subtypes_label))]
subtypes_color = list( all_colors[i] for i in [2, 4, 6, 8, 12, 14, 16, 18, 23, 26, 28, 34, 36, 45, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 72, 74, 76, 78,] )
subtypes_label, subtypes_value, subttypes_color, subtypes_no_data = remove_empty(subtypes_label, subtypes_value, subtypes_color)

fig, ax = plt.subplots()

size = 0.3

# Types plot
explode = np.ones(len(types_dico))*.01
ax.pie(types_value, radius=.9, colors=types_color, explode=explode, autopct=make_autopct(types_value), pctdistance = 0.7)
ax.legend(title = "Types:", labels=types_label,loc = 'upper right',bbox_to_anchor=(1.6, 0, 0.5, 1))

# Sub-Types plot
subexplode = np.ones(len(subtypes_value))*.01
ax.pie(subtypes_value, radius=.9+size, colors=subtypes_color, labeldistance=1, explode=subexplode, labels=subtypes_label, rotatelabels=True, wedgeprops=dict(width=size, edgecolor='w'))

ax.text(2, 1.5, subtypes_no_data, bbox=dict(facecolor='white', alpha=0.3))
ax.text(2.2, 1.3, f"updated {datetime.today().strftime('%Y-%m-%d')}", bbox=dict(facecolor='white', alpha=0.3))
ax.set(aspect="equal")
plt.savefig("media/data/types.svg",bbox_inches='tight')
print("Saving SVG file: \"types.svg\" plot in directory: media/data/ ")
#plt.show()

########################
# Generate Topics plot #
########################

# Renormalization
toto_Matter_Forces = (subtopics_dico["Nuclear & Atomic physics & radioactivity"] + subtopics_dico["Standard model of elementary particles"] + subtopics_dico["Higgs"] + subtopics_dico["Neutrino"] + subtopics_dico["Antimatter"] + subtopics_dico["Laws of physics"]) / topics_dico["Matter & Forces"]
toto_Universe = (subtopics_dico["The big bang and the universe"] + subtopics_dico["Gravitational waves"] + subtopics_dico["Dark matter"] + subtopics_dico["Cosmic rays"]) / topics_dico["Universe"]
toto_Technology = (subtopics_dico["Data analysis"] + subtopics_dico["Detector & Sensors"] + subtopics_dico["Machine learning"] + subtopics_dico["Accelerator & Collisions"] + subtopics_dico["Civil Engineering & Construction"] + subtopics_dico["Computing"] + subtopics_dico["Cryogeny, Magnets & Supraconductors"]) / topics_dico["Technology"]
toto_Science_Society = (subtopics_dico["Diversity"] + subtopics_dico["Applications and spin-off"] + subtopics_dico["Outreach trainings & tips"]) / topics_dico["Science & Society"]
toto_Art_Science = (subtopics_dico["Fine art"] + subtopics_dico["Music"] + subtopics_dico["Literature"]) / topics_dico["Art Science"]

subtopics_value_init = list(subtopics_dico.values())
subtopics_dico["Fine art"] /= toto_Art_Science
subtopics_dico["Music"] /= toto_Art_Science
subtopics_dico["Literature"] /= toto_Art_Science
subtopics_dico["Nuclear & Atomic physics & radioactivity"] /= toto_Matter_Forces
subtopics_dico["Standard model of elementary particles"] /= toto_Matter_Forces
subtopics_dico["Higgs"] /= toto_Matter_Forces
subtopics_dico["Neutrino"] /= toto_Matter_Forces
subtopics_dico["Antimatter"] /= toto_Matter_Forces
subtopics_dico["Laws of physics"] /= toto_Matter_Forces
subtopics_dico["Data analysis"] /= toto_Technology
subtopics_dico["Detector & Sensors"] /= toto_Technology
subtopics_dico["Machine learning"] /= toto_Technology
subtopics_dico["Accelerator & Collisions"] /= toto_Technology
subtopics_dico["Civil Engineering & Construction"] /= toto_Technology
subtopics_dico["Computing"] /= toto_Technology
subtopics_dico["Cryogeny, Magnets & Supraconductors"] /= toto_Technology
subtopics_dico["The big bang and the universe"] /= toto_Universe
subtopics_dico["Gravitational waves"] /= toto_Universe
subtopics_dico["Dark matter"] /= toto_Universe
subtopics_dico["Cosmic rays"] /= toto_Universe
subtopics_dico["Diversity"] /= toto_Science_Society
subtopics_dico["Applications and spin-off"] /= toto_Science_Society
subtopics_dico["Outreach trainings & tips"] /= toto_Science_Society

# Topics
topics_label = list(topics_dico.keys())
topics_value = list(topics_dico.values())
topics_label = [topics_label[i] + f" ({str(topics_value[i])})" for i in range (len(topics_label))]
topics_color = list( all_colors[i] for i in [9, 19, 29, 39, 49] )

# Sub-Topics
subtopics_label = list(subtopics_dico.keys())
subtopics_value = list(subtopics_dico.values())
subtopics_label = [subtopics_label[i] + f" ({str(subtopics_value_init[i])})" for i in range (len(subtopics_label))]
subtopics_color = list( all_colors[i] for i in [2, 5, 8, 12, 14, 15, 16, 17, 18, 20, 22, 23, 25, 26, 27, 28, 32, 34, 36, 38, 43, 46, 49] )
subtopics_label, subtopics_value, subtopics_color, subtopics_no_data = remove_empty(subtopics_label, subtopics_value, subtopics_color)

fig, ax = plt.subplots()

size = 0.3

# Topics plot
explode = np.ones(len(topics_dico))*.01
ax.pie(topics_value, radius=.9, colors=topics_color, explode=explode, autopct=make_autopct(topics_value), pctdistance = 0.7)
ax.legend(title = "Topics:", labels=topics_label ,loc = 'upper right',bbox_to_anchor=(1.5, 0, 0.5, 1))

# Sub-Topics plot
subexplode = np.ones(len(subtopics_value))*.01
ax.pie(subtopics_value, radius=.9+size, colors=subtopics_color, labeldistance=1, explode=subexplode, labels=subtopics_label, rotatelabels=True, wedgeprops=dict(width=size, edgecolor='w'))

ax.text(2, -.2, subtopics_no_data, bbox=dict(facecolor='white', alpha=0.3))
ax.text(3, -.4, f"updated {datetime.today().strftime('%Y-%m-%d')}", bbox=dict(facecolor='white', alpha=0.3))
ax.set(aspect="equal")
plt.savefig("media/data/topics.svg",bbox_inches='tight')
print("Saving SVG file: \"topics.svg\" plot in directory: media/data/ ")
#plt.show()