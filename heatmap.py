import pandas as pnd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Snap_Heatmap:
	def __init__(self):
		self._dates_str = list()

	#Concatenate the new list to the member
	def fill_dates(self, dates):
		self._dates_str.append(dates)

	#Remove all duplicate dates
	def sort_uniq_dates(self):
		self._dates_str = sorted(set(self._dates_str))

	#Convert all the string dates into datetime object
	def convert_str_to_date(self):
		return pnd.to_datetime(self._dates_str, format='%Y-%m-%d %H:%M:%S')

	def compute_dates(self, dates):
		#Create a DataFrame
		data = pnd.DataFrame({'dates': dates})

		#Extract the hour and day of the week
		data['hour'] = data['dates'].dt.hour
		data['day_of_week'] = data['dates'].dt.dayofweek

		#Normalize day_of_week so that the two Mondays are considered the same
		data['day_of_week'] = (data['day_of_week'] - data['day_of_week'].min()) % 7

		return data

	def generate_heatmap(self):
		self.sort_uniq_dates()
		dt_dates = self.convert_str_to_date()
		data = self.compute_dates(dt_dates)

		#Create a matrix to store counts
		heatmap_matrix = np.zeros((24, 7))

		#Fill the matrix with counts
		for _, row in data.iterrows():
		    heatmap_matrix[row['hour']][row['day_of_week']] += 1

		#Create a heatmap using seaborn
		plt.figure(figsize=(12, 8))
		sns.heatmap(heatmap_matrix, cmap="BuPu", xticklabels=1, yticklabels=False, annot=True)  # Remove ytick labels

		#Set axis labels
		plt.xlabel('Day of the Week')
		plt.ylabel('Hour of the Day')

		#Set x and y axis labels based on the day of the week and hours
		days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		hours_of_day = [str(i) + ':00' for i in range(24)]
		plt.xticks(np.arange(7) + 0.5, days_of_week)
		plt.yticks(np.arange(24) + 0.5, hours_of_day)

		plt.title('Upload Time Heatmap')
		plt.show()

	def create_heatmap(self):
		self.generate_heatmap()