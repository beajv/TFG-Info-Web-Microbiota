<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { Chart, registerables } from "chart.js";
  
  Chart.register(...registerables);
  
  const chartCanvas = ref(null);
  
  onMounted(() => {
    if (chartCanvas.value) {
      new Chart(chartCanvas.value, {
        type: "bar", // Tipos:  "line", "pie", etc.
        data: {
          labels: ["A", "B", "C", "D", "E"], // Nombres nombres de las categorías
          datasets: [
            {
              label: "Ejemplo de datos",
              data: [10, 20, 15, 30, 25], // Sustituiremos esto por datos reales
              backgroundColor: "rgba(75, 192, 192, 0.6)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  });
  </script>
  
  <style scoped>
  div {
    width: 600px;
    height: 400px;
  }
  </style>
  