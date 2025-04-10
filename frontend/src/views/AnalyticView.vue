/**
 * AnalyticView.vue - Componente Vue 3
 *
 * Este componente muestra una interfaz analítica para explorar datos microbiológicos. Incluye:
 * - Filtros por tipo de muestra (site) y condición médica (disease)
 * - Visualización de índices de diversidad (Shannon) mediante boxplot
 * - Tabla de valores por muestra
 * - Resumen estadístico por condición
 * - Gráfico de barras apiladas con abundancia relativa por género microbiano
 *
 * Se conecta a un backend vía FastAPI para obtener los datos, y utiliza Chart.js + chartjs-chart-boxplot
 * para las visualizaciones.
 */
 <template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <!-- Panel lateral -->
      <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-light sidebar-fixed">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-5 min-vh-100">
          <!-- Site -->
          <ul class="list-group">
            <li class="list-group-item custom-header d-flex justify-content-between align-items-center">Site</li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputCervix" type="radio" id="inputCervix" name="radioButton" @click="loadData('cervix')" />
              Cervix<span class="badge badge-pill bg-secondary float-end">82</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputUterus" type="radio" id="inputUterus" name="radioButton" @click="loadData('uterus')" />
              Uterus<span class="badge badge-pill bg-secondary float-end">79</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputRectum" type="radio" id="inputRectum" name="radioButton" @click="loadData('rectum')" />
              Rectum<span class="badge badge-pill bg-secondary float-end">89</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputVagina" type="radio" id="inputVagina" name="radioButton" @click="loadData('vagina')" />
              Vagina<span class="badge badge-pill bg-secondary float-end">89</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputOrine" type="radio" id="inputOrine" name="radioButton" @click="loadData('orine')" />
              Urine<span class="badge badge-pill bg-secondary float-end">86</span>
            </li>
          </ul>

          <!-- Group Selector -->
          <br />
          <ul class="list-group">
            <li class="list-group-item custom-header">
              <label for="groupSelector">Groups</label>
              <select class="form-select mt-2" id="groupSelector" v-model.number="numGrupos">
                <option value="0">-- No groups --</option>
                <option value="2">2 groups</option>
                <option value="3">3 groups</option>
                <option value="4">4 groups</option>
              </select>
            </li>
          </ul>

          <!-- Conditions -->
          <br />
          <ul class="list-group">
            <li class="list-group-item custom-header">Condition</li>
            <li class="list-group-item d-flex justify-content-between flex-wrap align-items-center" v-for="disease in diseases" :key="disease.name">
              <div class="d-flex align-items-center flex-wrap overflow-hidden">
                <input class="form-check-input me-1 disease-check" :id="'check_' + disease.name" type="checkbox" :value="disease.name" v-model="myList" />
                {{ disease.name }}
                <span class="badge badge-pill bg-secondary ms-2">{{ getCount(disease.name) }}</span>
              </div>
              <select class="form-select form-select-sm w-auto" v-model.number="disease.group" @change="updateItems">
                <option value="0">Sin grupo</option>
                <option v-for="n in numGrupos" :key="n" :value="n">Grupo {{ n }}</option>
              </select>

            </li>
          </ul>
        </div>
      </div>

      <!-- Contenido Principal -->
      <div class="col py-3">
        <!-- Header y descripción -->
        <div class="section-header text-center mb-4">
          <h3 class="fs-3">Analytics Section</h3>
          <p class="fs-6 text-muted">Here you can visualize and analyze selected data.</p>
        </div>

        <!-- Gráficos -->
        <div class="mt-4">
          
          <div class="d-flex flex-wrap justify-content-center align-items-start mt-4 gap-5">
          <div class="text-center">
            <h5>Abundancia relativa por género (por enfermedad)</h5>
            <canvas id="abundanciaChart" class="chart-canvas-large" width="800" height="600"></canvas>
          </div>
          <div class="text-center">
            <h5>Abundancia relativa por género (por grupo)</h5>
            <canvas id="abundanciaChartFiltrado" class="chart-canvas-large" width="800" height="500"></canvas>
          </div>
        </div>



        <div class="d-flex flex-wrap justify-content-center align-items-start gap-5 mt-4">
          <div class="text-center">
            <h5>Dispersión PCoA por enfermedad</h5>
            <canvas id="pcoaChart" class="chart-canvas-large" style="max-width: 1000px; max-height: 500px;"></canvas>
          </div>
          <div class="text-center">
            <h5>Dispersión PCoA por grupo</h5>
            <canvas id="pcoaChartPorGrupo" class="chart-canvas-large" style="max-width: 1000px; max-height: 500px;"></canvas>
          </div>
        </div>


        <div class="text-center">
          <h5>Violinplot del índice de Shannon por grupo</h5>
          <canvas id="shannonViolinplotChart" class="chart-canvas-large" width="700" height="400"></canvas>
        </div>

          <h5>Índice de Shannon por muestra</h5>
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th>Muestra</th>
                <th>Condition</th>
                <th>Shannon</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in filteredShannonResults" :key="row.sample_id">
                <td>{{ row.sample_id }}</td>
                <td>{{ row.diseases }}</td>
                <td>{{ row.shannon.toFixed(4) }}</td>
              </tr>
            </tbody>
          </table>

          <h5 class="mt-4">Resumen por enfermedad</h5>
          <table class="table table-sm table-bordered">
            <thead>
              <tr>
                <th>Enfermedad</th>
                <th>Media</th>
                <th>Desviación estándar</th>
                <th>Num. muestras</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in shannonSummary" :key="row.diseases">
                <td>{{ row.diseases }}</td>
                <td>{{ row.mean != null ? row.mean.toFixed(4) : '—' }}</td>
                <td>{{ row.std != null ? row.std.toFixed(4) : '—' }}</td>
                <td>{{ row.count != null ? row.count : '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<style>
.list-group {
  width: 100%;
  max-width: 900px;
}
.page-link:focus {
    box-shadow: none !important;
    border-color: transparent !important;
}
.custom-header {
  background-color: #4e73df; 
  color: white;
  font-weight: bold;
}

.chart-canvas {
  width: 100% !important;
  height: auto !important;
  max-width: 800px;
  margin-bottom: 2rem;
}

/* Sidebar siempre estrecha, incluso en pantallas medianas */
.sidebar-fixed {
  width: auto;
  max-width: 250px;
  min-width: 180px;
  flex-shrink: 0;
}


/* Asegura que el contenido principal puede crecer */
.col {
  flex: 1;
}

.chart-canvas-large {
  display: block;
  max-width: 800px;
  max-height: 1000px;
  width:700px !important;
  height: 400px !important;
  margin: 0 auto 2rem;
}



</style>

<script lang="ts" setup>

// Importaciones de librerías
import { ref, onMounted, nextTick, reactive, computed, watch} from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router';

// Chart.js y el plugin de gráficas tipo boxplot
import { Chart, registerables } from 'chart.js';
import { BoxPlotController, BoxAndWiskers , ViolinController, Violin} from '@sgratzl/chartjs-chart-boxplot';

//Regitro de todos los componentes necesarios para gráficas
Chart.register(...registerables, BoxPlotController, BoxAndWiskers, ViolinController, Violin);

// Ruta actual
const route = useRoute();

// Lista reactiva de enfermedades con su grupo inicializado a 0
const diseases = reactive([
  { name: 'RM', group: 0 },
  { name: 'MALE_FACTOR', group: 0 },
  { name: 'TUBAL_FACTOR', group: 0 },
  { name: 'ENDOMETRIOSIS', group: 0 },
  { name: 'ENDOMETRITIS', group: 0 },
  { name: 'MIOMA', group: 0 },
  { name: 'RIF', group: 0 },
  { name: 'UNEXPLAINED', group: 0 }
]);

// Variables para almacenar datos generales y filtrados
interface Item {
  [key: string]: any;
}


const items = ref<Item[]>([])
const originalItems = ref<Item[]>([])
const myList = ref<string[]>([])
const patiens = ref(0)

// Contadores por enfermedad
const numRM = ref(0)
const numMALE_FACTOR = ref(0)
const numTUBAL_FACTOR = ref(0)
const numENDOMETRIOSIS = ref(0)
const numENDOMETRITIS = ref(0)
const numMIOMA = ref(0)
const numRIF = ref(0)
const numUNEXPLAINED = ref(0)
//Numero de grupos
const numGrupos = ref(0)

const mother = ref({})

//Resultados de análisis de diversidad --> Shannon
const shannonResults = ref<any[]>([]);
const shannonSummary = ref<any[]>([]);
const abundanciaData = ref<any[]>([]);
// Beta diversity
const betaResults = ref<any[]>([]);

//Colores
const colores = [
  '#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854',
  '#ffd92f', '#e5c494', '#b3b3b3', '#1f78b4', '#33a02c',
  '#fb9a99', '#fdbf6f', '#cab2d6', '#6a3d9a', '#b15928',
  '#a65628', '#f781bf', '#999999', '#d95f02', '#7570b3',
  '#e7298a', '#66a61e', '#e6ab02', '#a6cee3', '#1b9e77',
  '#b2df8a', '#fb8072', '#80b1d3', '#fdb462', '#b3de69'
];

//Datos computados para construir boxplot por grupo
const shannonViolinData = computed(() => {
  const groups: { [key: number]: string[] } = {};
  for (let i = 1; i <= numGrupos.value; i++) {
    groups[i] = diseases.filter(d => d.group === i).map(d => d.name);
  }

  const getShannonForGroup = (group: string[]) =>
    shannonResults.value.filter(r => group.includes(r.diseases)).map(r => r.shannon).filter(val => typeof val === 'number');

  return {
    labels: Object.keys(groups).map(g => `Grupo ${g}`),
    datasets: [
      {
        label: 'Índice de Shannon',
        data: Object.values(groups).map(g => getShannonForGroup(g))
      }
    ]
  };
});


// Opciones para el gráfico
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Distribución del Índice de Shannon por Grupo'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Shannon Index'
      }
    }
  }
}

