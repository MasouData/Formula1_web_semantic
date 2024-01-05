import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from rdflib.namespace import OWL, RDFS
import numpy as np

circuits_df = pd.read_csv('./circuits.csv')
constructor_results_df = pd.read_csv('./constructor_results.csv')
constructor_standings_df = pd.read_csv('./constructor_standings.csv')
constructors_df = pd.read_csv('./constructors.csv')
driver_standings_df = pd.read_csv('./driver_standings.csv')
drivers_df = pd.read_csv('./drivers.csv')
lap_times_df = pd.read_csv('./lap_times.csv')
pit_stops_df = pd.read_csv('./pit_stops.csv')
qualifying_df = pd.read_csv('./qualifying.csv')
races_df = pd.read_csv('./races.csv')
results_df = pd.read_csv('./results.csv')
seasons_df = pd.read_csv('./seasons.csv')
sprint_results_df = pd.read_csv('./sprint_results.csv')
status_df = pd.read_csv('./status.csv')

dataframes = [circuits_df, constructor_results_df, constructors_df, driver_standings_df,
              drivers_df, lap_times_df, pit_stops_df, qualifying_df, races_df,
              results_df, seasons_df, sprint_results_df, status_df]

for df in dataframes:
    df.replace('\\N', None, inplace=True)

