const labels = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"];

const data = {
  labels: labels,
  datasets: [
    {
      label: "Badges",
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