/**
 * @brief Contador reactivo asociado a una enfermedad específica
 * @param disease Nombre de la enfermedad
 * @returns Referencia a la variable reactiva que contiene el número de muestras
 */
function getCount(disease: string) {
  return eval('num' + disease);
}

/**
 * @brief Filtra los resultados del índice de Shannon según los grupos de 
 *        enfermedades seleccionados
 */
 const filteredShannonResults = computed(() => {
  if (numGrupos.value === 0) return shannonResults.value;

  const assignedConditions = diseases
    .filter(d => d.group > 0 && myList.value.includes(d.name))
    .map(d => d.name);

  return shannonResults.value.filter(item =>
    assignedConditions.includes(item.diseases)
  );
});


/**
 * @brief Cuenta cuantas muestras estan asociadas a una enfermedad específica
 * @param site Nombre de la enfermedad
 * @returns Número de pacientes con dicha enfermedad
 */
function countCases(site: string) {
  var filtrados = originalItems.value.filter(item => item.diseases === site) 
  return filtrados.length
}



/**
 * @brief Carga desde el backend los datos asociados a un sitio 
 * @param site Nombre del sitio
 */
function loadData(site: string){

  originalItems.value = []
  updateItems()
  axios
    .get(import.meta.env.VITE_API_URL + site)
    .then((response) => {

      originalItems.value = response.data
      
      myList.value = ['RM', 'MALE_FACTOR', 'TUBAL_FACTOR', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'] 
      
      //Recuento por enfermedad
      numRM.value = countCases('RM')
      numMALE_FACTOR.value = countCases('MALE_FACTOR')
      numTUBAL_FACTOR.value = countCases('TUBAL_FACTOR')
      numENDOMETRIOSIS.value = countCases('ENDOMETRIOSIS')
      numENDOMETRITIS.value = countCases('ENDOMETRITIS')
      numMIOMA.value = countCases('MIOMA')
      numRIF.value = countCases('RIF')
      numUNEXPLAINED.value = countCases('UNEXPLAINED')

      updateItems()

      //Cálculo de métricas analíticas
      getShannonDiversity(site);
      getAbundanciaData(site);
      getBetaDiversity(site);
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}

/**
 * @brief Obtiene y muestra los resultados del índice de Shannon para un sitio específica
 * @param site El sitio anatómico a analizar 
 */
async function getShannonDiversity(site: string) {
  try {
    const response = await axios.get(`http://localhost:8000/shannon?site=${site}`);
    shannonResults.value = response.data.resumen_muestra;
    shannonSummary.value = response.data.resumen_enfermedad;
    await nextTick()  // Espera a que el DOM esté actualizado

    const ctx = document.getElementById('shannonViolinplotChart') as HTMLCanvasElement
    if (ctx) {
      const oldChart = Chart.getChart(ctx);
      if (oldChart) oldChart.destroy();

      new Chart(ctx, {
        type: 'violin',
        data: shannonViolinData.value,  
        options: chartOptions        
      });
    }

  } catch (error) {
    console.error("Error al obtener índice de Shannon:", error);
  }
}

/**
 * @brief Obtiene del backend los datos de abundancia relativa por enfermedad y genera su gráfica
 * @param site El sitio del cuerpo para el cual se quiere obtener la abundancia
 */
async function getAbundanciaData(site: string) {
  try {
    const response = await axios.get(`http://localhost:8000/abundancias?site=${site}`);
    abundanciaData.value = response.data;
  } catch (error) {
    console.error("Error al obtener abundancias:", error);
  }

  await nextTick();
  drawAbundanciaChart();
  if (numGrupos.value > 0) {
    await nextTick();
    drawAbundanciaPorGrupoChartFiltrado();
  }

  /*
  if (numGrupos.value > 0) {
    drawAbundanciaGroupChart();
  }*/
}

/**
 * @brief Obtiene del backend las coordenadas PCoA calculadas a partir
 *        de la diversidad beta (distancias Bray-Curtis) para un sitio dado
 * @param site Nombre del sitio anatómico 
 */
async function getBetaDiversity(site: string) {
  try {
    const response = await axios.get(`http://localhost:8000/beta?site=${site}`);
    betaResults.value = response.data;
    await nextTick(); //Para asegurar que este listo antes de dibujar
    drawPCoAChart();
    if (numGrupos.value > 0) {
      await nextTick();
      drawPCoAChartPorGrupo();
    }

  } catch (error) {
    console.error("Error al obtener datos de diversidad beta:", error);
  }
}

/**
 * @brief Dibuja el gráfico de dispersión (scatterplot) de diversidad beta
 *        usando las dos primeras componentes principales (PCoA).
 */
 function drawPCoAChart() {
  const canvas = document.getElementById('pcoaChart') as HTMLCanvasElement;
  if (!canvas) return;

  if (Chart.getChart(canvas)) {
    Chart.getChart(canvas)?.destroy();
  }

  const pc1 = betaResults.value["PC1"];
  const pc2 = betaResults.value["PC2"];
  const samples = betaResults.value["sample_id"];
  const diseases = betaResults.value["diseases"];

  // Generar un color diferente por enfermedad
  const colorPorEnfermedad: { [key: string]: string } = {
  "RM": '#66c2a5',
  "MALE_FACTOR": '#fc8d62',
  "TUBAL_FACTOR": '#8da0cb',
  "ENDOMETRIOSIS": '#e78ac3',
  "ENDOMETRITIS": '#a6d854',
  "MIOMA": '#ffd92f',
  "RIF": '#e5c494',
  "UNEXPLAINED": '#b3b3b3',
  "SOP": '#4e73df'
};


  const grupos: { [key: string]: any[] } = {};

  // Agrupar puntos por enfermedad
  Object.keys(pc1).forEach((i) => {
  const disease = diseases[i];
  if (!myList.value.includes(disease)) return; // Filtra SOP y ARTERIOVENOUS_MALFORMATION

  if (!grupos[disease]) grupos[disease] = [];
  grupos[disease].push({
    x: pc1[i],
    y: pc2[i],
    label: samples[i]
  });
});


  // Crear un dataset por enfermedad
  const datasets = Object.keys(grupos).map((disease) => ({
  label: disease,
  data: grupos[disease],
  backgroundColor: colorPorEnfermedad[disease] || '#000000', // fallback negro
  pointRadius: 5,
  parsing: {
    xAxisKey: 'x',
    yAxisKey: 'y'
  }
  }));


  new Chart(canvas, {
    type: 'scatter',
    data: { datasets },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context: any) {
              const p = context.raw;
              return `${p.label} (${context.dataset.label})`;
            }
          }
        },
        title: {
          display: true,
          text: 'Distribución PCoA de la Diversidad Beta'
        }
      },
      scales: {
        x: { title: { display: true, text: 'PC1' } },
        y: { title: { display: true, text: 'PC2' } }
      }
    }
  });
}
//Lo mismo por grupos
function drawPCoAChartPorGrupo() {
  const canvas = document.getElementById('pcoaChartPorGrupo') as HTMLCanvasElement;
  if (!canvas || numGrupos.value === 0) return;

  if (Chart.getChart(canvas)) {
    Chart.getChart(canvas)?.destroy();
  }

  const pc1 = betaResults.value["PC1"];
  const pc2 = betaResults.value["PC2"];
  const samples = betaResults.value["sample_id"];
  const enfermedades = betaResults.value["diseases"];

  // Mapeo de enfermedad a grupo
  const enfermedadAGrupo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0) enfermedadAGrupo[d.name] = d.group;
  });

  const grupos: Record<number, any[]> = {};
  Object.keys(pc1).forEach(i => {
    const enfermedad = enfermedades[i];
    const grupo = enfermedadAGrupo[enfermedad];

    if (grupo && myList.value.includes(enfermedad)) {
      if (!grupos[grupo]) grupos[grupo] = [];
      grupos[grupo].push({
        x: pc1[i],
        y: pc2[i],
        label: samples[i]
      });
    }
  });

  const datasets = Object.keys(grupos).map((g, i) => ({
    label: `Grupo ${g}`,
    data: grupos[Number(g)],
    backgroundColor: colores[i % colores.length],
    pointRadius: 5,
    parsing: {
      xAxisKey: 'x',
      yAxisKey: 'y'
    }
  }));

  new Chart(canvas, {
    type: 'scatter',
    data: { datasets },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'PCoA de diversidad beta por grupo'
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              const p = context.raw;
              return `${p.label} (${context.dataset.label})`;
            }
          }
        }
      },
      scales: {
        x: { title: { display: true, text: 'PC1' } },
        y: { title: { display: true, text: 'PC2' } }
      }
    }
  });
}


