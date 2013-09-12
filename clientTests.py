#!/usr/bin/python

import unittest 
from client import *

class ClientTester(unittest.TestCase):

   # Test the parse_data function
   def test_parse_data(self):
       data = "a b c"
       result = parse_data(data)
       self.assertEqual(result, ["a", "b", "c"])

   def test_is_operator(self):
       self.assertTrue(is_operator("+"))
       self.assertTrue(is_operator("-"))
       self.assertTrue(is_operator("*"))
       self.assertTrue(is_operator("/"))
       self.assertFalse(is_operator("8"))

   def test_is_valid_msg(self):
       self.assertTrue(is_valid_msg(["cs5700fall2013", "fdsafsa", "BYE\n"]))
       self.assertFalse(is_valid_msg(["cs5700fall2013", "fdsafsa", "BYE"]))
       self.assertTrue(is_valid_msg(["cs5700fall2013", "STATUS", "1", "+", "2\n"]))
       self.assertTrue(is_valid_msg(["cs5700fall2013", "STATUS", "1", "-", "2\n"]))
       self.assertTrue(is_valid_msg(["cs5700fall2013", "STATUS", "1", "*", "2\n"]))
       self.assertTrue(is_valid_msg(["cs5700fall2013", "STATUS", "1", "/", "2\n"]))
       self.assertFalse(is_valid_msg(["cs5700fall2013", "STATUS", "1", "%", "2\n"]))

   def test_calculate_solution(self):
       self.assertEqual(3, calculate_solution("1", "+", "2"))
       self.assertEqual(-1, calculate_solution("1", "-", "2"))
       self.assertEqual(2, calculate_solution("1", "*", "2"))
       self.assertEqual(2, calculate_solution("4", "/", "2"))
       self.assertEqual(0, calculate_solution("1", "/", "2"))
       self.assertEqual(1, calculate_solution("5", "/", "3"))

unittest.main()
