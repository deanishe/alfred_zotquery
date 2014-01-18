#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from dependencies import applescript
import alp
import json
from _zotquery import zot_string, prepare_feedback

"""
This script searches within the tag chosen in the previous step (z:tag) for the queried term.
""" 

# First, ensure that Configuration has taken place
if os.path.exists(alp.storage(join="first-run.txt")):

	# Get Zotero data from JSON cache
	with open(alp.storage(join='zotero_db.json'), 'r') as f:
		zot_data = json.load(f)
		f.close()

	query = alp.args()[0]
	#query = 'epistem'

	if len(query) <= 3:
		res_dict = {'title': 'Error', 'subtitle': "Need at least 4 letters to execute search", 'valid': False, 'uid': None, 'icon': 'icons/n_delay.png'}
		res_item = alp.Item(**res_dict)
		alp.feedback(res_item)
	else:
		matches = []
		for item in zot_data:
			if item['attachments'] != []:
			
				for key, val in item.items():
					if key == 'data':
						for sub_key, sub_val in val.items():
							if sub_key in ['title', 'container-title', 'collection-title']:
								if query.lower() in sub_val.lower():
									matches.insert(0, item)
							elif sub_key in ['note', 'event-place', 'source', 'publisher', 'abstract']:
								if query.lower() in sub_val.lower():
									matches.append(item)
								
					# Since the creator key contains a list
					elif key == 'creator':
						for i in val:
							for key1, val1 in i.items():
								if val1.lower().startswith(query.lower()):
									matches.insert(0, item)

		if matches != []:

			# Rank the results
			results = alp.fuzzy_search(query, matches, key=lambda x: zot_string(x))
				
			alp_res = prepare_feedback(results)

			# Remove any duplicate items
			xml_res = list(set([x for x in alp_res]))
					
			alp.feedback(xml_res)
		else:
			alp.feedback(alp.Item(**{'title': "Error", 'subtitle': "No results found.", 'valid': False, 'icon': 'icons/n_error.png'}))

# Not configured
else:
	a_script = """
			tell application "Alfred 2" to search "z:config"
			"""
	applescript.asrun(a_script)