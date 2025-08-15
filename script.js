// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Dropdown validation
    const form = document.querySelector("form");
    const team1Dropdown = document.getElementById("team1");
    const team2Dropdown = document.getElementById("team2");
    const timeLeftInput = document.getElementById("time_left");
    const raidSuccessInputs = document.querySelectorAll("[id^=raid_success]");
    const tackleSuccessInputs = document.querySelectorAll("[id^=tackle_success]");
    const errorMessage = document.createElement("p");

    errorMessage.style.color = "red";
    errorMessage.style.display = "none";
    form.appendChild(errorMessage);

    // Team dropdown validation
    form.addEventListener("submit", function (event) {
        if (team1Dropdown.value === team2Dropdown.value) {
            event.preventDefault();
            errorMessage.textContent = "Team 1 and Team 2 cannot be the same.";
            errorMessage.style.display = "block";
        } else {
            errorMessage.style.display = "none";
        }
    });

    // Real-time validation for time left
    timeLeftInput.addEventListener("input", function () {
        const time = parseInt(timeLeftInput.value);
        if (time < 0 || time > 40) {
            timeLeftInput.setCustomValidity("Time Left should be between 0 and 40 minutes.");
        } else {
            timeLeftInput.setCustomValidity("");
        }
    });

    // Real-time validation for success rates
    const validatePercentage = (input) => {
        input.addEventListener("input", function () {
            const value = parseFloat(input.value);
            if (value < 0 || value > 1) {
                input.setCustomValidity("Success rates must be between 0.0 and 1.0.");
            } else {
                input.setCustomValidity("");
            }
        });
    };

    raidSuccessInputs.forEach(validatePercentage);
    tackleSuccessInputs.forEach(validatePercentage);

    // Set the default values for dropdowns
    const teams = [
        "Bengaluru Bulls", "Telugu Titans", "U Mumba", "U.P. Yoddhas",
        "Dabang Delhi K.C.", "Patna Pirates", "Puneri Paltan",
        "Jaipur Pink Panthers", "Tamil Thalaivas", "Bengal Warriors",
        "Gujarat Giants", "Haryana Steelers"
    ];

    // Populate the dropdown menus
    const populateDropdown = (dropdown) => {
        teams.forEach(team => {
            const option = document.createElement("option");
            option.value = team;
            option.textContent = team;
            dropdown.appendChild(option);
        });
    };

    populateDropdown(team1Dropdown);
    populateDropdown(team2Dropdown);
});
