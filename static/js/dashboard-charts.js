// ===============================
// CENTER TEXT PLUGIN (Budget)
// ===============================
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
        ctx.font = "bold 18px sans-serif";
        ctx.fillStyle = "#333";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(options.text || '', x, y);
        ctx.restore();
    }
});


// ===============================
// 1️⃣ INCOME VS EXPENSE (BAR)
// ===============================
const canvas = document.getElementById("incomeExpenseChart");

if (canvas) {
    const incomeLabels = JSON.parse(canvas.dataset.incomeLabels || "[]");
    const incomeValues = JSON.parse(canvas.dataset.incomeValues || "[]").map(v => Number(v) || 0);

    const expenseLabels = JSON.parse(canvas.dataset.expenseLabels || "[]");
    const expenseValues = JSON.parse(canvas.dataset.expenseValues || "[]").map(v => Number(v) || 0);

    const allLabels = Array.from(new Set([...incomeLabels, ...expenseLabels]));

    const incomeData = allLabels.map(label => {
        const idx = incomeLabels.indexOf(label);
        return idx !== -1 ? incomeValues[idx] : 0;
    });

    const expenseData = allLabels.map(label => {
        const idx = expenseLabels.indexOf(label);
        return idx !== -1 ? expenseValues[idx] : 0;
    });

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: allLabels,
            datasets: [
                {
                    label: "Income",
                    data: incomeData,
                    backgroundColor: "rgba(25, 135, 84, 0.7)",
                    borderRadius: 6
                },
                {
                    label: "Expense",
                    data: expenseData,
                    backgroundColor: "rgba(220, 53, 69, 0.7)",
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: true } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return "Rs. " + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}


// ===============================
// 2️⃣ MONTHLY BUDGET (DOUGHNUT)
// ===============================

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


// ===============================
// 3️⃣ EXPENSE BY CATEGORY (PIE)
// ===============================

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


const debtCanvas = document.getElementById("debtChart");

if (debtCanvas) {

    const labels = JSON.parse(debtCanvas.dataset.labels || "[]");
    const values = JSON.parse(debtCanvas.dataset.values || "[]");

    new Chart(debtCanvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Remaining (Rs.)",
                data: values,
                backgroundColor: "rgba(220, 53, 69, 0.7)",
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
                    beginAtZero: true,
                    min: 0,
                    max: Math.max(...values) * 1.2, // adds 20% space on top
                    ticks: {
                        stepSize: Math.ceil(Math.max(...values) / 5)
                    }
                }
            }
        }
    });
}
