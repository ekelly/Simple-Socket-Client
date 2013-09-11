#!/usr/bin/python

import unittest 
from client import *

class ClientTester(unittest.TestCase):

   # Test the parse_data function
   def test_parse_data(self):
       data = "a b c"
       result = parse_data(data)
       self.assertEqual(result, ["a", "b", "c"])

   def test_num(self):
       self.assertEqual(num("1"), 1)
       self.assertEqual(num("1.2"), 1.2)

   def test_calculate_solution(self):
       self.assertEqual(3, calculate_solution("1", "+", "2"))
       self.assertEqual(-1, calculate_solution("1", "-", "2"))
       self.assertEqual(2, calculate_solution("1", "*", "2"))
       self.assertEqual(2, calculate_solution("4", "/", "2"))
       self.assertEqual(0, calculate_solution("1", "/", "2"))
       self.assertEqual(1, calculate_solution("5", "/", "3"))

unittest.main()
