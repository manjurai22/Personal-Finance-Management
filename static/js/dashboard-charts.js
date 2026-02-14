
// CENTER TEXT PLUGIN (Budget)
Chart.register({
    id: 'centerText',
    afterDraw(chart, args, options) {
        if (chart.config.type !== 'doughnut') return;

        const { ctx } = chart;
        const meta = chart.getDatasetMeta(0);
        if (!meta || !meta.data || !meta.data[0]) return;

        const x = meta.data[0].x;
        const y = meta.data[0].y;

        ctx.save();
        const fontSize = Math.min(chart.width, chart.height) / 8;
        ctx.font = `bold ${fontSize}px sans-serif`;
        ctx.fillStyle = "#333";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(options.text || '', x, y);
        ctx.restore();
    }
});


// INCOME VS EXPENSE (BAR)
document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("incomeExpenseChart");
    if (!canvas) return;

    // Get data from HTML
    const labels = JSON.parse(canvas.dataset.labels || "[]");
    const incomeData = JSON.parse(canvas.dataset.income || "[]").map(Number);
    const expenseData = JSON.parse(canvas.dataset.expense || "[]").map(Number);

    // Split long labels into multiple lines
    const formattedLabels = labels.map(label => {
        if (label.length > 15) {
            return label.split(" ");   // breaks into stacked words
        }
        return label;
    });

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: formattedLabels,
            datasets: [
                {
                    label: "Income",
                    data: incomeData,
                    backgroundColor: "rgba(25, 135, 84, 0.8)",
                    borderRadius: 8,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7
                },
                {
                    label: "Expense",
                    data: expenseData,
                    backgroundColor: "rgba(220, 53, 69, 0.8)",
                    borderRadius: 8,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: "easeOutQuart"
            },
            plugins: {
                legend: {
                    position: "top",
                    labels: {
                        font: {
                            size: 13,
                            weight: "600"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ": Rs. " +
                                context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 30,
                        minRotation: 0,
                        autoSkip: false,
                        font: {
                            size: 12,
                            weight: "500"
                        }
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return "Rs. " + value.toLocaleString();
                        },
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });

});

// MONTHLY BUDGET (DOUGHNUT)

const budgetCanvas = document.getElementById("budgetGauge");

if (budgetCanvas) {

    const budget = parseFloat(budgetCanvas.dataset.budget) || 0;
    const expense = parseFloat(budgetCanvas.dataset.expense) || 0;
    const remaining = Math.max(budget - expense, 0);

    new Chart(budgetCanvas, {
        type: "doughnut",
        data: {
            labels: ["Spent", "Remaining"],
            datasets: [{
                data: [expense, remaining],
                backgroundColor: [
                    "rgba(220, 53, 69, 0.8)",
                    "rgba(25, 135, 84, 0.8)"
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "70%",
            plugins: {
                legend: { position: "bottom" },
                centerText: {
                    text: "Rs. " + budget.toLocaleString()
                }
            }
        }
    });
}

// EXPENSE BY CATEGORY (PIE)

const categoryCanvas = document.getElementById("categoryPieChart");

if (categoryCanvas) {

    const labels = JSON.parse(categoryCanvas.dataset.labels || "[]");
    const values = JSON.parse(categoryCanvas.dataset.values || "[]");

    if (labels.length > 0) {

        new Chart(categoryCanvas, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        "#0d6efd",
                        "#198754",
                        "#dc3545",
                        "#ffc107",
                        "#6f42c1",
                        "#fd7e14",
                        "#20c997",
                        "#6c757d"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }
}

// Debt Chart
const debtCanvas = document.getElementById("debtChart");

if (debtCanvas) {

    const labels = JSON.parse(debtCanvas.dataset.labels || "[]");
    const values = JSON.parse(debtCanvas.dataset.values || "[]");
    const types  = JSON.parse(debtCanvas.dataset.types || "[]");

    const colors = [];
    for (let i = 0; i < values.length; i++) {

        const type = (types[i] || "").toLowerCase();

        if (type === "borrowed") {
            values[i] = -Math.abs(values[i]); 
            colors.push("rgba(220, 53, 69, 0.7)"); 
        } 
        else if (type === "lent") {
            colors.push("rgba(25, 135, 84, 0.7)"); 
        } 
        else {
            colors.push("rgba(108, 117, 125, 0.7)"); 
        }
    }
 
    new Chart(debtCanvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Remaining (Rs.)",
                data: values,
                backgroundColor: colors,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    }
                }
            }
        }
    );
}
