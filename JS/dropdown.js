async function populateDriversDropdowns() {
    try {
        const response = await fetch('drivers_full_name.json');
        if (response.ok) {
            const drivers = await response.json();

            const driverSelect = document.getElementById('driverSelect');
            const driver1Select = document.getElementById('driver1Select');
            const driver2Select = document.getElementById('driver2Select');

            drivers.forEach(driver => {
                const fullName = `${driver.forename} ${driver.surname}`;
                driverSelect.options[driverSelect.options.length] = new Option(fullName, fullName);
                driver1Select.options[driver1Select.options.length] = new Option(fullName, fullName);
                driver2Select.options[driver2Select.options.length] = new Option(fullName, fullName);
            });
        } else {
            throw new Error('Failed to load driver names');
        }
    } catch (error) {
        console.error('Error loading driver names:', error);
    }
}

// Call this function when the page loads to populate the dropdowns
populateDriversDropdowns();
