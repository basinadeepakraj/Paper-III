#!/usr/bin/env python3
import sys 
import os 
import numpy as np 
import csv 
import random as rd 
class DataGeneration:
	def __init__(self, Microgrid_id):
		Appliance_Filename = "datafiles/M-"+str(Microgrid_id)+"-Appliances.csv"
		Resource_Filename = "M-"+str(Microgrid_id)+"-Resources.csv"
		rd.seed(Microgrid_id)
		#Constant Variables 
		self.NTimeSlots = 24
		self.PriceTariffs = [1, 2, 3, 4, 5, 6, 7, 8] #Currency units 
		NTypes_of_Houses = 5 
		NCat_of_Appls = 5 # Number of categories of applianes 
		Type_of_Appliance = ["Rigid", "Elastic"]
		Catwise_Appls = [["Light", "Fan", "Security Camera", "Projector", "Desktops", "Monitors"],["Laptop", "Water Pump", "Audio System"], ["Air Purifier", "Humidifier", "Dehumidifier", "AC", "Heater"], ["Printer","TV", "Rice Cooker", "Water Purifier", "Vacuum Cleaner", "Coffee Maker"], ["Dishwasher", "Washing Machine", "Microwave Oven", "Kettle", "Refrigerator"]]
		Catwise_RatedPows = [[1, 1, 1, 3, 3, 2], [1, 10, 2], [3, 3, 3, 10, 10], [5, 5, 2, 2, 2, 10], [10, 10, 10, 10, 5]]#Units of 100W
		House_Type_MaxPow_Limit = [20, 40, 60, 80, 100] #*100 Watts; Multiples of hundred 
		Min_NHouses_per_Type = 1000
		Max_NHouses_per_Type = 1500
		Catwise_tariffmeans = [6.5, 5.5, 4.5, 3.5, 2.5]
		Catwise_tariffstddev = [.75]*5
		NHouses_per_Type = [rd.randint(Min_NHouses_per_Type, Max_NHouses_per_Type) for h in range(NTypes_of_Houses)]
		# print(NHouses_per_Type)
		Appliances, RatedPows, Tariffs, Appliance_Type, Appliance_Starts,Starts_Lengths = [], [], [], [], [], []
		for typ in range(NTypes_of_Houses):
			for house in range(NHouses_per_Type[typ]):
				total = 0
				while True:
					cat = rd.randint(0, NCat_of_Appls-1)
					appl_indx = rd.randint(0, len(Catwise_Appls[cat])-1)
					while(1):
						tar = round(rd.normalvariate(Catwise_tariffmeans[cat],Catwise_tariffstddev[cat]))
						if tar in self.PriceTariffs:
							break
					if (total+ Catwise_RatedPows[cat][appl_indx] > House_Type_MaxPow_Limit[typ]):
						break
					appl_type = rd.choice(Type_of_Appliance)					
					if appl_type == "Rigid":
						NStarts = rd.randint(1, 5)
						starts = rd.sample(range(self.NTimeSlots), NStarts)
						starts.sort()
						_temp = starts+[24]
						for l in range(NStarts):							
							Appliances.append(Catwise_Appls[cat][appl_indx])
							RatedPows.append(Catwise_RatedPows[cat][appl_indx])
							Tariffs.append(tar)
							Appliance_Type.append(appl_type)												
							Appliance_Starts.append([starts[l]])
							Starts_Lengths.append(rd.randint(1,_temp[l+1]-_temp[l]))
					else:
						starts = rd.sample(range(self.NTimeSlots-1),3)
						starts.sort()
						lengths = rd.randint(1,min(23-starts[2], starts[2]-starts[1], starts[1]-starts[0]))						
						Appliances.append(Catwise_Appls[cat][appl_indx])
						RatedPows.append(Catwise_RatedPows[cat][appl_indx])
						Tariffs.append(tar)
						Appliance_Type.append(appl_type)	
						Appliance_Starts.append(starts)
						Starts_Lengths.append(lengths)
					total+= Catwise_RatedPows[cat][appl_indx]



		# fields = ["ID", "Appliance", "Rated Power", "Tariff", "Type", "Starts", "Lenghts", "Revenue", "Key"]
		self.appl_data = [["ID", "Appliance", "Rated Power", "Tariff", "Type", "Starts", "Lengths"]]
		for i,a,r,t,ty,s,l in zip(range(1,len(Appliances)+1),Appliances,RatedPows, Tariffs, Appliance_Type, Appliance_Starts,Starts_Lengths):
			self.appl_data.append([i,a,r,t,ty,s,l])
		# print(data)
		with open(Appliance_Filename, 'w') as csvfile:  
		    csvwriter = csv.writer(csvfile)  
		    csvwriter.writerows(self.appl_data)

		self.res = [rd.randint(8000, 10000) for j in range(self.NTimeSlots)]
		# print(Res)
		# with open(Resource_Filename, 'w') as csvfile:  
		#     csvwriter = csv.writer(csvfile)  
		#     csvwriter.writerows(Res)