/**
 * @brief Renderiza el gráfico de barras apiladas con la abundancia relativa de los géneros microbianos
 */
function drawAbundanciaChart() {
  const ctx = document.getElementById('abundanciaChart') as HTMLCanvasElement;
  if (!ctx) return;

  // Destruimos el gráfico anterior si existe
  const oldChart = Chart.getChart(ctx);
  if (oldChart) oldChart.destroy();

  //const enfermedades = abundanciaData.value.map(d => d.diseases);
  const enfermedades = abundanciaData.value
  .filter(d => myList.value.includes(d.diseases)) // 👈 Filtra aquí
  .map(d => d.diseases);

  const keys = Object.keys(abundanciaData.value[0]).filter(k => k.startsWith('x'));

  // Suma total por género
  const totalAbundancias: Record<string, number> = {};
  keys.forEach(k => {
    totalAbundancias[k] = abundanciaData.value.reduce((sum, row) => sum + (row[k] || 0), 0);
  });

  const totalMuestras = abundanciaData.value.length;

  // Filtramos los géneros con abundancia media global ≥ 3%
  /*
  const topKeys = keys.filter(k => (totalAbundancias[k] / totalMuestras) >= 3);
  const otherKeys = keys.filter(k => !topKeys.includes(k));
  */
  //Filtrar 30% de más abundantes
  
  const sortedKeys = keys.sort((a, b) => totalAbundancias[b] - totalAbundancias[a]);
  const topN = Math.ceil(keys.length * 0.3);
  const topKeys = sortedKeys.slice(0, topN);
  const otherKeys = sortedKeys.slice(topN);
  
  // Dataset de los top
  const datasets = topKeys.map((k, i) => ({
    label: k,
    //data: abundanciaData.value.map(d => d[k]),
    data: abundanciaData.value.filter(d => myList.value.includes(d.diseases)).map(d => d[k]),
    backgroundColor: colores[i % colores.length],
    stack: 'stack1'
  }));

  // Dataset de "otros"
  //const otros = abundanciaData.value.map(d =>otherKeys.reduce((sum, k) => sum + (d[k] || 0), 0));
  const otros = abundanciaData.value
  .filter(d => myList.value.includes(d.diseases)) // 👈 aquí también
  .map(d => otherKeys.reduce((sum, k) => sum + (d[k] || 0), 0));

  datasets.push({
    label: 'Otros',
    data: otros,
    backgroundColor: '#999999',
    stack: 'stack1'
  });

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: enfermedades,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Abundancia relativa por enfermedad (filtrada ≥3%)'
        },
        legend: {
          position: 'bottom'
        }
      },
      scales: {
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          title: {
            display: true,
            text: 'Abundancia relativa (%)'
          }
        }
      }
    }
  });
}

