import markdown

def open_and_read(filename):
	with open(filename) as f:
		return f.read()

md = markdown.markdown(open_and_read("test.md"))
head = open_and_read("head.html")

with open("test.html", 'w') as o:
	o.write("{}\n<body>\n{}\n</body>".format(head, md))