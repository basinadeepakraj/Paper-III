import csv
import sys
from datageneration import DataGeneration
from linkedlistv2 import ApplianceSSLL
import time
import numpy as np


class Heuristic:
	def __init__(self, Microgrid_id):
		self.data_obj = DataGeneration(Microgrid_id)

		# print(self.data_obj.appl_data)
		# print(self.data_obj.res)
		# print(len(self.data_obj.appl_data))
		self.bs = [-1 for a in range(len(self.data_obj.appl_data))]
		self.heuristic_best()
		self.generate_demandlevels()
		# print(self.data_obj.res)

		# print(len(self.bs))


	def heuristic_best(self):
		A_dash = ApplianceSSLL()

		for row in self.data_obj.appl_data[1:]:
			idx = row[0]
			r,t,l = row[2],row[3],row[6]
			if l==1:
				rev = (r*t)
			else:
				rev = round((r*t*l)*((1.1**(l-1))/0.8),3)
			key = round(rev/(l*r),3)
			# print(key)
			cin = 0 #initially
			A_dash.insert(idx, key, cin)
		sum_res = sum(self.data_obj.res)
		while A_dash.isnotempty() and sum_res != 0:
			idx, key, cin = A_dash.pop()
			row = self.data_obj.appl_data[idx]
			r,t,app,st,l = row[2],row[3],row[4],row[5],row[6]
			flag = 1
			for le in range(l):
				if row[2] > self.data_obj.res[st[cin]+le]:
					flag = 0
					break
			if flag:
				self.data_obj.res[st[cin]] -= r
				sum_res -= r
				self.bs[idx] = st[cin]
			else:
				if app == "Rigid" or cin==2:
					continue
				else:
					cin+=1
					if l==1:
						rev = (r*t)/((1.2**(cin))/0.7)
					else:
						rev = round( ( (r*t*l) * ((1.1**(l-1))/0.8) ) / ((1.2**(cin))/0.7) ,3 )

					key = round(rev/(l*r),3)
					A_dash.insert(idx, key, cin)

	def generate_demandlevels(self,):
		Consol_demand = [[0]*len(self.data_obj.PriceTariffs) for i in range(self.data_obj.NTimeSlots)]
		Consol_revenue = [[0]*len(self.data_obj.PriceTariffs) for i in range(self.data_obj.NTimeSlots)]
		Demand_levels = [[0]*len(self.data_obj.PriceTariffs) for i in range(self.data_obj.NTimeSlots)]
		Revenues = [[0]*len(self.data_obj.PriceTariffs) for i in range(self.data_obj.NTimeSlots)]
		for i,b in enumerate(self.bs):
			if b != -1:
				row = self.data_obj.appl_data[i]
				app,rp,tar,typ,st,le = row[1], row[2], row[3], row[4], row[5], row[6]
				for ts in range(b, b+le):
					Consol_demand[ts][tar-1] += rp
					for ele in range(8-tar,8):
						Demand_levels[ts][ele] += rp
					if le==1:
						if typ =="Rigid":
							rev = rp*tar
						else:
							cin = st.index(b)
							if cin == 0:
								rev = rp*tar
							else:
								rev = rp*tar/ ((1.2**(cin))/0.7)
							
					else:
						if typ == "Rigid":
							rev = rp*tar*le*((1.1**(le-1))/0.8)
						else:
							cin = st.index(b)
							if cin == 0:
								rev = rp*tar*le*((1.1**(le-1))/0.8)
							else:
								rev = rp*tar*le*((1.1**(le-1))/0.8)/ ((1.2**(cin))/0.7)
					Consol_revenue[ts][tar-1] += round(rev)
					for ele in range(8-tar,8):
						Revenues[ts][ele] += round(rev)
			with open("datafiles/DemandLevels.csv", 'w') as csvfile:  
				csvwriter = csv.writer(csvfile)  
				csvwriter.writerows(Demand_levels)
			with open("datafiles/Revenues.csv", 'w') as csvfile:  
				csvwriter = csv.writer(csvfile)  
				csvwriter.writerows(Revenues)




if __name__ == '__main__':
	Heuristic(1)