//
function drawAbundanciaPorGrupoChartFiltrado() {
  const canvas = document.getElementById('abundanciaChartFiltrado') as HTMLCanvasElement;
  if (!canvas || numGrupos.value === 0) return;

  // Destruimos el gráfico anterior si existe
  const oldChart = Chart.getChart(canvas);
  if (oldChart) oldChart.destroy();

  // Agrupamos enfermedades por grupo
  const groupMapping: Record<number, string[]> = {};
  for (let i = 1; i <= numGrupos.value; i++) {
    groupMapping[i] = diseases.filter(d => d.group === i).map(d => d.name);
  }

  // Agrupamos muestras por grupo
  const samplesByGroup: Record<number, any[]> = {};
  for (let i = 1; i <= numGrupos.value; i++) {
    samplesByGroup[i] = abundanciaData.value.filter(d => groupMapping[i].includes(d.diseases));
  }

  // Claves microbianas tipo 'x1', 'x2'...
  const keys = Object.keys(abundanciaData.value[0]).filter(k => k.startsWith('x'));

  // Suma total global de cada género
  const totalAbundancias: Record<string, number> = {};
  keys.forEach(k => {
    totalAbundancias[k] = 0;
    for (let i = 1; i <= numGrupos.value; i++) {
      totalAbundancias[k] += samplesByGroup[i].reduce((sum, row) => sum + (row[k] || 0), 0);
    }
  });

  // Ordenamos de mayor a menor y seleccionamos el top 30%
  
  const sortedKeys = keys.sort((a, b) => totalAbundancias[b] - totalAbundancias[a]);
  const topN = Math.ceil(keys.length * 0.3);
  const topKeys = sortedKeys.slice(0, topN);
  const otherKeys = sortedKeys.slice(topN);
  
  // Filtramos por abundancia media global ≥ 3%
  /*
  const totalMuestras = abundanciaData.value.length;
  const topKeys = keys.filter(k => (totalAbundancias[k] / totalMuestras) >= 3);
  const otherKeys = keys.filter(k => !topKeys.includes(k));
*/
  // Calculamos la media por grupo para los top
  const groupAverages: Record<string, number[]> = {};
  topKeys.forEach(k => {
    groupAverages[k] = [];
    for (let i = 1; i <= numGrupos.value; i++) {
      const grupo = samplesByGroup[i];
      const mean = grupo.reduce((sum, row) => sum + (row[k] || 0), 0) / (grupo.length || 1);
      groupAverages[k].push(mean);
    }
  });

  // Creamos datasets para top
  const datasets = topKeys.map((k, i) => ({
    label: k,
    data: groupAverages[k],
    backgroundColor: colores[i % colores.length],
    stack: 'stack1'
  }));

  // Agrupamos los "otros"
  const otros = Array(numGrupos.value).fill(0);
  for (let i = 1; i <= numGrupos.value; i++) {
    const grupo = samplesByGroup[i];
    otherKeys.forEach(k => {
      otros[i - 1] += grupo.reduce((sum, row) => sum + (row[k] || 0), 0) / (grupo.length || 1);
    });
  }

  datasets.push({
    label: 'Otros',
    data: otros,
    backgroundColor: '#999999',
    stack: 'stack1'
  });

  const labels = Array.from({ length: numGrupos.value }, (_, i) => `Grupo ${i + 1}`);

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Abundancia relativa por grupo (filtrada)'
        },
        legend: {
          position: 'bottom'
        }
      },
      scales: {
        x: { stacked: true },
        y: {
          stacked: true,
          title: {
            display: true,
            text: 'Abundancia relativa (%)'
          }
        }
      }
    }
  });
}



