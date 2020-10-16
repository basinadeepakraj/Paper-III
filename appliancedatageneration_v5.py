#!/usr/bin/env python3
import sys 
import os 
import numpy as np 
import csv 
import random as rd 

# Microgrid_id = sys.argv[1]
Microgrid_id = 1
rd.seed(Microgrid_id)
#Constant Variables 
NTimeSlots = 24
PriceTariffs = [1, 2, 3, 4, 5, 6, 7, 8] #Currency units 
NTypes_of_Houses = 5 
NCat_of_Appls = 5 # Number of categories of applianes 
Type_of_Appliance = ["Rigid", "Elastic"]
Catwise_Appls = [["Light", "Fan", "Security Camera", "Projector", "Desktops", "Monitors"],["Laptop", "Water Pump", "Audio System"], ["AirPurifier", "Humidifier", "Dehumidifier", "AC", "Heater"], ["Printer","TV", "Rice Cooker", "Water Purifier", "Vaccum Cleaner", "Coffee Maker"], ["Dishwasher", "Washing Machine", "Microwave Oven", "Kettle", "Refrigerator"]]		

Catwise_RatedPows = [[1, 1, 1, 3, 3, 2], [1, 10, 2], [3, 3, 3, 10, 10], [5, 5, 2, 2, 2, 10], [10, 10, 10, 10, 5]]#Units of 100W
House_Type_MaxPow_Limit = [20, 40, 60, 80, 100] #*100 Watts; Multiples of hundred 
Min_NHouses_per_Type = 8
Max_NHouses_per_Type = 10
NHouses_per_Type = [rd.randint(Min_NHouses_per_Type, Max_NHouses_per_Type) for h in range(NTypes_of_Houses)]
print(NHouses_per_Type)
Appliances, RatedPows, Tariffs, Appliance_Type, Appliance_Starts,Starts_Lengths = [], [], [], [], [], []
for typ in range(NTypes_of_Houses):
	for house in range(NHouses_per_Type[typ]):
		total = 0
		while True:
			cat = rd.randint(0, NCat_of_Appls-1)
			appl_indx = rd.randint(0, len(Catwise_Appls[cat])-1)
			if (total+ Catwise_RatedPows[cat][appl_indx] > House_Type_MaxPow_Limit[typ]):
				break
			Appliances.append(Catwise_Appls[cat][appl_indx])
			RatedPows.append(Catwise_RatedPows[cat][appl_indx])
			Tariffs.append(rd.choice(PriceTariffs))
			appl_type = rd.choice(Type_of_Appliance)
			Appliance_Type.append(appl_type)
			if appl_type == "Rigid":
				NStarts = rd.randint(1, 5)
				starts = rd.sample(range(NTimeSlots-1), NStarts)
				starts.sort()
				lengths = []
				tempstarts = starts+[23]
				for l in range(NStarts):
					lengths.append(rd.randint(1,tempstarts[l+1]-tempstarts[l]))
			else:
				starts = rd.sample(range(NTimeSlots-1),3)
				starts.sort()
				lengths = rd.randint(1,min(23-starts[2], starts[2]-starts[1], starts[1]-starts[0]))
			Appliance_Starts.append(starts)
			Starts_Lengths.append([lengths])
			total+= Catwise_RatedPows[cat][appl_indx]



fields = ["Appliance", "RatedPower", "Tariff", "Type", "Starts", "Lenghts"]
data = []
for a,r,t,ty,s,l in zip(Appliances,RatedPows, Tariffs, Appliance_Type, Appliance_Starts,Starts_Lengths):
	data.append([a,r,t,ty,s,l])
print(data)

Filename = "M-id-"+str(Microgrid_id)+".csv"

with open(Filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(data) 