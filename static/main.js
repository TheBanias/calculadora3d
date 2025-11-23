async function cargarFilamento(select) {
    const index = select.value;
    if (index === "") {
        document.getElementById("precio_bobina").value = "";
        document.getElementById("peso_bobina").value = "";
        return;
    }
    const response = await fetch("/filamento/" + index);
    if (response.ok) {
        const data = await response.json();
        document.getElementById("precio_bobina").value = data.precio;
        document.getElementById("peso_bobina").value = data.peso;
    }
}

function seleccionarJob(jobName, jobDuration) {
    document.getElementById("job_seleccionado").value = jobName;
    document.getElementById("job_duration").value = jobDuration;
    document.getElementById("calcular_form").submit();
}