/**
 * @brief Maneja el cambio de grupo seleccionado desde el menú desplegable
 * @param event Evento de cambio del elemento '<select>' de grupos
 */
/*
function handleGroupSelection(event: Event) {
  const selected = parseInt((event.target as HTMLSelectElement).value);
  if (!selected) return;

  selectedGroups.value = [selected];

  // Encuentra las enfermedades asignadas a este grupo
  const assigned = diseases
    .filter(d => d.group === selected)
    .map(d => d.name);

  // Asigna esas enfermedades a myList
  myList.value = []; // limpia antes

  nextTick(() => {
    myList.value = [...assigned];
    // Recorre los checkbox del DOM
    const checkboxes = document.querySelectorAll('.disease-check');
    checkboxes.forEach((c) => {
      console.log("Checkbox ID:", c.id, " Value:", (c as HTMLInputElement).value);
    });

    updateItems();
  });
}*/

/**
 * @brief Carga los metadatos de todas las muestras desde el backend,
 *        llama a 'check()' para seleccionar el sitio en función de la ruta,
 *      y muestra una gráfica inicial si hay canvas disponible
 */
onMounted(() => {
  axios
    .get(import.meta.env.VITE_API_URL + 'all')
    .then((response) => {

      mother.value = response.data
      check()
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
    //Comprobación
    nextTick(() => {
      console.log("Violinplot data:", shannonViolinData.value);

    const canvas = document.getElementById('shannonChart') as HTMLCanvasElement;
    if (canvas) {
      new Chart(canvas, {
        type: 'violinplot',
        data: shannonViolinData.value,
        
        options: chartOptions
      });
    }
    const checks = document.querySelectorAll('.disease-check') as NodeListOf<HTMLInputElement>;
    checks.forEach(c => {
      console.log("Checkbox ID:", c.id, " Value:", c.value);
    });
  });
  
})

/**
 * @brief Observador reactivo que actualiza el gráfico boxplot cuando cambian los datos Shannon
 * @param newData Datos actualizados para el gráfico boxplot
 */
watch(shannonViolinData, async (newData) => {
  await nextTick(); // Espera a que el DOM esté actualizado
  const canvas = document.getElementById('shannonViolinplotChart') as HTMLCanvasElement;

  if (canvas) {
    // Destruir el gráfico anterior si existe
    if (Chart.getChart(canvas)) {
      Chart.getChart(canvas)?.destroy();
    }

    new Chart(canvas, {
      type: 'violin',
      data: newData,
      options: chartOptions
    });
  }
});


function updateItems() {
  items.value = originalItems.value.filter((item) => myList.value.includes(item.diseases))
  patiens.value = items.value.length


}


function check()  {
  var inputs = null;
  switch (route.params.site){
      case "cervix":
          loadData('cervix')
          inputs = document.querySelectorAll('.inputCervix');
          inputs.forEach((elem) => {
             (elem as HTMLInputElement).checked = true
          });
          break;
      case "uterus":
          loadData('uterus')
          inputs = document.querySelectorAll('.inputUterus');
          inputs.forEach((elem) => {
             (elem as HTMLInputElement).checked = true
          });
          break;
      case "rectum":
          loadData('rectum')
          inputs = document.querySelectorAll('.inputRectum');
          inputs.forEach((elem) => {
             (elem as HTMLInputElement).checked = true
          });
          break;
      case "vagina":
          loadData('vagina')
          inputs = document.querySelectorAll('.inputVagina');
          inputs.forEach((elem) => {
             (elem as HTMLInputElement).checked = true
          });
          break;
      case "orine":
          loadData('orine')
          inputs = document.querySelectorAll('.inputOrine');
          inputs.forEach((elem) => {
             (elem as HTMLInputElement).checked = true
          });
          break;
  }


}


</script>