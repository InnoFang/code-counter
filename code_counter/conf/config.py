#!/usr/bin/env python3
# coding:utf8
import json  
import sys
import pkg_resources

class Config:

	def __init__(self, args):
		if args.restore:
			self.__restore()
			return 
		
		conf = self.__load()
		self.suffix = args.suffix if args.suffix else conf['suffix']
		self.comment = args.comment if args.comment else conf['comment']
		self.ignore = args.ignore if args.ignore else conf['ignore']

		if any([args.suffix_add, args.comment_add, args.ignore_add]):
			self.__append_config(args.suffix_add, args.comment_add, args.ignore_add)

		if any([args.suffix_save, args.comment_save, args.ignore_save]):
			self.__save_config(args.suffix_save, args.comment_save, args.ignore_save)
			
	def show(self):
		print(json.dumps(self.__dict__, indent=4))
	
	def __confirm(self,tips):
		check = input(tips)
		return check.strip().lower() == 'y'

	def __append_config(self, suffix_add, comment_add, ignore_add):
		if suffix_add:
			if self.__confirm("'suffix' will be appended with {} (y/n)".format(suffix_add)):
				self.suffix.extend(suffix_add)
		if comment_add:
			if self.__confirm("'comment' will be appended with {} (y/n)".format(comment_add)):
				self.comment.extend(comment_add)
		if ignore_add:
			if self.__confirm("'ignore' will be appended with {} (y/n)".format(ignore_add)):
				self.ignore.extend(ignore_add)

		self.__update()
	
	def __save_config(self, suffix_save, comment_save, ignore_save):
		if suffix_save:
			if self.__confirm("'suffix' will be replaced with {} (y/n)".format(suffix_save)):
				self.suffix = suffix_save
		if comment_save:
			if self.__confirm("'comment' will be replaced with {} (y/n)".format(comment_save)):
				self.comment = comment_save
		if ignore_save:
			if self.__confirm("'ignore' will be replaced with {} (y/n)".format(ignore_save)):
				self.ignore = ignore_save

		self.__update()
		
	def __restore(self):
		self.suffix = ["py", "java", "c", "h", "cpp", "hpp", "js", "pde", "kt", "dart", "go", "lisp", "cu", "cuh"]
		self.comment = ["#", "//", "/*", "*", ":", ";"]
		self.ignore = ["out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode"]

		if self.__confirm('Default configuration will be restored (y/n)?'):
			self.__update()

	def __load(self):
		filename = pkg_resources.resource_filename(__name__, 'config.json')
		with open(filename, 'r') as config:
			conf = json.load(config)
		return conf
	
	def __update(self):
		filename = pkg_resources.resource_filename(__name__, 'config.json')
		with open(filename,'w') as config:
			json.dump(self.__dict__, config, indent=4)
	
