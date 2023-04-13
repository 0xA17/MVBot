import unittest
import mvbot
import requests
import json

from parser import Parser
from database import Database
from apiOperation import ApiOperation
from stringValidation import StringValidation

class TestMvbot(unittest.TestCase):
      
  def setUp(self):
    self.stringValidation = StringValidation()
      
  def test_ShortenText(self):
    self.assertEqual(StringValidation.SearchValidation(Database('db.db'), 514133808), "2425345")
      
  def test_SearchValidation(self):
    self.assertEqual(StringValidation.ShortenText("testString", 4), "test...")
    
  def test_GenreStrValidation(self):
    self.assertEqual(StringValidation.GenreStrValidation("testGenreStrValidation"), 
                     "t, e, s, t, G, e, n, r, e, S, t, r, V, a, l, i, d, a, t, i, o, n.")
        
  def setUp(self):
    self.parser = Parser()
        
  def test_GetDataFromCSV(self):
    with open("kinopoisk-top250.csv") as f_obj:
        self.assertIsNotNone(Parser.GetDataFromCSV(f_obj))
            
  def setUp(self):
    self.database = Database('db.db')
    
  def test_DBConnection(self):
    self.assertIsNotNone(Database.GetCurrentDBConnection())
        
  def setUp(self):
    self.apiOperation = ApiOperation()

  def test_APIReader(self):
    response = requests.get(
        f"https://api.kinopoisk.dev/movie?search=Прикол&field=name&isStrict=false&token={mvbot.API_TOKEN}")
    self.assertIsNotNone(ApiOperation.APIReader(json.loads(response.text)))
  
  def test_API_ID_Reader(self):
    response = requests.get(f"https://api.kinopoisk.dev/movie?search=1045585&field=id&token={mvbot.API_TOKEN}")
    self.assertIsNotNone(ApiOperation.API_ID_Reader(json.loads(response.text)))
    
  def test_ReviewReader(self):
    response = requests.get(
        f"https://api.kinopoisk.dev/review?search=326&field=movieId&token={mvbot.API_TOKEN}")
    self.assertIsNotNone(ApiOperation.ReviewReader(json.loads(response.text)))
    
  def test_PersonReader(self):
    response = requests.get(
        f"https://api.kinopoisk.dev/person?search=Джонни&field=name&token={mvbot.API_TOKEN}")
    self.assertIsNotNone(ApiOperation.PersonReader(json.loads(response.text)))
    
    
if __name__ == "__main__":
  unittest.main()
  
  #python testMvbot.py -v