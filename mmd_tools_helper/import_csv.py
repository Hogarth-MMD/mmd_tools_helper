import bpy
import csv

# Each row read from the csv file is returned as a list of strings.

def use_csv_bones_dictionary():
	bones_dictionary = (__file__ + "bones_dictionary.csv").replace("import_csv.py" , "")
	with open(bones_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		BONES_DICTIONARY = [tuple(x) for x in CSVreader]

	# print('\n')
	# print("BONES_DICTIONARY = ")
	# for t in BONES_DICTIONARY:
		# print(t , ",")

	return BONES_DICTIONARY


def use_csv_bones_fingers_dictionary():
	finger_bones_dictionary = (__file__ + "bones_fingers_dictionary.csv").replace("import_csv.py" , "")
	with open(finger_bones_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		FINGER_BONES_DICTIONARY = [tuple(x) for x in CSVreader]

	# print('\n')
	# print("FINGER_BONES_DICTIONARY = ")
	# for t in FINGER_BONES_DICTIONARY:
		# print(t , ",")

	return FINGER_BONES_DICTIONARY

def use_csv_translations_dictionary():
	translations_dictionary = (__file__ + "translations.csv").replace("import_csv.py" , "")
	with open(translations_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		TRANSLATIONS_DICTIONARY = [tuple(x[:2]) for x in CSVreader]

	# print('\n')
	# print("TRANSLATIONS_DICTIONARY = ")
	# for t in TRANSLATIONS_DICTIONARY:
		# print(t , ",")

	return TRANSLATIONS_DICTIONARY
