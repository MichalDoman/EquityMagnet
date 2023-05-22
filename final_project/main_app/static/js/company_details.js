const tab_buttons = document.querySelectorAll(".tab-btn");
const details = document.querySelectorAll(".details");
const section = document.querySelector(".section-center")

section.addEventListener("click", function (event) {
    const tab_id = event.target.dataset.id;
    if (tab_id) {
        tab_buttons.forEach(function (button) {
            button.classList.remove("active");
            event.target.classList.add("active");
        });
        details.forEach(function (detail) {
            detail.classList.remove("active");
        });
        const tab = document.getElementById(tab_id);
        tab.classList.add("active");
    }
});

const context = document.querySelector("#price-chart-canvas").getContext("2d");
const chartData = JSON.parse(document.querySelector("#price-chart").getAttribute("data-chart-data"));
const chartLabels = JSON.parse(document.querySelector("#price-chart").getAttribute("data-chart-labels"));

document.addEventListener("DOMContentLoaded", function () {
    const priceChart = new Chart(context, {
        type: "line",
        data: {
            labels: chartLabels,
            datasets: [{
                data: chartData,
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 4,
                tension: 0.1,
            }]
        },
        options: {
            maintainAspectRatio: false,
            elements: {
                point: {
                    radius: 0
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            },
        }
    });
    const chartBody = document.querySelector(".chart-body")
    const labelsNumber = priceChart.data.labels.length
    chartBody.style.width = `${labelsNumber * 5}px`;
});

