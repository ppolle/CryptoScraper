import re
from datetime import datetime

def get_slug(text):
	return text[text.find("(")+1:text.find(")")].strip()

def get_name(text):
	return re.sub(r'\([^)]*\)|\n', '', text).strip()

def get_num(text):
	if text is not None:
		if any(char.isdigit() for char in text):
			return  float(re.sub("[^0-9.]", "", text.strip()))
		else:
			return 0.0
	else:
		return 0.0

def get_date(text):
	return datetime.strptime(text, '%Y-%m-%d')

def get_date2(text):
	return datetime.strptime(text, '%b %d, %Y')

def sanitize_string(text):
	if isinstance(text, list):
		return [re.sub(r'\n', '', x.lstrip(':')) for x in text]
	else:
		return re.sub(r'\n', '', text.lstrip(':'))
