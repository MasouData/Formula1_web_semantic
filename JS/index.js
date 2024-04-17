document.getElementById('driverInfoBtn').addEventListener('click', function() {
    showDriverInfoSection();
});

document.getElementById('driverCompareBtn').addEventListener('click', function() {
    showDriverCompareSection();
});

function showDriverInfoSection() {

    document.getElementById('driverInfo').innerHTML = '';
    document.getElementById('comparisonResult').innerHTML = '';

    document.getElementById('driverInfoSection').style.display = 'block';
    document.getElementById('driverCompareSection').style.display = 'none';
    document.getElementById('backBtn').style.display = 'block';
    // Additional logic to populate dropdowns
}

function showDriverCompareSection() {

    document.getElementById('driverInfo').innerHTML = '';
    document.getElementById('comparisonResult').innerHTML = '';

    document.getElementById('driverInfoSection').style.display = 'none';
    document.getElementById('driverCompareSection').style.display = 'block';
    document.getElementById('backBtn').style.display = 'block';
    // Additional logic to populate dropdowns
}

function backToMainMenu() {
    document.getElementById('driverInfoSection').style.display = 'none';
    document.getElementById('driverCompareSection').style.display = 'none';
    document.getElementById('backBtn').style.display = 'none';

    document.getElementById('driverInfo').innerHTML = '';
    document.getElementById('comparisonResult').innerHTML = '';
}

// ################################## Main ##########################

// var currentChart = null;
window.totalPointsChart = null;
window.avgPointsChart = null;

var prefixes = `
    PREFIX ns1: <http://example.com/f1/> 
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
`;

async function fetchDriverData() {
    var selectedDriver = document.getElementById('driverSelect').value;
    var [forename, surname] = selectedDriver.split(' ');

    var query = `
    ${prefixes}
    SELECT DISTINCT ?dob ?nationality ?raceName ?circuitName ?raceDate (SUM(?points) AS ?totalPoints) ?position ?time ?constructorName
    WHERE {
        ?driverId foaf:givenName "${forename}" ;
                  foaf:familyName "${surname}" ;
                  foaf:birthday ?dob ;
                  ns1:nationality ?nationality .
        ?participation ns1:driverId ?driverId ;
                       ns1:raceId ?raceId ;
                       ns1:points ?points .
        OPTIONAL { ?participation ns1:position ?position . }
        OPTIONAL { ?participation ns1:time ?time . }
        ?raceId ns1:name ?raceName ;
                ns1:date ?raceDate ;
                ns1:circuitId ?circuitId .
        ?circuitId ns1:name ?circuitName .
        OPTIONAL { ?constructorId ns1:name ?constructorName . }
    }
    GROUP BY ?fname ?lname ?dob ?nationality ?raceName ?circuitName ?raceDate ?position ?time ?constructorName
    ORDER BY DESC(?raceDate)
    LIMIT 30`;

    var url = 'http://localhost:3000/blazegraph' + "?query=" + encodeURIComponent(query) + "&format=json";
    var infoDiv = document.getElementById('driverInfo');
    infoDiv.innerHTML = '<p>Loading data, please wait...</p>';

    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            displayDriverInfo(data, selectedDriver);
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        infoDiv.innerHTML = `<p>Error loading data: ${error.message}</p>`;
    }
}

function displayDriverInfo(data, selectedDriver) {
    var infoDiv = document.getElementById('driverInfo');
    infoDiv.innerHTML = '';

    if (data.results.bindings.length > 0) {
        var drivers = groupByDriver(data.results.bindings);
        Object.keys(drivers).forEach(function(driverId) {
            var driverResults = drivers[driverId];
            var firstResult = driverResults[0];

            var fullName = selectedDriver;
            // var fullName = (firstResult.fname?.value || 'Unknown') + ' ' + (firstResult.lname?.value || 'Unknown');
            var dob = firstResult.dob?.value || 'Unknown';
            var nationality = firstResult.nationality?.value || 'Unknown';

            
            infoDiv.innerHTML += `<h3>Full Name: ${fullName}</h3>`;
            infoDiv.innerHTML += `<p>Date of Birth: ${dob}</p>`;
            infoDiv.innerHTML += `<p>Nationality: ${nationality}</p>`;

            var tableHtml = '<table border="1"><tr><th>Race Name</th><th>Circuit Name</th><th>Race Date</th><th>Total Points</th><th>Position</th><th>Time</th><th>Constructor Name</th></tr>';
            driverResults.forEach(function(binding) {
                var raceName = binding.raceName?.value || 'Unknown';
                var circuitName = binding.circuitName?.value || 'Unknown';
                var raceDate = binding.raceDate?.value || 'Unknown';
                var totalPoints = binding.totalPoints?.value || '0';
                var position = binding.position?.value || 'Unknown';
                // var time = binding.time?.value || 'Unknown';
                var time = binding.time ? binding.time.value : 'Unknown';
                var constructorName = binding.constructorName?.value || 'Unknown';

                tableHtml += `<tr>
                                <td>${raceName}</td>
                                <td>${circuitName}</td>
                                <td>${raceDate}</td>
                                <td style="text-align:center">${totalPoints}</td>
                                <td style="text-align:center">${position}</td>
                                <td style="text-align:center">${time}</td>
                                <td style="text-align:center">${constructorName}</td>
                              </tr>`;
            });
            tableHtml += '</table><hr>';
            infoDiv.innerHTML += tableHtml;
        });
    } else {
        infoDiv.innerHTML = '<p>No data found for the selected driver.</p>';
    }
}

