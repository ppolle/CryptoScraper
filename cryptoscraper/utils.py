import re
from datetime import datetime

def get_slug(text):
	return text[text.find("(")+1:text.find(")")]

def get_name(text):
	return re.sub(r'\([^)]*\)|\n', '', text)

def get_num(text):
	if any(char.isdigit() for char in text):
		return  float(re.sub("[^0-9.]", "", text))
	else:
		return 0.0

def get_date(text):
	return datetime.strptime(text, '%Y-%m-%d')
