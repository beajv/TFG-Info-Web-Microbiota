<template>
    <div class="chart-container" @mouseleave="handleChartMouseLeave">
      <Bar :data="chartData" :options="chartOptions" ref="chart" />
    </div>
</template>

<script>
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
}
</script>

