from jinja2 import Template
from datetime import date
import time
import json
import math
import hashlib
import webcolors

JSON_DATE_FORMAT = "%Y, %m, %d"


def parse_date(string, format):
	raw_time = time.strptime(string, format)
	return date(raw_time.tm_year, raw_time.tm_mon, raw_time.tm_mday)


def parse_json(filename):
	with open(filename) as j:
		data_dict = json.load(j)
	print data_dict

def hash_color_tint(string, rgb_tint):
	h = hashlib.new("sha1")
	h.update(string)
	hex_color = "#{}".format(str(h.hexdigest()[:6]))

	rgb_color = webcolors.hex_to_rgb(hex_color)

	def avg2(a, b):
		return (a + b) / 2

	rgb_color_tinted = (avg2(rgb_color[0],rgb_tint[0]), avg2(rgb_color[1], rgb_tint[1]), avg2(rgb_color[2], rgb_tint[2]))

	return webcolors.rgb_to_hex(rgb_color_tinted)


def open_and_read(filename):
	with open(filename) as f:
		return f.read()


def tidy_date(date):
	"""
	Returns the formatted version of the raw Date() class for use in template
	"""
	return date.strftime("%B %Y")


class PersonalDetail(object):
	def __init__(self, label, detail):
		self.label = label
		self.detail = detail


class Employment(object):
	def __init__(self, title, employer, start_date, description="", finish_date=None):
		self.title = title
		self.employer = employer
		self.start_date = start_date
		self.finish_date = finish_date
		self.start_date_formatted = tidy_date(self.start_date)
		self.color = hash_color_tint(self.title + self.employer, (215, 215, 215))

		if self.finish_date is not None:
			self.finish_date_formatted = tidy_date(self.finish_date)
		else:
			self.finish_date_formatted = "Current"

		self.description = description


	def get_job_length(self):
		if self.finish_date is None:
			return (date.today() - self.start_date).days
		else:
			return (self.finish_date - self.start_date).days


class EmploymentLength(object):
	def __init__(self, employment):
		self.employment = employment
		self.start_date = employment.start_date
		self.finish_date = employment.finish_date
		self.employment_length = employment.get_job_length()
		self.color = employment.color

class YearMarker(object):
	def __init__(self, year, percent):
		self.year = year
		self.percent = percent

def main():
	output_filename = "test.html"

	template = Template(open_and_read("cv.html"))

	details = []
	jobs = []

	with open("test.json") as j:
		json_data = json.load(j)
		for key in json_data.keys():
			
			if key == "details":
				for k, v in json_data[key].items():
					details.append(PersonalDetail(k, v))

			if key == "profile":
				profile = json_data[key]['text'].replace('\n', '<br>')

			if key == "jobs":
				for job in json_data[key]:

					finish_date = None
					if "finish_date" in job:
						finish_date = parse_date(job["finish_date"], JSON_DATE_FORMAT)
					
					jobs.append(Employment(job["title"], job["employer"], parse_date(job["start_date"], JSON_DATE_FORMAT), job["description"], finish_date))


	job_lengths = []
	for job in jobs:
		job_lengths.append(EmploymentLength(job))


	first_day = date.today()
	for job_length in job_lengths:
		if job_length.start_date < first_day:
			first_day = job_length.start_date

	total_days = (date.today() - first_day).days

	years = []

	year_count = int(math.ceil(total_days / 365.25))

	for year in range(first_day.year + 1, first_day.year + year_count):
		years.append(YearMarker(year, (date(year, 1, 1) - first_day).days / float(total_days) * 100))


	for job_length in job_lengths:
		job_length.employment_length_percent = job_length.employment_length / float(total_days) * 100
		job_length.start_length_percent = (job_length.start_date - first_day).days / float(total_days) * 100

	with open(output_filename, 'w') as o:
		o.write(template.render(details=details, profile=profile, jobs=jobs, job_lengths=job_lengths, years=years))

	print "Output saved to {}".format(output_filename)

if __name__ == '__main__':
	main()

