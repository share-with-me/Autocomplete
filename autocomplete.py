from flask import Flask, Response, render_template, request, jsonify
app = Flask(__name__)

import wtforms as wt
from wtforms import TextField, Form

NAMES=["Heee","How are you","How old are you","What is your name","India", "Indian", "Indians", "Ind", "Hindi"]

queries = []

class Node:
	def __init__(self):
		self.next = {}
		self.end_word = False

	def add_item(self, string):
		if len(string) == 0:
			self.end_word = True
			return

		key = string[0]
		string = string[1:]

		if self.next.has_key(key):
			self.next[key].add_item(string)
		else:
			node = Node()
			self.next[key] = node
			node.add_item(string)

	def dfs(self, traversed=None):
		if self.next.keys() == []:
			queries.append(traversed)
			return
		if self.end_word == True:
			queries.append(traversed)

		for key in self.next.keys():
			self.next[key].dfs(traversed + key)

	def search(self, string, traversed=""):
		if len(string) > 0:
			key = string[0]
			string = string[1:]
			if self.next.has_key(key):
				traversed = traversed + key
				self.next[key].search(string, traversed)
			else:
				queries.append('Not Found')
		else:
			if self.end_word == True:
				queries.append(traversed)
			for key in self.next.keys():
				self.next[key].dfs(traversed + key)


def createTrie(NAMES):
	root = Node()
	for name in NAMES:
		root.add_item(name)

	return root


class SearchForm(Form):
    autocomp= TextField('AutoComplete Feature',id='autocomplete')

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    searchVals = request.args.get('q')
    del queries[:]
    root = createTrie(NAMES)
    app.logger.debug(searchVals)
    root.search(searchVals)
    app.logger.debug(queries)
    keys = root.next.keys()
    app.logger.debug(keys)
    return jsonify(json_list=queries)

@app.route('/',methods=['GET','POST'])
def index():

    form = SearchForm(request.form)
    return render_template("search.html",form=form)

if __name__ == '__main__':
    app.run(debug=True)
