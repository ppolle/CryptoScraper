import re
from datetime import datetime

def get_slug(text):
	return text[text.find("(")+1:text.find(")")].strip()

def get_name(text):
	return re.sub(r'\([^)]*\)|\n', '', text).strip()

def get_num(text):
	if text is not None:
		if any(char.isdigit() for char in text):
			return  float(re.sub("[^0-9.-]", "", text.strip()))
		else:
			return None
	else:
		return None

def get_date(text):
	try:
		return datetime.strptime(text, '%Y-%m-%d')
	except Exception:
		return None

def get_date2(text):
	try:
		return datetime.strptime(text, '%b %d, %Y')
	except Exception:
		return None

def sanitize_string(text):
	if isinstance(text, list):
		updated_list = [re.sub(r'\n', '', x.lstrip(':')) for x in text]
		return [i for i in updated_list if i]
	else:
		return re.sub(r'\n', '', text.lstrip(':'))

