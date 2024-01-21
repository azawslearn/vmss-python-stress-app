window.onload = function () {
    document.getElementById('start-stress').addEventListener('click', startStress);
    document.getElementById('reboot-instance').addEventListener('click', rebootInstance);

    function updateCpuUtilization() {
        fetch('/cpu_utilization')
            .then(response => response.json())
            .then(data => {
                document.getElementById('cpu-value').textContent = data.utilization;
            });
        setTimeout(updateCpuUtilization, 1000); // Update every second
    }

    function startStress() {
        fetch('/start_stress', { method: 'GET' })
            .then(response => response.json())
            .then(data => console.log(data.status));
    }

    function rebootInstance() {
        fetch('/reboot_instance', { method: 'GET' })
            .then(response => response.json())
            .then(data => console.log(data.status));
    }

    updateCpuUtilization(); // Start updating CPU utilization
};
