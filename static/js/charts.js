document.addEventListener("DOMContentLoaded", function () {

    const chartEl = document.getElementById("incomeExpenseChart");
    if (!chartEl) return;

    const income = parseFloat(chartEl.dataset.income);
    const expense = parseFloat(chartEl.dataset.expense);

    new Chart(chartEl, {
        type: "bar",
        data: {
            labels: ["Income", "Expense"],
            datasets: [{
                label: "Amount",
                data: [income, expense],
                backgroundColor: ["#4CAF50", "#F44336"],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

});

document.addEventListener("DOMContentLoaded", function () {

    const barEl = document.getElementById("monthlyExpenseChart");
    if (!barEl) return;

    const labels = JSON.parse(barEl.dataset.labels);
    const values = JSON.parse(barEl.dataset.values);

    new Chart(barEl, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Monthly Expense",
                data: values,
                backgroundColor: "#6C63FF",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

});
