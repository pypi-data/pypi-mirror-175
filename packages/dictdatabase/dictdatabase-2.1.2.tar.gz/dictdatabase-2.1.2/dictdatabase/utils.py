from __future__ import annotations
from typing import Tuple
import os
import glob
from . import config


def db_paths(db_name: str) -> Tuple[str, bool, str, bool]:
	"""
	Returns a tuple of four elements, the first and third being the paths to the JSON
	and and DDB files, and the second and third being booleans indicating whether those
	files exist:

	>>> (json_path, json_exists, ddb_path, ddb_exists)

	:param db_name: The name of the database
	"""
	base = f"{config.storage_directory}/{db_name}"
	j, d = f"{base}.json", f"{base}.ddb"
	return j, os.path.exists(j), d, os.path.exists(d)


def to_path_str(s) -> str:
	"""
		Join a tuple or list using "/" as a separator.
		:param s: The string to convert to a path string.
	"""
	return "/".join(s) if isinstance(s, (tuple, list)) else s


def find(*pattern) -> list[str]:
	"""
	Returns a list of all the database names that match the given glob pattern.

	:param pattern: The glob pattern to search for
	"""
	pattern = to_path_str(pattern)
	dbs_ddb = glob.glob(f"{config.storage_directory}/{pattern}.ddb")
	dbs_json = glob.glob(f"{config.storage_directory}/{pattern}.json")
	dbs_all = dbs_ddb + dbs_json
	for trim in [f"{config.storage_directory}/", ".ddb", ".json"]:
		dbs_all = [d.replace(trim, "") for d in dbs_all]
	return dbs_all


def expand_find_path_pattern(path):
	"""
		For a tuple of path items, expand it to a list of all real paths.
		An item can be some string, a wildcard "*" or a list to select specific paths.

		Args:
		- `path`: A tuple of path items
	"""
	res = [[]]
	for item in path.split("/"):
		if isinstance(item, str):
			res = [r + [item] for r in res]
	return [f for r in res for f in find(*r)]


def seek_index_through_value(data: str, index: int) -> int:
	"""
	Finds the index of the next comma or closing bracket/brace, but only if
	it is at the same indentation level as at the start index.

	Args:
	- `data`: A vaild JSON string
	- `index`: The start index in data

	Returns:
	- The end index of the value.
	"""

	# See https://www.json.org/json-en.html for the JSON syntax

	skip_next, in_str, list_depth, dict_depth = False, False, 0, 0

	for i in range(index, len(data)):
		if skip_next:
			skip_next = False
			continue
		current = data[i]
		if current == "\\":
			skip_next = True
			continue
		if current == '"':
			in_str = not in_str
		if in_str or current == " ":
			continue
		if current == "[":
			list_depth += 1
		elif current == "]":
			list_depth -= 1
		elif current == "{":
			dict_depth += 1
		elif current == "}":
			dict_depth -= 1
		if list_depth == 0 and dict_depth == 0:
			return i + 1

	raise TypeError("Invalid JSON syntax")


def count_nesting(data: str, start: int, end: int) -> int:
	"""
	Returns the number of nesting levels between the start and end indices.

	:param data: The string to be parsed
	"""
	skip_next, in_str, nesting = False, False, 0

	for i in range(start, end):
		if skip_next:
			skip_next = False
			continue
		current = data[i]
		if current == "\\":
			skip_next = True
			continue
		if current == '"':
			in_str = not in_str
		if in_str or current == " ":
			continue
		elif current == "{":
			nesting += 1
		elif current == "}":
			nesting -= 1
	return nesting


def find_outermost_key_str_index(data: str, key: str):
	"""
		Returns the index of the key that is at the outermost nesting level.
		If the key is not found, return -1.
		If the key you are looking for is `some_key`, then you should pass
		`"some_key":` as the `key` argument to this function.
		Args:
		- `data`: Correct JSON as a string
		- `key`: The key of an object in `data` to search for
	"""
	if (curr_i := data.find(key, 0)) == -1:
		return -1

	key_nest = [(curr_i, 0)]  # (key, nesting)

	while (next_i := data.find(key, curr_i + len(key))) != -1:
		nesting = count_nesting(data, curr_i + len(key), next_i)
		key_nest.append((next_i, nesting))
		curr_i = next_i

	# Early exit if there is only one key
	if len(key_nest) == 1:
		return key_nest[0][0]

	# Relative to total nesting
	for i in range(1, len(key_nest)):
		key_nest[i] = (key_nest[i][0], key_nest[i - 1][1] + key_nest[i][1])
	return min(key_nest, key=lambda x: x[1])[0]
