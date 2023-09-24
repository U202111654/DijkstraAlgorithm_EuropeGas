import folium as fl
import pandas as pd
from folium.plugins import MiniMap
from folium.plugins import FloatImage
import random
import math
import numpy as np
import heapq as hq


class Graph:
  def __init__(self, loops=False, directed=True, weighted=False):
    self.dictG = dict()
    self.loops = loops
    self.directed = directed
    self.weighted = weighted

  def addNodes(self, nodes):
    nodes = list(nodes)
    for n in nodes:
      if n not in self.dictG:
        self.dictG[n] = []

  def addEdges(self, edges):
    if type(edges) == list:
      for e in edges:
        if self.weighted == True:
          u, v, w = e
          if u in self.dictG:
            if (v, w) not in self.dictG[u]:
             self.dictG[u].append((v, w))
          else:
            continue
        else:
          u, v = e
          if u in self.dictG:
            self.dictG[u].append((v))
          else:
            continue
    else:
      print("You need to insert a list")

  def dijkstra(self, s, t, airports_array):
    def airports_and_edges(parent, s, t, n):
      edges = []
      airports = []
      while parent[t][0] != s:
        edges.append([parent[t][0], t, parent[t][1]])
        airports.append(airports_array.find_byID(t))
        t = parent[t][0]
      edges.append([parent[t][0], t, parent[t][1]])
      airports.append(airports_array.find_byID(t))
      airports.append(airports_array.find_byID(s))
      return airports, edges

    n = len(self.dictG)
    visited = []
    path = {}
    cost = {}
    cost[s] = 0
    pqueue = [(0, s)]

    while pqueue:
      g, u = hq.heappop(pqueue)
      if u == t:
        visited.append(u)
        break
      if u not in visited:
        visited.append(u)
        for v, w in self.dictG[u]:
          if v not in visited:
            f = g + w
            if v not in cost or f < cost[v]:
              cost[v] = f
              path[v] = [u, w]
              hq.heappush(pqueue, (f, v))
    if t in visited:
      airports, edges = airports_and_edges(path, s, t, n)
      return airports, edges, cost[t]
    else:
      return [], [], []

  def bfs(self, s, t, airports_array):
    def airports_and_edges(parent, s, t, n):
      edges = []
      airports = []
      while parent[t][0] != s:
        edges.append([parent[t][0], t, parent[t][1]])
        airports.append(airports_array.find_byID(t))
        t = parent[t][0]
      edges.append([parent[t][0], t, parent[t][1]])
      airports.append(airports_array.find_byID(t))
      airports.append(airports_array.find_byID(s))
      return airports, edges

    n = len(self.dictG)
    visited = []
    path = {}
    queue = [s]
    cost = {}
    cost[s] = 0
    visited.append(s)
    while queue:
      u = queue.pop(0)
      g = cost[u]
      if u == t:
        cost[t] = g
        break
      for v, w in self.dictG[u]:
         if v not in visited:
          visited.append(v)
          cost[v] = g + w
          path[v] = [u,w]
          queue.append(v)
    if t in visited:
      airports, edges = airports_and_edges(path, s, t, n)
      return airports, edges, cost[t]
    else:
      return [], [], []

class listAirports:
  def __init__(self):
    self.array = []
    self.len = 0

  def find_byID(self, id):
    for airport in self.array:
      if id == airport.id:
        return airport
    return None

  def find_byCity(self, city):
    auxlist = []
    for airport in self.array:
      if city == airport.city:
        auxlist.append(airport)
    return auxlist

  def find_byCountry(self, country):
    auxlist = []
    for airport in self.array:
      if country == airport.country:
        auxlist.append(airport)
    return auxlist

  def addAirport(self, airport):
    self.array.append(airport)

  def add_byFile(self, file_name):
    lenFile = len(file_name)
    for i in range(lenFile):
      self.array.append(Airport(file_name['Airport ID'][i], file_name['Name'][i], file_name['Country'][i],
                                   file_name['City'][i], file_name['Latitude'][i], file_name['Longitude'][i]))
      self.len += 1

