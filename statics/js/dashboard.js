// script.js

document.addEventListener('DOMContentLoaded', function() {
    const settingsButton = document.querySelector('.settings-button');
    const settingsDropdown = document.querySelector('.settings-dropdown');

    if (!settingsButton || !settingsDropdown) {
        alert('Elements not found');
        return;
    }

    settingsButton.addEventListener('click', function() {
        settingsDropdown.classList.toggle('show');
    });

    window.addEventListener('click', function(e) {
        if (!settingsButton.contains(e.target) && !settingsDropdown.contains(e.target)) {
            settingsDropdown.classList.remove('show');
        }
    });
});