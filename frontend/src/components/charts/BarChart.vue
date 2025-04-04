<template>
  <div class="chart-container" @mouseleave="() => labelColors = ['black','black','black','black','black']">
    <canvas ref="canvas" style="height: 300px;"></canvas>
  </div>
</template>

<script lang="ts">
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'

export default {
  name: 'BarChart',
  mounted() {
    // Registro de los controladores necesarios para que funcione el gráfico de barras
    Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip)

    const ctx = (this.$refs.canvas as HTMLCanvasElement).getContext('2d')

    new Chart(ctx!, {
      type: 'bar',
      data: {
        labels: this.chartLabels,
        datasets: [{
          label: 'Número de muestras',
          data: this.chartValues,
          backgroundColor: this.chartColors,
          hoverBackgroundColor: this.hoverColors
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            ticks: {
              color: this.labelColors
            }
          },
          x: {
            display: false
          }
        },
        onHover: (event, chartElements) => {
          if (chartElements && chartElements.length) {
            const index = chartElements[0].index
            this.handleChartColorLabel(index)
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            const routes = ['cervix', 'uterus', 'rectum', 'vagina', 'orine']
            window.location.href = "/data/" + routes[index]
          }
        }
      }
    });
  },
  data() {
    return {
      chartLabels: ['Cervix', 'Uterus', 'Rectum', 'Vagina', 'Urine'],
      chartValues: [82, 79, 89, 89, 86],
      chartColors: [
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)'
      ],
      hoverColors: [
        "rgb(255, 99, 132)",
        "rgb(255, 99, 132)",
        "rgb(255, 99, 132)",
        "rgb(255, 99, 132)",
        "rgb(255, 99, 132)"
      ],
      labelColors: ['black', 'black', 'black', 'black', 'black']
    }
  },
  methods: {
    handleChartColorLabel(index) {
      this.labelColors = this.labelColors.map((_, i) => i === index ? 'red' : 'black');
    }
  }
}
</script>

<style scoped>

.chart-container {
  width: 100%;
  height: 200px;
}
</style>

/** Script no compatible con la versión usada en analytic
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Tooltip, BarElement, CategoryScale, LinearScale)


export default {
  name: 'BarChart',
  components: { Bar },
  computed: {
    chartData() {
      return {
        labels: this.chartLabels,
        datasets: [
          {
            backgroundColor: this.chartColors,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            data: this.chartValues,
            hoverBackgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(255, 99, 132)",
              "rgb(255, 99, 132)",
              "rgb(255, 99, 132)",
              "rgb(255, 99, 132)",
            ],
          }
        ]
      }
    },
    chartOptions() {
      return {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
           y: {
             grid: {
                 display: false
             },
             ticks:{
                   color: this.labelColors
             }
           },
           x: {
                display: false
           },
        },
        onHover: (event, chartElements) => {
          if (chartElements && chartElements.length) {
            const index = chartElements[0].index
            this.handleChartColorLabel(index)
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {

             var index = elements[0].index;
              switch (index) {
              case 0:
                  window.location.href = "/data/cervix"
                  break;
              case 1:
                  window.location.href = "/data/uterus"
                  break;
              case 2:
                  window.location.href = "/data/rectum"
                  break;
              case 3:
                  window.location.href = "/data/vagina"
                  break;
              case 4:
                  window.location.href = "/data/orine"
                  break;
              }
           }
        },
      }
    }
  },
  data() {
    return {
      chartLabels: ['Cervix', 'Uterus', 'Rectum', 'Vagina', 'Urine'],
      chartValues: [82, 79, 89, 89, 86],
      chartColors: ['rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 0.2)'],
      labelColors: ['black', 'black', 'black', 'black', 'black', 'black']
    }
  },
  methods: {
    updateChartData() {
      // Generar nuevos datos aleatorios para el gráfico
      this.chartValues = Array.from({ length: 6 }, () => Math.floor(Math.random() * 100))
      // Actualizar el gráfico llamando al método update() del componente Bar
      this.$refs.chart.update()
    },
    handleChartMouseLeave() {
      console.log('El ratón ha salido del gráfico')
      this.labelColors = ['black', 'black', 'black', 'black', 'black', 'black']
    },
    handleChartColorLabel(index) {
            console.log(index)
            if( this.labelColors[index] != 'red' ) { 
                this.labelColors = ['black', 'black', 'black', 'black', 'black', 'black']
                this.labelColors[index] = 'red'
            }
    }
  }
}*/


