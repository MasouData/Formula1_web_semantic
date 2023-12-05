import pandas as pd

drivers_df = pd.read_csv('drivers.csv')
drivers_df.head()

qualifying_df = pd.read_csv('qualifying.csv')
qualifying_df.head()

# Replace '\N' with None
drivers_df.replace('\\N', None, inplace=True)

qualifying_df.replace({'q1': '\\N', 'q2': '\\N', 'q3': '\\N'}, {'q1': 'rdf:nil', 'q2': 'rdf:nil', 'q3': 'rdf:nil'}, inplace=True)
qualifying_df.replace('\\N', None, inplace=True)

from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from rdflib.namespace import OWL, RDFS

g = Graph()

F1 = Namespace('http://example.com/f1/')

# Define the Driver class
g.add((F1.Driver, RDF.type, OWL.Class))
g.add((F1.Driver, RDFS.label, Literal("Driver")))

# Specify Property Characteristics for driverId
g.add((F1.driverId, RDF.type, OWL.DatatypeProperty))
g.add((F1.driverId, RDFS.label, Literal("Driver ID")))
g.add((F1.driverId, RDFS.domain, F1.Qualifying))
g.add((F1.driverId, RDFS.range, XSD.integer))

# Specify Property Characteristics for driver
g.add((F1.driver, RDF.type, OWL.ObjectProperty))
g.add((F1.driver, RDFS.label, Literal("Driver")))
g.add((F1.driver, RDFS.domain, F1.Qualifying))
g.add((F1.driver, RDFS.range, F1.Driver))

# Specify Property Characteristics
g.add((F1.driverRef, RDF.type, OWL.DatatypeProperty))
g.add((F1.driverRef, RDFS.label, Literal("Driver Reference")))
g.add((F1.driverRef, RDFS.domain, F1.Driver))
g.add((F1.driverRef, RDFS.range, XSD.string))

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
    g.add((driver_uri, F1.url, Literal(row['url'], datatype=XSD.anyURI)))

g.add((F1.Qualifying, RDF.type, OWL.Class))
g.add((F1.Qualifying, RDFS.label, Literal("Qualifying")))


for index, row in qualifying_df.iterrows():
    qualifying_uri = URIRef(F1['qualifying/' + str(row['qualifyId'])])
    g.add((qualifying_uri, RDF.type, F1.Qualifying))
    g.add((qualifying_uri, F1.raceId, Literal(row['raceId'], datatype=XSD.integer)))
    g.add((qualifying_uri, F1.driverId, Literal(row['driverId'], datatype=XSD.integer)))
    g.add((qualifying_uri, F1.constructorId, URIRef(F1['constructor/' + str(row['constructorId'])])))
    g.add((qualifying_uri, F1.number, Literal(row['number'])))
    g.add((qualifying_uri, F1.position, Literal(row['position'], datatype=XSD.integer)))
    g.add((qualifying_uri, F1.qualifyingTime1, Literal(row['q1'], datatype=XSD.duration)))
    g.add((qualifying_uri, F1.qualifyingTime2, Literal(row['q2'], datatype=XSD.duration)))
    g.add((qualifying_uri, F1.qualifyingTime3, Literal(row['q3'], datatype=XSD.duration)))
    # we can convert '01:26.6' to XSD.duration or XSD.dateTime
    driver_uri = URIRef(F1['driver/' + str(row['driverId'])])
    g.add((qualifying_uri, F1.driver, driver_uri))

# # savw as RDF Data
# g.serialize('f1_data.rdf', format='turtle')
g.serialize('f1_data.rdf', format='turtle')

from rdflib import Graph, Literal, XSD, Namespace

# # Load the RDF data into a graph
g = Graph()
g.parse('f1_data.rdf', format='turtle')

# # Define the namespace
F1 = Namespace('http://example.com/f1/')

# Write the SPARQL query
query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?driver ?nationality ?surname ?forename ?constructorId ?q1
WHERE {
    ?qualifying a F1:Qualifying ;
                 F1:driver ?driver ;
                 F1:constructorId ?constructor ;
                 F1:qualifyingTime1 ?q1 .
    ?driver a F1:Driver ;
            F1:nationality ?nationality ;
            F1:surname ?surname ;
            F1:forename ?forename .
    ?constructor F1:constructorId ?constructorId .
    FILTER (xsd:duration(?q1) < "PT1M27S"^^xsd:duration)
}
"""

# Run the SPARQL query
qres = g.query(query, initNs={'F1': F1})

# Print the results
for row in qres:
    print(f"Driver: {row.driver}, Nationality: {row.nationality}, Surname: {row.surname}, Forename: {row.forename}, ConstructorId: {row.constructorId}, Q1 Time: {row.q1}")
