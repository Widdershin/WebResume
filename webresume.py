from jinja2 import Template

output_filename = "test.html"

def open_and_read(filename):
	with open(filename) as f:
		return f.read()

template = Template(open_and_read("cv.html"))

with open(output_filename, 'w') as o:
	o.write(template.render(test="nifty as fuck", lorem=open_and_read("lorem.txt").split('\n')))

print "Output saved to {}".format(output_filename)