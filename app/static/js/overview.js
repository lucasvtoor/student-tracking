const labels = [
  "class 1",
  "class 2",
  "class 3",
  "class 4",
  "class 5",
  "class 6",
];

const data = {
  labels: labels,
  datasets: [
    {
      label: "Questions",
      backgroundColor: "#3190ED",
      borderColor: "#3190ED",
      data: [60, 40, 30, 20, 10, 5],
    },
  ],
};

const config = {
  type: "bar",
  data: data,
  options: {
    indexAxis: "y",
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
};

const myChart = new Chart(document.getElementById("myChart"), config);