function groupByDriver(bindings) {
    var drivers = {};
    bindings.forEach(function(binding) {
        var driverId = (binding.fname?.value || 'Unknown') + "_" + (binding.lname?.value || 'Unknown') + "_" + (binding.dob?.value || 'Unknown');
        if (!drivers[driverId]) {
            drivers[driverId] = [];
        }
        drivers[driverId].push(binding);
    });
    return drivers;
}


async function compareDrivers() {
    var driver1FullName = document.getElementById('driver1Select').value;
    var driver2FullName = document.getElementById('driver2Select').value;
    var [forename1, surname1] = driver1FullName.split(' ');
    var [forename2, surname2] = driver2FullName.split(' ');

    var query = `
    ${prefixes}
    SELECT ?driverFullName (COUNT(DISTINCT ?raceId) AS ?numRaces) (SUM(?points) AS ?totalPoints) (AVG(?points) AS ?avgPoints) (MIN(?position) AS ?bestPosition) (COUNT(?win) AS ?numWins)
    WHERE {
        {
            SELECT ?driverId (CONCAT(?fname, " ", ?lname) AS ?driverFullName) ?fname ?lname 
            WHERE {
                ?driverId foaf:givenName ?fname ;
                          foaf:familyName ?lname .
                FILTER((?fname="${forename1}" && ?lname="${surname1}") || (?fname="${forename2}" && ?lname="${surname2}"))
            }
        }
        ?participation ns1:driverId ?driverId ;
                       ns1:raceId ?raceId ;
                       ns1:points ?points .
        OPTIONAL {
                    ?participation ns1:position ?position .
                    FILTER(?position = 1)
                    BIND(1 AS ?win)
                    }
                        
    }
    GROUP BY ?driverFullName
    `;

    var url = 'http://localhost:3000/blazegraph' + "?query=" + encodeURIComponent(query) + "&format=json";
    var comparisonDiv = document.getElementById('comparisonResult');
    comparisonDiv.innerHTML = '<p>Loading comparison data...</p>';

    try {
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            displayComparisonChart(data);
        } else {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        comparisonDiv.innerHTML = '<p>Error loading comparison data.</p>';
    }
}
function displayComparisonChart(data) {
    var labels = [], totalPoints = [], avgPoints = [];
    var tableHtml = '<table border="1"><tr><th>Driver</th><th>Number of Races</th><th>Total Points</th><th>Average Points</th><th>Best Position</th><th>Number of Wins</th></tr>';

    data.results.bindings.forEach(function(binding) {
        labels.push(binding.driverFullName.value);
        totalPoints.push(binding.totalPoints.value);
        avgPoints.push(parseFloat(binding.avgPoints.value).toFixed(2));

        // Handle missing properties
        var bestPosition = binding.bestPosition ? binding.bestPosition.value : 'N/A';
        var numWins = binding.numWins ? binding.numWins.value : '0';

        tableHtml += `<tr>
                        <td>${binding.driverFullName.value}</td>
                        <td>${binding.numRaces.value}</td>
                        <td>${binding.totalPoints.value}</td>
                        <td>${parseFloat(binding.avgPoints.value).toFixed(2)}</td>
                        <td>${bestPosition}</td>
                        <td>${numWins}</td>
                      </tr>`;
    });

    tableHtml += '</table>';

    // Display the table
    var comparisonResultDiv = document.getElementById('comparisonResult');
    comparisonResultDiv.innerHTML = tableHtml;

    // Check if a chart already exists and destroy it
    if (window.totalPointsChart) {
        window.totalPointsChart.destroy();
        window.totalPointsChart = null;
    }
    if (window.avgPointsChart) {
        window.avgPointsChart.destroy();
        window.avgPointsChart = null;
    }
    // if (window.totalPointsChart) window.totalPointsChart.destroy();
    // if (window.avgPointsChart) window.avgPointsChart.destroy();

    // Create Total Points Chart
    var ctxTotalPoints = document.getElementById('totalPointsChart').getContext('2d');
    window.totalPointsChart = new Chart(ctxTotalPoints, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Points',
                data: totalPoints,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Create Average Points Chart
    var ctxAvgPoints = document.getElementById('avgPointsChart').getContext('2d');
    window.avgPointsChart = new Chart(ctxAvgPoints, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Points',
                data: avgPoints,
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}