class Airport:
  def __init__(self, id, name, country, city, lat, lon):
    self.id = id
    self.name = name
    self.country = country
    self.city = city
    self.lat = lat
    self.lon = lon

  def showName(self):
    return f"{self.name} ({self.country})"

  def getPosition(self):
    return tuple([self.lat, self.lon])

class listRoutes:
  def __init__(self):
    self.array = []
    self.len = 0

  def add_byFile(self, file_name):
    lenFile = len(file_name)
    for i in range(lenFile):
      self.array.append(Route(file_name['Airline ID'][i], file_name['Source airport ID'][i],
                               file_name['Destination airport ID'][i], file_name["Distance"][i]))
      self.len += 1

class Route:
  def __init__(self, id_airline, id_departure, id_arrival, distance):
    self.id_airline = id_airline
    self.id_departure = id_departure
    self.id_arrival = id_arrival
    self.distance = distance

  def getRoute(self):
    return [self.id_departure, self.id_arrival]

  def getroute_distance(self):
    return [self.id_departure, self.id_arrival, self.distance]

def createGraph():
    path = "https://raw.githubusercontent.com/EduardoPuglisevich/A_Complexity/main/AirportsFinal.csv"
    airports_csv = pd.read_csv(path, delimiter=';')
    path = "https://raw.githubusercontent.com/EduardoPuglisevich/A_Complexity/main/routesFinal.csv"
    routes_csv = pd.read_csv(path, delimiter=';')

    airports_array = listAirports()
    airports_array.add_byFile(airports_csv)

    routes_array = listRoutes()
    routes_array.add_byFile(routes_csv)

    g = Graph(weighted=True)
    g.addNodes([airport.id for airport in airports_array.array])
    R = []
    for route in routes_array.array:
        r = route.getroute_distance()
        if r[2] == 0:
            continue
        R.append(r)
    g.addEdges(R)
    return g, airports_array, routes_array

def showOptions(city, airports_array):
    aux = airports_array.find_byCity(city)
    return [a.name for a in aux]

def findRoutes(g, airports_array, departure, arrive):
    paths = []
    paths.append(g.dijkstra(departure, arrive, airports_array))
    paths.append(g.bfs(departure,arrive, airports_array))
    return paths

def showMap(data,airports_array,routes_array):
  map = fl.Map()
  A = []
  colors = [
    'red','blue','green','darkred','lightred','orange','beige','gray',
    'darkgreen','lightgreen','darkblue','lightblue','purple','darkpurple',
    'pink','cadetblue','lightgray','black']
  for _data in data:
    airports, edges, totalCost = _data
    eColor =  colors.pop(0)
    for a in airports:
      if a not in A:
        if a == airports[0]:
          _color = 'red'
        elif a == airports[-1]:
          _color = 'green'
        else:
          _color = 'blue'

        A.append(a)
        fl.Marker(
          location = a.getPosition(),
          popup = a.name,
          icon= fl.Icon(prefix = "fa", icon = "plane", color = _color, opacity = 0.5, weight = 0.5)     
        ).add_to(map)  
    added = set()
    for e in edges:
      u,v, w = e
      draw = False
      if not f"{u},{v}" in added:
        added.add(f"{u},{v}")
        draw = True
      if draw:
        a_departure = airports_array.find_byID(u)
        a_arrive = airports_array.find_byID(v)
        fl.PolyLine([a_departure.getPosition(),a_arrive.getPosition()], color = eColor, weight=2, opacity=0.6,popup=f"Distance = {w} km",).add_to(map)
        fl.RegularPolygonMarker(location=a_arrive.getPosition(), fill_color='blue',color= 'red', number_of_sides=3, radius=5, rotation=90*math.atan((a_departure.lat-a_arrive.lat)/(a_departure.lon-a_arrive.lon))).add_to(map)
  return map
