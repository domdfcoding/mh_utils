# stdlib
from itertools import chain, permutations
from pathlib import PureWindowsPath
from typing import Any, Iterable

# 3rd party
import pytest

# this package
from mh_utils.utils import as_path, camel_to_snake, element_to_bool
from tests.common import Len, counts, double_chain, true_false_strings, whitespace, whitespace_perms


class TestAsPath:
	filenames = pytest.mark.parametrize(
			"value, expects",
			[
					("foo", PureWindowsPath("foo")),
					("foo/bar", PureWindowsPath("foo/bar")),
					("foo/bar/file.txt", PureWindowsPath("foo/bar/file.txt")),
					("C:/foo/bar/file.txt", PureWindowsPath("C:/foo/bar/file.txt")),
					]
			)

	@whitespace_perms
	@counts
	def test_as_path_whitespace_none(self, char: str, count: int):
		assert as_path(char * count) is None

	@pytest.mark.parametrize("value", [None, [], (), set(), {}, 0, False])
	def test_as_path_none(self, value):
		assert as_path(value) is None

	@pytest.mark.parametrize("whitespace_pos", ["left", "right", "both"])
	@counts
	@whitespace_perms
	@filenames
	def test_as_path(
			self,
			whitespace_pos,
			count,
			char,
			value,
			expects,
			):

		if whitespace_pos == "left":
			with_whitespace = f"{char * count}{value}"
		elif whitespace_pos == "right":
			with_whitespace = f"{value}{char * count}"
		elif whitespace_pos == "both":
			with_whitespace = f"{char * count}{value}{char * count}"
		else:
			with_whitespace = value

		assert as_path(with_whitespace) == expects

	@filenames
	def test_as_path_no_whitespace(
			self,
			value,
			expects,
			):

		assert as_path(value) == expects


class TestElementToBool:

	@pytest.mark.parametrize(
			"obj, expects",
			true_false_strings,
			)
	def test_element_to_bool(self, obj, expects):
		assert element_to_bool(obj) == expects

	@pytest.mark.parametrize(
			"obj, expects",
			[
					("truthy", ValueError),
					("foo", ValueError),
					("bar", ValueError),
					(None, ValueError),  # AttributeError in domdf_python_tools
					(1.0, ValueError),  # AttributeError in domdf_python_tools
					(0.0, ValueError),  # AttributeError in domdf_python_tools
					(50, ValueError),  # valid in domdf_python_tools
					("50", ValueError),  # also invalid in domdf_python_tools
					],
			)
	def test_element_to_bool_errors(self, obj, expects):
		with pytest.raises(expects):
			element_to_bool(obj)


@pytest.mark.parametrize(
		"value, expects",
		[
				("HelloWorld", "hello_world"),
				("Hello_World", "hello__world"),
				("Helloworld", "helloworld"),
				("BizBazBar", "biz_baz_bar"),
				("biz_baz_bar", "biz_baz_bar"),
				("HELLOWORLD", "helloworld"),  # not h_e_l_l_o_w_o_r_l_d
				("HELLOWorld", "hello_world"),
				]
		)
def test_camel_to_snake(value, expects):
	assert camel_to_snake(value) == expects
