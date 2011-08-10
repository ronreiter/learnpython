from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

import logging
import os
import urllib
import traceback
import sys
import StringIO
import types
import handlers
import simplejson
import re
import copy
import turtle

sections = re.compile(r"Tutorial\n[=\-]+\n+(.*)\n*Tutorial Code\n[=\-]+\n+(.*)\n*Expected Output\n[=\-]+\n+(.*)\n*", re.MULTILINE | re.DOTALL)

ILLEGAL_MODULES = ["os"]
ILLEGAL_PREFIXES = ["google"]

#real_import = copy.deepcopy(globals()["__builtins__"]["__import__"])

# prepare the safe exec
def safe_import(module, *args):
	if module in ILLEGAL_MODULES:
		raise ImportError("Illegal module.")
		
	if any([module.startswith(x) for x in ILLEGAL_PREFIXES]):
		raise ImportError("Illegal module.")
		
	globals()[module] = real_import(module, *args)

class TutorialHandler(webapp.RequestHandler):
	def get(self):
		tutorial_id = self.request.get("id")
		tutorial_page = handlers.PageHandler()._get_page(tutorial_id)

		tutorial_data = {}
		tutorial_data["title"] = "Page %s does not exist." % tutorial_id
		tutorial_data["code"] = ""
		tutorial_data["output"] = ""
		
		if not tutorial_page["page_exists"]:
			tutorial_data["text"] = "Click <a href='/%s'>here</a> to create the page." % urllib.quote(tutorial_id)
		else:
		
			tutorial_sections = sections.findall(tutorial_page["page_options"]["text"])
			if tutorial_sections:
				text, code, output = tutorial_sections[0]
				tutorial_data["title"] = tutorial_page["page_title"]
				tutorial_data["text"] = handlers.wikify(text)
				tutorial_data["code"] = code.replace("\t", "").strip()
				tutorial_data["output"] = output.replace("\t", "").strip()
			else:
				tutorial_data["text"] = tutorial_page["page_options"]["text"]
			
		
		self.response.out.write(simplejson.dumps(tutorial_data))
			

class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		template_values = {}
		welcome_page = handlers.PageHandler()._get_page("Welcome")
		if not welcome_page["page_exists"]:
			template_values["welcome"] = "No welcome page."
		else:
			template_values["welcome"] = welcome_page["page_text"]
		
		self.response.out.write(template.render(path, template_values))

	def post(self):
		temp_stdout = sys.stdout
		sys.stdout = StringIO.StringIO()
		
		# get the POST data, unquote and strip
		cmd = list(self.request.POST)[0]
		cmd = cmd.replace(u"\xa0", "")
		
		logging.info("command: %s" % repr(cmd))
		data = {}
		data["output"] = "text"
		
		try:
			#safe_globals = prepare_safe_globals()
			#safe_globals = {
			#	"__builtins__": None, "dir" : dir, "help" : help, "range": range, "xrange": xrange,
			#	#['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError','SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs','all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super','tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']
			#}
			#safe_builtins = __builtins__
			#safe_builtins.__import__ = safe_import
			#safe_builtins.__import__ = None
			#safe_globals = {"__builtins__" : safe_builtins}
			turtle.init_track()
			
			safe_globals = {"go": turtle.go, "turn": turtle.turn}
			exec(cmd, safe_globals)
			if turtle.is_drawing():
				data = turtle.get_data()
			else:
				# get output from buffer
				data["text"] = sys.stdout.getvalue()
			
		except Exception, e:
			exception_data = StringIO.StringIO()
			traceback.print_exc(file=exception_data)
			exception_data.seek(0)
			data["output"] = "exception"
			data["text"] = "%s\r\n" % exception_data.read()
		
		sys.stdout = temp_stdout
	
		logging.info("data: %s" % simplejson.dumps(repr(data)))
		self.response.out.write(simplejson.dumps(data))
		
		
def main():
	application = webapp.WSGIApplication([
		('/tutorial/', TutorialHandler),
		('/', MainHandler),
	], debug=True)
	util.run_wsgi_app(application)

	
if __name__ == '__main__':
	main()
