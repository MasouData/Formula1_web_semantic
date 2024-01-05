function fetchDriverData() {
    var driverNickname = document.getElementById('driverNicknameInput').value;
    var query = `
    PREFIX ns1: <http://example.com/f1/> 
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

    SELECT ?fname ?lname ?dob ?nationality ?raceName ?circuitName ?raceDate (COUNT(?raceId) AS ?numRaces)
    (SUM(?points) AS ?totalPoints) (AVG(?points) AS ?avgPoints)
    WHERE {
        ?driverId foaf:nick ?nick ;
                  foaf:givenName ?fname ;
                  foaf:familyName ?lname ;
                  foaf:birthday ?dob ;
                  ns1:nationality ?nationality .
        OPTIONAL { ?driverId foaf:homepage ?wikipediaUri }
        FILTER(REGEX(STR(?nick), "${driverNickname}", "i"))
        ?participation ns1:driverId ?driverId ;
                       ns1:raceId ?raceId ;
                       ns1:points ?points .
        ?raceId ns1:name ?raceName ;
                ns1:date ?raceDate ;
                ns1:circuitId ?circuitId .
        ?circuitId ns1:name ?circuitName .
    }
    GROUP BY ?fname ?lname ?dob ?nationality ?raceName ?circuitName ?raceDate
    `;

    console.log("Final SPARQL Query:", query);

    var url = 'http://localhost:3000/blazegraph' + "?query=" + encodeURIComponent(query) + "&format=json";

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            displayDriverInfo(response);
        } else {
            console.error('Error fetching data');
        }
    };
    xhr.send();
}

function displayDriverInfo(data) {
    var infoDiv = document.getElementById('driverInfo');
    infoDiv.innerHTML = ''; // Clear existing content

    if (data.results.bindings.length > 0) {
        // Group results by driver
        var drivers = groupByDriver(data.results.bindings);

        // Display information for each driver
        Object.keys(drivers).forEach(function(driverId) {
            var driverResults = drivers[driverId];
            var firstResult = driverResults[0];
            // Display driver's personal information
            infoDiv.innerHTML += `<h3>Full Name: ${firstResult.fname.value} ${firstResult.lname.value}</h3>`;
            infoDiv.innerHTML += `<p>Date of Birth: ${firstResult.dob.value}</p>`;
            infoDiv.innerHTML += `<p>Nationality: ${firstResult.nationality.value}</p>`;

            // Create a table for race details
            var tableHtml = '<table border="1"><tr><th>Race Name</th><th>Circuit Name</th><th>Race Date</th><th>Number of Races</th><th>Total Points</th><th>Average Points</th></tr>';
            driverResults.forEach(function(binding) {
                tableHtml += `<tr>
                                <td>${binding.raceName.value}</td>
                                <td>${binding.circuitName.value}</td>
                                <td>${binding.raceDate.value}</td>
                                <td style="text-align:center">${binding.numRaces.value}</td>
                                <td style="text-align:center">${binding.totalPoints.value}</td>
                                <td style="text-align:center">${binding.avgPoints.value}</td>
                              </tr>`;
            });
            tableHtml += '</table><hr>';
            infoDiv.innerHTML += tableHtml;
        });
    } else {
        infoDiv.innerHTML = '<p>No data found for the given driver nickname.</p>';
    }
}

// Helper function to group results by driver
function groupByDriver(bindings) {
    var drivers = {};

    bindings.forEach(function(binding) {
        // Create a unique identifier for each driver
        var driverId = binding.fname.value + "_" + binding.lname.value + "_" + binding.dob.value;

        if (!drivers[driverId]) {
            drivers[driverId] = [];
        }
        drivers[driverId].push(binding);
    });

    return drivers;
}