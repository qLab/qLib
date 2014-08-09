"""
		@file		qliblabels.py
		@author		xy
		@since		2014-08-09

		@brief		qLib, node tagging/labeling functions (semantics).

		Location: $HIH/scripts/python/

"""

import hou
import re
import traceback
import datetime
import sys


def msg(m):
	msg = "[%s qliblabels.py] %s" % (datetime.datetime.now().strftime("%y%m%d %H:%M.%S"), str(m), )
	sys.stderr.write(msg+"\n")
	#print msg

def warn(m):
	msg('WARNING: %s' % m)

def err(m):
	msg('ERROR: %s' % m)

def dbg(m):
	msg('[debug] %s' % m)



dbg('LOADED')


# module-wide constants
#

# name/label for tags parameter
n_tags = '__tags'
l_tags = 'tags (semantics)'

# tag list separator
tags_s = ' '



def has_tags_parm(node):
	'''.'''
	#assert type(node) is hou.Node
	r = node.parm(n_tags) is not None
	return r



def add_tags_parm(node):
	'''.'''
	#assert type(node) is hou.Node

	if not has_tags_parm(node):
		pass # add tags parm

		#hou_parm_template_group = hou.ParmTemplateGroup()
		hou_parm_template_group = node.parmTemplateGroup()

		# Code for parameter template
		hou_parm_template = hou.StringParmTemplate(n_tags, l_tags,
			1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1,
			string_type=hou.stringParmType.Regular,
			menu_items=([]),
			menu_labels=([]),
			icon_names=([]),
			item_generator_script="",
			item_generator_script_language=hou.scriptLanguage.Python,
			menu_type=hou.menuType.Normal)

		hou_parm_template_group.append(hou_parm_template)

		node.setParmTemplateGroup(hou_parm_template_group)
	else:
		dbg('%s already has tags parm' % node.path() )

	return node.parm(n_tags)



def rem_tags_parm(node):
	'''.'''
	#assert

	if has_tags_parm(node):
		g = node.parmTemplateGroup()
		t = g.find(n_tags)
		if t:
			g.remove(t)
			node.setParmTemplateGroup(g)
		else:
			dbg('%s -- no tags parm found' % node.path() )

	else:
		dbg('%s has no tags parm' % node.path() )



def tags_parm(node):
	'''.'''
	return add_tags_parm(node)


def get_tag_list(node):
	'''.'''
	r = []
	if has_tags_parm(node):
		p = tags_parm(node)
		r = p.evalAsString().lower()
		# strip of spaces (in case separator is not a space)
		r = [ n.strip() for n in r.split(tags_s) ]
	return r


def set_tag_list(node, taglist):
	'''.'''
	assert type(taglist) is list, 'expecting a list of strings'
	l = [ n.strip() for n in taglist if n.strip()!='' ]
	dbg(' -- tags: %s' % str(l) )
	l = tags_s.join(l)
	dbg(' -- writing tags: "%s"' % l )
	if len(l)>0:
		p = tags_parm(node)
		p.set(l)
	else:
		dbg('(removing parm)')
		rem_tags_parm(node)




def get_label_table():
	'''.'''
	return labels


def find_all_prefixes(labels):
	'''.'''
	r = set()

	for L in labels:
		E = labels[L]

		cats = E['cats'] if 'cats' in E else []
		if 'prefix' in E:
			r.add(E['prefix'])
		for c in cats:
			p = 'prefix.%s' % c
			if p in E:
				r.add(E[p])

	r = list(r)
	return r


def get_label_data(label):
	L = get_label_table()
	r = L[label]  if label in L else  {}
	return r



def apply_color(node):
	'''.'''
	pass
	# TODO: finish this



def apply_naming(node):
	'''.'''
	"""
	TODO: make sure to
	- remove _all_ known prefixes as well, when necessary
	- rename to a default name if previous tagging had an explicit naming scheme
	"""
	pass
	c = node.type().category().name().lower() # 'sop', etc.



def process_op(node, tags, tags_prev=[]):
	'''.'''
	# TODO: set color, prefix/name, etc.
	had_prev_tags = len(tags_prev)>0

	if len(tags):
		pass # TODO: apply new color, replace prefix, etc.
	else:
		pass # TODO: reset op to its defaults




def uimsg(msg, sev=hou.severityType.Message):
	'''.'''
	hou.ui.setStatusMessage('[qLib | semantics]  %s' % str(msg), severity=sev)

def uiwarn(msg):
	uimsg(msg, sev=hou.severityType.Warning)