# Define RDF namespaces
F1 = Namespace('http://example.com/f1/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

g = Graph()

# Define RDF types
g.add((F1.Circuit, RDF.type, RDFS.Class))
g.add((F1.Constructor, RDF.type, RDFS.Class))
g.add((F1.Driver, RDF.type, RDFS.Class))

# Iterate over circuits DataFrame
for index, row in circuits_df.iterrows():
    circuit_uri = URIRef(F1['circuit/' + str(row['circuitId'])])
    g.add((circuit_uri, RDF.type, F1.Circuit))
    g.add((circuit_uri, F1.circuitRef, Literal(row['circuitRef'])))
    g.add((circuit_uri, F1.name, Literal(row['name'])))
    g.add((circuit_uri, F1.location, Literal(row['location'])))
    g.add((circuit_uri, F1.country, Literal(row['country'])))
    g.add((circuit_uri, F1.latlng, Literal(f"{row['lat']},{row['lng']}", datatype=XSD.string)))
    g.add((circuit_uri, F1.alt, Literal(row['alt'], datatype=XSD.integer)))
    g.add((circuit_uri, F1.url, URIRef(row['url'])))

# Iterate over constructor_results DataFrame
for index, row in constructor_results_df.iterrows():
    constructor_results_uri = URIRef(F1['constructor_results/' + str(row['constructorResultsId'])])
    g.add((constructor_results_uri, RDF.type, F1.ConstructorResults))
    g.add((constructor_results_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((constructor_results_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((constructor_results_uri, F1.points, Literal(row['points'], datatype=XSD.float)))
    g.add((constructor_results_uri, F1.status, Literal(row['status'])))

# Iterate over constructor_standings DataFrame
for index, row in constructor_standings_df.iterrows():
    constructor_standings_uri = URIRef(F1['constructor_standings/' + str(row['constructorStandingsId'])])
    g.add((constructor_standings_uri, RDF.type, F1.ConstructorStandings))
    g.add((constructor_standings_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((constructor_standings_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((constructor_standings_uri, F1.points, Literal(row['points'], datatype=XSD.float)))
    g.add((constructor_standings_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((constructor_standings_uri, F1.positionText, Literal(row['positionText'])))
    g.add((constructor_standings_uri, F1.wins, Literal(row['wins'], datatype=XSD.integer)))

# Iterate over constructors DataFrame
for index, row in constructors_df.iterrows():
    constructor_uri = URIRef(F1['constructor/' + str(row['constructorId'])])
    g.add((constructor_uri, RDF.type, F1.Constructor))
    g.add((constructor_uri, F1.constructorRef, Literal(row['constructorRef'])))
    g.add((constructor_uri, F1.name, Literal(row['name'])))
    g.add((constructor_uri, F1.nationality, Literal(row['nationality'])))
    g.add((constructor_uri, F1.url, URIRef(row['url'])))

# Iterate over driver_standings DataFrame
for index, row in driver_standings_df.iterrows():
    driver_standings_uri = URIRef(F1['driver_standings/' + str(row['driverStandingsId'])])
    g.add((driver_standings_uri, RDF.type, F1.DriverStandings))
    g.add((driver_standings_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((driver_standings_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((driver_standings_uri, F1.points, Literal(row['points'], datatype=XSD.float)))
    g.add((driver_standings_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((driver_standings_uri, F1.positionText, Literal(row['positionText'])))
    g.add((driver_standings_uri, F1.wins, Literal(row['wins'], datatype=XSD.integer)))

# Iterate over drivers DataFrame
for index, row in drivers_df.iterrows():
    driver_uri = URIRef(F1['driver/' + str(row['driverId'])])
    g.add((driver_uri, RDF.type, F1.Driver))
    g.add((driver_uri, F1.driverRef, Literal(row['driverRef'])))
    g.add((driver_uri, F1.number, Literal(row['number'], datatype=XSD.integer)))
    g.add((driver_uri, F1.code, Literal(row['code'])))
    g.add((driver_uri, F1.forename, Literal(row['forename'])))
    g.add((driver_uri, F1.surname, Literal(row['surname'])))
    g.add((driver_uri, F1.dob, Literal(row['dob'], datatype=XSD.date)))
    g.add((driver_uri, F1.nationality, Literal(row['nationality'])))
    g.add((driver_uri, F1.url, URIRef(row['url'])))

# Iterate over lap_times DataFrame
for index, row in lap_times_df.iterrows():
    lap_times_uri = URIRef(F1['lap_times/' + str(row['lap'])])
    g.add((lap_times_uri, RDF.type, F1.LapTimes))
    g.add((lap_times_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((lap_times_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((lap_times_uri, F1.lap, Literal(row['lap'], datatype=XSD.integer)))
    g.add((lap_times_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((lap_times_uri, F1.time, Literal(row['time'], datatype=XSD.time)))
    g.add((lap_times_uri, F1.milliseconds, Literal(row['milliseconds'], datatype=XSD.integer)))
    # Add more properties as needed

# Iterate over pit_stops DataFrame
for index, row in pit_stops_df.iterrows():
    pit_stops_uri = URIRef(F1['pit_stops/' + str(row['stopId'])])
    g.add((pit_stops_uri, RDF.type, F1.PitStops))
    g.add((pit_stops_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((pit_stops_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((pit_stops_uri, F1.stop, Literal(row['stop'], datatype=XSD.integer)))
    g.add((pit_stops_uri, F1.lap, Literal(row['lap'], datatype=XSD.integer)))
    g.add((pit_stops_uri, F1.time, Literal(row['time'], datatype=XSD.duration)))
    g.add((pit_stops_uri, F1.duration, Literal(row['duration'], datatype=XSD.integer)))
    g.add((pit_stops_uri, F1.milliseconds, Literal(row['milliseconds'], datatype=XSD.integer)))

# Iterate over qualifying DataFrame
for index, row in qualifying_df.iterrows():
    qualifying_uri = URIRef(F1['qualifying/' + str(row['qualifyId'])])
    g.add((qualifying_uri, RDF.type, F1.Qualifying))
    g.add((qualifying_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((qualifying_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((qualifying_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((qualifying_uri, F1.number, Literal(row['number'], datatype=XSD.integer)))
    g.add((qualifying_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((qualifying_uri, F1.q1, Literal(row['q1'], datatype=XSD.duration)))
    g.add((qualifying_uri, F1.q2, Literal(row['q2'], datatype=XSD.duration)))
    g.add((qualifying_uri, F1.q3, Literal(row['q3'], datatype=XSD.duration)))

# Iterate over races DataFrame
for index, row in races_df.iterrows():
    races_uri = URIRef(F1['race/' + str(row['raceId'])])
    g.add((races_uri, RDF.type, F1.Race))
    g.add((races_uri, F1.year, Literal(row['year'], datatype=XSD.gYear)))
    g.add((races_uri, F1.round, Literal(row['round'], datatype=XSD.integer)))
    g.add((races_uri, F1.circuitId, URIRef(F1['circuit/' + str(row['circuitId'])])))
    g.add((races_uri, F1.name, Literal(row['name'])))
    g.add((races_uri, F1.datetime, Literal(row['datetime'], datatype=XSD.dateTime)))
    g.add((races_uri, F1.url, URIRef(row['url'])))

# Iterate over results DataFrame
for index, row in results_df.iterrows():
    results_uri = URIRef(F1['results/' + str(row['resultId'])])
    g.add((results_uri, RDF.type, F1.Results))
    g.add((results_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((results_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((results_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((results_uri, F1.number, Literal(row['number'], datatype=XSD.integer)))
    g.add((results_uri, F1.grid, Literal(row['grid'], datatype=XSD.integer)))
    g.add((results_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((results_uri, F1.positionText, Literal(row['positionText'])))
    g.add((results_uri, F1.positionOrder, Literal(row['positionOrder'], datatype=XSD.integer)))
    g.add((results_uri, F1.points, Literal(row['points'], datatype=XSD.float)))
    g.add((results_uri, F1.laps, Literal(row['laps'], datatype=XSD.integer)))
    g.add((results_uri, F1.time, Literal(row['time'], datatype=XSD.duration)))
    g.add((results_uri, F1.milliseconds, Literal(row['milliseconds'], datatype=XSD.integer)))
    g.add((results_uri, F1.fastestLap, Literal(row['fastestLap'], datatype=XSD.integer)))
    g.add((results_uri, F1.rank, Literal(row['rank'], datatype=XSD.integer)))
    g.add((results_uri, F1.fastestLapTime, Literal(row['fastestLapTime'], datatype=XSD.duration)))
    g.add((results_uri, F1.fastestLapSpeed, Literal(row['fastestLapSpeed'], datatype=XSD.float)))
    g.add((results_uri, F1.statusId, URIRef(F1['status/' + str(row['statusId'])])))

# Iterate over seasons DataFrame
for index, row in seasons_df.iterrows():
    seasons_uri = URIRef(F1['season/' + str(row['year'])])
    g.add((seasons_uri, RDF.type, F1.Season))
    g.add((seasons_uri, F1.year, Literal(row['year'], datatype=XSD.gYear)))
    g.add((seasons_uri, F1.url, URIRef(row['url'])))

# Iterate over sprint_results DataFrame
for index, row in sprint_results_df.iterrows():
    sprint_results_uri = URIRef(F1['sprint_results/' + str(row['resultId'])])
    g.add((sprint_results_uri, RDF.type, F1.SprintResults))
    g.add((sprint_results_uri, F1.raceId, URIRef(F1['race/' + str(row['raceId'])])))
    g.add((sprint_results_uri, F1.driverId, URIRef(F1['driver/' + str(row['driverId'])])))
    g.add((sprint_results_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((sprint_results_uri, F1.number, Literal(row['number'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.grid, Literal(row['grid'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.positionText, Literal(row['positionText'])))
    g.add((sprint_results_uri, F1.positionOrder, Literal(row['positionOrder'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.points, Literal(row['points'], datatype=XSD.float)))
    g.add((sprint_results_uri, F1.laps, Literal(row['laps'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.time, Literal(row['time'], datatype=XSD.duration)))
    g.add((sprint_results_uri, F1.milliseconds, Literal(row['milliseconds'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.fastestLap, Literal(row['fastestLap'], datatype=XSD.integer)))
    g.add((sprint_results_uri, F1.fastestLapTime, Literal(row['fastestLapTime'], datatype=XSD.duration)))
    g.add((sprint_results_uri, F1.statusId, URIRef(F1['status/' + str(row['statusId'])])))

# Iterate over status DataFrame
for index, row in status_df.iterrows():
    status_uri = URIRef(F1['status/' + str(row['statusId'])])
    g.add((status_uri, RDF.type, F1.Status))
    g.add((status_uri, F1.status, Literal(row['status'])))

g.serialize('all_f1_data.rdf', format='turtle')