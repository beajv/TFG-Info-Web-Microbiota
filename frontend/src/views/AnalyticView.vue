/**
 * AnalyticView.vue - Componente Vue 3
 *
 * Este componente muestra una interfaz analítica para explorar datos microbiológicos. Incluye:
 * - Filtros por tipo de muestra (site) y condición médica (disease)
 * - Visualización de índices de diversidad (Shannon) mediante violinplot
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
          <!--Botón reset-->
          <button class="btn btn-outline-danger mb-3" @click="resetSelections" aria-label="Reset button">
            Reset
          </button>
          <!-- Site -->
          <ul class="list-group">
            <li class="list-group-item custom-header d-flex justify-content-between align-items-center">Site</li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputCervix" type="radio" id="inputCervix" name="radioButton" @click="loadData('cervix')" />
              Cervix<span class="badge badge-pill bg-secondary float-end">{{ siteCounts.cervix }}</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputUterus" type="radio" id="inputUterus" name="radioButton" @click="loadData('uterus')" />
              Uterus<span class="badge badge-pill bg-secondary float-end">{{ siteCounts.uterus }}</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputRectum" type="radio" id="inputRectum" name="radioButton" @click="loadData('rectum')" />
              Rectum<span class="badge badge-pill bg-secondary float-end">{{ siteCounts.rectum }}</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputVagina" type="radio" id="inputVagina" name="radioButton" @click="loadData('vagina')" />
              Vagina<span class="badge badge-pill bg-secondary float-end">{{ siteCounts.vagina }}</span>
            </li>
            <li class="list-group-item align-items-center">
              <input class="form-check-input me-1 inputOrine" type="radio" id="inputOrine" name="radioButton" @click="loadData('orine')" />
              Urine<span class="badge badge-pill bg-secondary float-end">{{ siteCounts.orine }}</span>
            </li>
          </ul>

          <!-- Group Selector -->
          <br />
          <ul class="list-group">
            <li class="list-group-item custom-header">
              <label for="groupSelector">Groups</label>
              <select class="form-select mt-2" id="groupSelector" v-model.number="numGrupos" aria-label="Group Selector">
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
                <input
                  class="form-check-input me-1 disease-check"
                  :id="'check_' + disease.name"
                  type="checkbox"
                  :value="disease.name"
                  v-model="myList"
                />
                <!--Etiqueta para la accesibilidad-->
                <label
                  class="ms-1"
                  :for="'check_' + disease.name"
                >
                  {{ disease.name }}
                </label>
                <span class="badge badge-pill bg-secondary ms-2">{{ getCount(disease.name) }}</span>
              </div>
              <select class="form-select form-select-sm w-auto" v-model.number="disease.group" @change="updateItems">
                <option value="0">No group </option>
                <option v-for="n in numGrupos" :key="n" :value="n">Group {{ n }}</option>
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
          
          <div class="row gx-4 gy-4 justify-content-center">
          <div class="col-md-6 text-center">
            <h5>Relative abundance by condition</h5>
            <canvas id="abundanciaChart" class="chart-canvas-large" role="img" aria-label="Relative abundance by condition" width="800" height="400" style="width: 800px; height: 400px;"></canvas>
          </div>
          <div class="col-md-6 text-center">
            <h5>Relative abundance by group</h5>
            <canvas id="abundanciaChartFiltrado" class="chart-canvas-large" role="img" aria-label="Relative abundance by group" width="800" height="400" style="width: 800px; height: 400px;"></canvas>
          </div>
        </div>

        <!-- Contador dinámico de pacientes por grupo -->
        <div class="text-center mb-4" v-if="numGrupos > 0">
          <div class="d-inline-block text-start border rounded p-3 shadow-sm bg-light">
            <div v-for="(cantidad, grupo) in conteoGrupos" :key="grupo">
              <strong>Group {{ grupo }}:</strong> {{ cantidad }} patients
            </div>
          </div>
        </div>

        <div class="row gx-4 gy-4 justify-content-center">
          <div class="col-md-6 text-center">
            <h5>
              PCoA scatterplot by condition
            </h5>
            <canvas id="pcoaChart" class="chart-canvas-large" role="img" aria-label="PCoA scatterplot by condition" style="max-width: 1000px; max-height: 500px;"></canvas>
          </div>
          <div class="col-md-6 text-center">
            <h5>PCoA scatterplot by group</h5>
            <div class="text-center mb-2">
              <small 
                v-if="betaResults && betaResults.p_value !== null"
                :class="{ 'fade-in': true, 'text-success': betaResults.p_value < 0.05 }"
              >
                PERMANOVA p-value:
                <strong>
                  {{ betaResults.p_value.toExponential(2) }}
                  <span v-if="betaResults.p_value < 0.05" title="Significativo"> ➡️Es significativo </span>
                </strong>
              </small>
            </div>
            <canvas id="pcoaChartPorGrupo" class="chart-canvas-large" role="img" aria-label="PCoA scatterplot by group" style="max-width: 1000px; max-height: 500px;"></canvas>
          </div>
        </div>

        <div class="row gx-4 gy-4 justify-content-center">
          <div class="col-md-6 text-center">
            <h5>Shannon diversity index by group (violin plot)</h5>
            <div class="text-center mb-2">
              <small 
                v-if="shannonPValue !== null"
                :class="{ 'fade-in': true, 'text-success': shannonPValue < 0.05 }"
              >
                Shannon α-diversity p-value:
                <strong>
                  {{ shannonPValue.toExponential(2) }}
                  <span v-if="shannonPValue < 0.05" title="Significativo"> ➡️ Es significativo </span>
                </strong>
                <span v-if="shannonTest"> ({{ shannonTest }})</span>
              </small>
            </div>

            <canvas id="shannonViolinplotChart" role="img" aria-label="Shannon diversity index (violin plot) by group" width="300" height="200"></canvas>
          </div>
          <div class="col-md-6 text-center">
            <h5>Richness index by group (violin plot)</h5>
              <div class="text-center mb-2">
                <small 
                  v-if="richnessPValue !== null"
                  :class="{ 'fade-in': true, 'text-success': richnessPValue < 0.05 }"
                >
                  Richness α-diversity p-value:
                  <strong>
                    {{ richnessPValue.toExponential(2) }}
                    <span v-if="richnessPValue < 0.05" title="Significativo"> ➡️ Es significativo </span>
                  </strong>
                  <span v-if="richnessTest"> ({{ richnessTest }})</span>
                </small>
              </div>
            <canvas id="richnessChart" role="img" aria-label="Richness index by group" width="300" height="200"></canvas>
          </div>
        </div>

        <h5 class="mt-4">
          Differentially abundant biomarkers between groups
          <span v-if="nombreTest">
            (<span v-if="nombreTest === 'mannwhitney'">Mann–Whitney U</span>
            <span v-else-if="nombreTest === 'kruskalwallis'">Kruskal–Wallis</span>
            test)
          </span>
        </h5>

          <table class="table table-sm table-bordered w-auto text-center align-middle">
            <thead class="table-warning">
              <tr>
                <th>Microorganism</th>
                <th v-for="g in numGrupos" :key="'grupo'+g">
                  Group {{ g }}<br>(% samples, mean ± std)
                </th>
                <th>p-value<br><span v-if="nombreTest">(test: {{ nombreTest }})</span></th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="row in biomarcadores"
                :key="row.micro"
                :class="{ 'fila-significativa': esSignificativo(row.p_value) }"
              >
                <td>{{ row.nombre_limpio || row.micro }}</td>

                <!-- Columnas dinámicas por grupo -->
                <td v-for="g in numGrupos" :key="'valor'+g">
                  <div v-if="row['n_g' + g] != null">
                    {{ row['n_g' + g] }} / {{ row['total_g' + g] }} samples,<br>
                    {{
                      row['total_g' + g] > 0
                        ? ((row['n_g' + g] / row['total_g' + g]) * 100).toFixed(2) + ' %'
                        : '—'
                    }}<br>
                    {{
                      row['mean_g' + g] != null
                        ? row['mean_g' + g].toFixed(2)
                        : '—'
                    }} ± {{
                      row['std_g' + g] != null
                        ? row['std_g' + g].toFixed(2)
                        : '—'
                    }}
                  </div>
                  <div v-else>—</div>
                </td>
                  <td>
                    {{ row.p_value != null ? Number(row.p_value).toExponential(2) : '—' }}
                  </td>
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
 /* max-width: 800px;
  max-height: 1000px;*/
  width:100% !important;
  height: auto !important;
  margin: 0 auto 2rem;
}

/* Resalta la fila con pvalor significativo*/ 
table tr.fila-significativa td {
  background-color: #eefbea !important; /* Verde clarito */
}
.fade-in {
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
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
//Gráfico de riqueza
const richnessPorGrupo = ref<any[]>([]);

// Beta diversity
//const betaResults = ref<any[]>([]);
const betaResults = ref<{ pcoa: any[]; p_value: number | null }>({ pcoa: [], p_value: null });
const betaResultsPorEnfermedad = ref<{ pcoa: any[]; p_value: number | null }>({ pcoa: [], p_value: null });

const selectedSite = ref("");  // para recordar el site seleccionado
const siteCounts = ref<Record<string,number>>({
  cervix: 0,
  uterus: 0,
  rectum: 0,
  vagina: 0,
  orine: 0
});

const nombreTest = ref<string|null>(null);

//Colores
const colores = [
  '#66c2a5', // verde agua
  '#fc8d62', // salmón
  '#8da0cb', // azul lavanda
  '#e78ac3', // rosa fucsia
  '#a6d854', // lima
  '#ffd92f', // amarillo
  '#1f78b4', // azul fuerte
  '#33a02c', // verde vivo
  '#fb9a99', // rosa claro
  '#fdbf6f', // naranja claro
  '#cab2d6', // lila claro
  '#6a3d9a', // violeta oscuro
  '#b15928', // marrón rojizo
  '#e31a1c', // rojo vivo
  '#ff7f00', // naranja vivo
  '#a6cee3', // azul celeste
  '#b2df8a', // verde pastel
  '#fb8072', // coral
  '#80b1d3', // azul pastel
  '#bc80bd', // púrpura pastel
  '#ffed6f', // amarillo claro
  '#33b5e5', // azul cielo
  '#ff6f69', // rojo coral
  '#2ecc71', // verde menta
  '#e67e22', // naranja tostado
  '#9b59b6', // morado fuerte
  '#3498db', // azul cielo fuerte
  '#f1c40f', // amarillo dorado
  '#e74c3c', // rojo intenso
  '#16a085'  // verde azulado
];

const coloresPorGrupos: Record<number,string>={
  1: '#66c2a5', //verde agua
  2: '#fc8d62',  // salmón
  3: '#8da0cb',  // azul lavanda
  4: '#e78ac3'   // rosa fucsia
}
const coloresPorGruposTransparente: Record<number,string> = {
  1: 'rgba(102,194,165,0.4)', // verde agua
  2: 'rgba(252,141,98,0.4)',  // salmón
  3: 'rgba(141,160,203,0.4)', // azul lavanda
  4: 'rgba(231,138,195,0.4)'  // rosa fucsia
}
let colorMap: Record<string, string> = {};

//Datos computados para construir boxplot por grupo
const shannonViolinData = computed(() => {
  const groups: { [key: number]: string[] } = {};
  for (let i = 1; i <= numGrupos.value; i++) {
    groups[i] = diseases.filter(d => d.group === i).map(d => d.name);
  }

  const getShannonForGroup = (group: string[]) =>
    shannonResults.value.filter(r => group.includes(r.diseases)).map(r => r.shannon).filter(val => typeof val === 'number');

  return {
    labels: Object.keys(groups).map(g => `Group ${g}`),
    datasets: [
      {
        label: 'Shannon Index',
        data: Object.values(groups).map(g => getShannonForGroup(g)),
        backgroundColor: Object.keys(groups).map(g => coloresPorGruposTransparente[parseInt(g)]),
        itemBackgroundColor: Object.keys(groups).map(g => coloresPorGrupos[parseInt(g)]),
        borderColor: Object.keys(groups).map(g => coloresPorGrupos[parseInt(g)]),
        borderWidth: 1,
        outlierRadius: 4,
        itemRadius: 3,
        padding: 10
        
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
      text: 'Shannon diversity index by group'
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

function esSignificativo(p: any): boolean {
  const valor = parseFloat(p);
  const resultado = !isNaN(valor) && valor < 0.05;
  return resultado;
}
/**
 * @brief Calcula el número de pacientes por grupo (según enfermedades asignadas a cada uno).
 */
 const conteoGrupos = computed(() => {
  const conteo: Record<number, number> = {};

  for (let i = 1; i <= numGrupos.value; i++) {
    const enfermedadesDelGrupo = diseases
      .filter(d => d.group === i)
      .map(d => d.name);

    const pacientesDelGrupo = originalItems.value
      .filter(item => enfermedadesDelGrupo.includes(item.diseases)).length;

    conteo[i] = pacientesDelGrupo;
  }

  return conteo;
});


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
 async function loadData(site: string) {
  selectedSite.value = site //Actualizar variable
  originalItems.value = []
  updateItems()
  axios
    .get(import.meta.env.VITE_API_URL +'data/'+ site)
    .then(async (response) => {
      originalItems.value = response.data
      myList.value = ['RM', 'MALE_FACTOR', 'TUBAL_FACTOR', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'] 

      // Recuentos
      numRM.value = countCases('RM')
      numMALE_FACTOR.value = countCases('MALE_FACTOR')
      numTUBAL_FACTOR.value = countCases('TUBAL_FACTOR')
      numENDOMETRIOSIS.value = countCases('ENDOMETRIOSIS')
      numENDOMETRITIS.value = countCases('ENDOMETRITIS')
      numMIOMA.value = countCases('MIOMA')
      numRIF.value = countCases('RIF')
      numUNEXPLAINED.value = countCases('UNEXPLAINED')

      updateItems()

      // Carga de gráficas
      getShannonDiversity(site)
      await getShannonPValue(site);

      getAbundanciaData(site)
      getBetaDiversity(site)
      getRichnessPorGrupo(site);

      //  Esperamos a que se actualicen los grupos
      await nextTick()

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
 
    const ctx = document.getElementById('shannonViolinplotChart') as HTMLCanvasElement //Uso DOM
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
    console.error("Error Shannon Index:", error);
  }
}

const shannonPValue = ref<number | null>(null);
const shannonTest = ref<string | null>(null);

async function getShannonPValue(site: string) {
  if (numGrupos.value < 2) {
    shannonPValue.value = null;
    shannonTest.value = "error_not_enough_groups";
    return;
  }

  const mapeo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0 && myList.value.includes(d.name)) {
      mapeo[d.name] = d.group;
    }
  });

  const gruposUnicos = new Set(Object.values(mapeo));
  const hayGruposValidos = Array.from(gruposUnicos).every(g => {
    return Object.values(mapeo).filter(val => val === g).length > 0;
  });
  // Si no hay al menos 2 grupos definidos con enfermedades seleccionadas, no llamar al backend
  if (gruposUnicos.size < 2 || !hayGruposValidos) {
    shannonPValue.value = null;
    shannonTest.value = "error_not_enough_groups";
    return;
  }

  try {
    const response = await axios.post(`http://localhost:8000/shannon_pvalue?site=${site}`, mapeo);
    shannonPValue.value = response.data.p_value;
    shannonTest.value = response.data.test;
  } catch (error) {
    console.error("Error p-valor --> Shannon:", error);
    shannonPValue.value = null;
    shannonTest.value = null;
  }
}

const richnessPValue = ref<number | null>(null);
const richnessTest = ref<string | null>(null);
async function getRichnessPValue(site: string) {
  if (numGrupos.value < 2) {
    richnessPValue.value = null;
    richnessTest.value = "error_not_enough_groups";
    return;
  }

  const mapeo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0 && myList.value.includes(d.name)) {
      mapeo[d.name] = d.group;
    }
  });

  const gruposUnicos = new Set(Object.values(mapeo));
  if (gruposUnicos.size < 2) {
    richnessPValue.value = null;
    richnessTest.value = "error_not_enough_groups";
    return;
  }

  try {
    const response = await axios.post(`http://localhost:8000/richness_pvalue?site=${site}`, mapeo);
    richnessPValue.value = response.data.p_value;
    richnessTest.value = response.data.test;
  } catch (error) {
    console.error("Error p-valor --> Richness:", error);
    richnessPValue.value = null;
    richnessTest.value = null;
  }
}




/**
 * @brief Obtiene los datos del backend para el gráfico de riqueza 
 * @param site El sitio del cuerpo para el cual se quiere obtener la abundancia

*/ 
async function getRichnessPorGrupo(site: string) {
  if (numGrupos.value < 1) {
    richnessPorGrupo.value = [];
    return;
  }

  const mapeo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0 && myList.value.includes(d.name)) {
      mapeo[d.name] = d.group;
    }
  });

  try {
    const response = await axios.post(`http://localhost:8000/richness?site=${site}`, mapeo);
    richnessPorGrupo.value = response.data;
    drawRichnessChart();
  } catch (error) {
    console.error("Error --> Richness index:", error);
    richnessPorGrupo.value = [];
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

    const keys = Object.keys(abundanciaData.value[0]).filter(k => k.startsWith('x'));
    colorMap = {}; // reiniciamos el mapa
    keys.forEach((k, i) => {
      colorMap[k] = colores[i % colores.length];
    });

  } catch (error) {
    console.error("Error -->Abundances:", error);
  }

  await nextTick();
  drawAbundanciaChart();
  if (numGrupos.value > 0) {
    await nextTick();
    drawAbundanciaPorGrupoChartFiltrado();
  }

}

/**
 * @brief Obtiene del backend las coordenadas PCoA calculadas a partir
 *        de la diversidad beta (distancias Bray-Curtis) para un sitio dado
 * @param site Nombre del sitio anatómico 
 */
async function getBetaDiversity(site: string) {
  try {
    // 1. Obtener SIEMPRE los datos de diversidad beta por enfermedad
    const responseEnfermedad = await axios.get(`http://localhost:8000/beta?site=${site}`);
    betaResultsPorEnfermedad.value = responseEnfermedad.data;
    await nextTick();

    drawPCoAChart(); // pcoaChart por enfermedad

    // 2. Si hay grupos, obtenemos beta_por_grupo
    const mapeo: Record<string, number> = {};
    diseases.forEach(d => {
      if (d.group > 0 && myList.value.includes(d.name)) {
        mapeo[d.name] = d.group;
      }
    });

    const gruposUnicos = new Set(Object.values(mapeo));
    if (gruposUnicos.size >= 2) {
      const responseGrupo = await axios.post(`http://localhost:8000/beta_por_grupo?site=${site}`, mapeo);
      betaResults.value = responseGrupo.data;
      await nextTick();
      drawPCoAChartPorGrupo(); 
    } else {
      // Si no hay suficientes grupos, vaciamos ese gráfico
      const canvasGrupo = document.getElementById('pcoaChartPorGrupo') as HTMLCanvasElement;
      if (canvasGrupo && Chart.getChart(canvasGrupo)) {
        Chart.getChart(canvasGrupo)?.destroy();
      }
      betaResults.value = { pcoa: [], p_value: null };
    }

  } catch (error) {
    console.error("Error Beta Diversity:", error);
  }
}




/**
 * @brief Obtiene del backend los biomarcadores diferenciales entre dos grupos
 * @param site Nombre del sitio anatómico 
 */
 const biomarcadores = ref([]);

async function getBiomarcadores(site: string) {
  if (numGrupos.value < 2) {
    biomarcadores.value = [];
    return;
  }

  const mapeo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0) {
      mapeo[d.name] = d.group;
    }
  });

  try {
    const response = await axios.post(`http://localhost:8000/biomarcadores?site=${site}`, mapeo);

    biomarcadores.value = response.data.map((row: any) => {
      const microKey = row.micro;
      const entry = mother.value[microKey];
      const nombre_limpio =
        entry && (entry[1] || '').trim() !== ''
          ? entry[1].trim()
          : entry && (entry[0] || '').trim() !== ''
          ? entry[0].trim()
          : row.micro;

      return {
        ...row,
        nombre_limpio
      };
    });
    // Ordenar por p_value de menor a mayor
    biomarcadores.value.sort((a, b) => {
      const pA = parseFloat(a.p_value);
      const pB = parseFloat(b.p_value);
      if (isNaN(pA)) return 1;
      if (isNaN(pB)) return -1;
      return pA - pB;
    });
    nombreTest.value = response.data.length > 0 ? response.data[0].test : null;


  } catch (error) {
    console.error("Error biomarkers:", error);
    biomarcadores.value = [];
  }
}



const abundanciaPorGrupo = ref<any[]>([]);

async function getAbundanciaPorGrupo(site: string) {
  const mapeo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0 && myList.value.includes(d.name)) {
      mapeo[d.name] = d.group;
    }
  });

  //Evita que cree grupos que no se han asignado
  if (Object.keys(mapeo).length === 0) {
    abundanciaPorGrupo.value = []; // limpiamos el gráfico
    drawAbundanciaPorGrupoChartFiltrado();
    return;
  }
  try {
  const response = await axios.post(`http://localhost:8000/abundancia_por_grupo?site=${site}`, mapeo);

  abundanciaPorGrupo.value = response.data.map((fila, i) => {
    const microKey = fila.micro.toUpperCase();
    const entry = mother.value[microKey];
    let nombre = fila.micro;

    if (entry) {
      const name1 = (entry[1] || '').trim();
      const name0 = (entry[0] || '').trim();
      nombre = name1 !== '' ? name1 : (name0 !== '' ? name0 : fila.micro);
    }

    if (!colorMap[nombre]) {
      colorMap[nombre] = colores[i % colores.length];
    }

    return {
      ...fila,
      nombreMostrado: nombre
    };
  });

  drawAbundanciaPorGrupoChartFiltrado(); 

} catch (error) {
  console.error("Error Relative abundance:", error);
}
}



/**
 * @brief Dibuja el gráfico de dispersión (scatterplot) de diversidad beta
 *        usando las dos primeras componentes principales (PCoA).
 */
 function drawPCoAChart() {
  const canvas = document.getElementById('pcoaChart') as HTMLCanvasElement; //uso DOM
  if (!canvas) return;

  const pcoaData = betaResultsPorEnfermedad.value?.pcoa;

  if (!Array.isArray(pcoaData)) {
    console.warn("PCoA data is missing or not an array.");
    return;
  }

  if (Chart.getChart(canvas)) {
    Chart.getChart(canvas)?.destroy();
  }

  const pc1 = pcoaData.map(r => r.PC1);
  const pc2 = pcoaData.map(r => r.PC2);
  const samples = pcoaData.map(r => r.sample_id);
  const diseases = pcoaData.map(r => r.diseases);

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
  for (let i = 0; i < pc1.length; i++) {
    const disease = diseases[i];
    if (!myList.value.includes(disease)) continue;

    if (!grupos[disease]) grupos[disease] = [];
    grupos[disease].push({
      x: pc1[i],
      y: pc2[i],
      label: pcoaData[i]["sample_id"] || `Sample ${i + 1}`
    });
  }



  // Crear un dataset por enfermedad
  const datasets = Object.keys(grupos).map((disease) => ({
    label: disease,
    data: grupos[disease],
    backgroundColor: colorPorEnfermedad[disease] || '#000000', // fallback negro
    pointRadius: 7,
    pointHoverRadius: 10,
    pointHitRadius: 10, // mejora la detección del ratón
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
          enabled:true,
          callbacks: {
            label: function(context: any) {
              const p = context.raw;
              const label = p.label || 'No Label';
              return `${label} (${context.dataset.label})`;
            
            }
          }
        },
        title: {
          display: true,
          text: 'PCoA scatterplot by condition (Beta-diversity)'
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

  // Mapeo de enfermedad a grupo
  const enfermedadAGrupo: Record<string, number> = {};
  diseases.forEach(d => {
    if (d.group > 0) enfermedadAGrupo[d.name] = d.group;
  });

  const grupos: Record<number, any[]> = {};
  betaResults.value.pcoa.forEach((fila) => {
    const enfermedad = fila.diseases;
    const grupo = enfermedadAGrupo[enfermedad];

    if (grupo && myList.value.includes(enfermedad)) {
      if (!grupos[grupo]) grupos[grupo] = [];
      grupos[grupo].push({
        x: fila.PC1,
        y: fila.PC2,
        label: fila["sample_id"] || `Sample`
      });
    }
  });

  const datasets = Object.keys(grupos).map((g) => ({
    label: `Group ${g}`,
    data: grupos[Number(g)],
    backgroundColor: coloresPorGrupos[parseInt(g)] || '#000000',
    pointRadius: 7,
    pointHoverRadius: 10,
    pointHitRadius: 10,
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
          text: 'PCoA scatterplot by group (Beta-diversity)'
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
  colores.value = {}; 
  if (!abundanciaData.value || abundanciaData.value.length === 0) return;

  const ctx = document.getElementById('abundanciaChart') as HTMLCanvasElement;
  if (!ctx) return;

  const oldChart = Chart.getChart(ctx);
  if (oldChart) oldChart.destroy();

  if (myList.value.length === 0) return;

  // Filtrar por enfermedades seleccionadas
  const filtrado = abundanciaData.value.filter(d => myList.value.includes(d.diseases));

  // Agrupar por enfermedad → micro → sumar abundancia
  const grupos: Record<string, Record<string, number>> = {};
  filtrado.forEach(({ diseases, micro, abundance }) => {
    if (!grupos[diseases]) grupos[diseases] = {};
    grupos[diseases][micro] = (grupos[diseases][micro] || 0) + abundance;
  });

  // Lista de enfermedades visibles (labels)
  const enfermedades = Object.keys(grupos);

  // Suma total por microbio (para elegir los top 15)
  const totalMicro: Record<string, number> = {};
  filtrado.forEach(({ micro, abundance }) => {
    totalMicro[micro] = (totalMicro[micro] || 0) + abundance;
  });

  const topMicro = Object.entries(totalMicro)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([m]) => m);

  const otherMicro = Object.keys(totalMicro).filter(m => !topMicro.includes(m));

  // Colores
  topMicro.forEach((m, i) => {
    if (!colorMap[m]) colorMap[m] = colores[i % colores.length];
  });

  // Normalización por enfermedad
  const normalizado: Record<string, number> = {};
  for (const enf in grupos) {
    const total = Object.values(grupos[enf]).reduce((a, b) => a + b, 0);
    normalizado[enf] = total > 0 ? total : 1;
  }

  // Construcción de datasets
  const datasets = topMicro.map(micro => ({
    label: (mother.value[micro.toUpperCase()]?.[1] || '').trim() !== ''
      ? mother.value[micro.toUpperCase()][1]
      : (mother.value[micro.toUpperCase()]?.[0] || micro),
    data: enfermedades.map(enf => (grupos[enf]?.[micro] || 0) / normalizado[enf] * 100),
    backgroundColor: colorMap[micro] || '#000000',
    stack: 'stack1'
  }));

  // Dataset de "Otros"
  const otros = enfermedades.map(enf =>
    otherMicro.reduce((sum, m) => sum + (grupos[enf]?.[m] || 0), 0) / normalizado[enf] * 100
  );
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
          text: 'Relative abundance by condition'
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            usePointStyle: true
          }
        }
      },
      scales: {
        x: { stacked: true },
        y: {
          stacked: true,
          max: 100,
          title: {
            display: true,
            text: 'Relative abundance (%)'
          }
        }
      }
    }
  });
}


function drawAbundanciaPorGrupoChartFiltrado() {
  const canvas = document.getElementById('abundanciaChartFiltrado') as HTMLCanvasElement;
  if (!canvas) return;

  const oldChart = Chart.getChart(canvas);
  if (oldChart) {
    oldChart.destroy();
  }

  if (!abundanciaPorGrupo.value || abundanciaPorGrupo.value.length === 0) return;

  // Agrupar por grupo
  const grupos: Record<number, Record<string, number>> = {};
  abundanciaPorGrupo.value.forEach(fila => {
    const g = fila.grupo;
    const micro = fila.micro;
    const valor = fila.abundance ?? 0;
    if (!grupos[g]) grupos[g] = {};
    grupos[g][micro] = valor;
  });

  const allMicro = Array.from(new Set(abundanciaPorGrupo.value.map(f => f.micro)));

  // Elegir los top 15 microorganismos más abundantes
  const sumaTotal: Record<string, number> = {};
  allMicro.forEach(m => {
    sumaTotal[m] = abundanciaPorGrupo.value
      .filter(f => f.micro === m)
      .reduce((sum, f) => sum + (f.abundance || 0), 0);
  });

  const topMicro = Object.entries(sumaTotal)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([key]) => key);

  const otherMicro = allMicro.filter(m => !topMicro.includes(m));
  const labels = Object.keys(grupos).map(g => `Group ${g}`);

  // Recalcula porcentajes normalizados por fila
  const normalizadoPorGrupo: Record<number, number> = {};
  Object.entries(grupos).forEach(([g, fila]) => {
    const suma = Object.values(fila).reduce((acc, val) => acc + val, 0);
    normalizadoPorGrupo[+g] = suma > 0 ? suma : 1; // evita división por 0
  });

  const datasets = topMicro.map(micro => {
    const filaConNombre = abundanciaPorGrupo.value.find(f => f.micro === micro);
    const nombre = filaConNombre?.nombreMostrado || micro;

    return {
      label: nombre,
      backgroundColor: colorMap[nombre] || '#000000',
      data: Object.keys(grupos).map(g => (grupos[+g][micro] || 0) / normalizadoPorGrupo[+g] * 100),
      stack: 'stack1'
    };
  });

  // Dataset de "Otros"
  const otros = Object.keys(grupos).map(g =>
    otherMicro.reduce((sum, micro) => sum + (grupos[+g][micro] || 0), 0) / normalizadoPorGrupo[+g] * 100
  );


  datasets.push({
    label: 'Otros',
    data: otros,
    backgroundColor: '#999999',
    stack: 'stack1'
  });


  new Chart(canvas, {
    type: 'bar',
    data: { labels, datasets },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Relative abundance by group'
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            usePointStyle: true
          }
        }
      },
      scales: {
        x: { stacked: true },
        y: {
          stacked: true,
          max: 100,
          title: {
            display: true,
            text: 'Relative abundance  (%)'
          }
        }
      }
    }
  });
}

function drawRichnessChart() {
  const canvas = document.getElementById('richnessChart') as HTMLCanvasElement;
  if (!canvas) return;

  const oldChart = Chart.getChart(canvas);
  if (oldChart) oldChart.destroy();

  // Claves numéricas para que el color se asigne bien
  const grupos: Record<number, number[]> = {};
  richnessPorGrupo.value.forEach(fila => {
    const grupo = fila.grupo;
    if (!grupos[grupo]) grupos[grupo] = [];
    grupos[grupo].push(...fila.richness);
  });

  const labels = Object.keys(grupos).map(g => `Grupo ${g}`);
  const data = Object.values(grupos);
  const coloresG = Object.keys(grupos).map(g => coloresPorGrupos[parseInt(g)] || '#cccccc');
  const coloresTransparentes = Object.keys(grupos).map(g => coloresPorGruposTransparente[parseInt(g)] || 'rgba(200,200,200,0.4)');

  new Chart(canvas, {
    type: 'violin',
    data: {
      labels: labels,
      datasets: [{
        label: 'Richness (Number of genera)',
        data: data,
        backgroundColor: coloresTransparentes,
        itemBackgroundColor: coloresG,
        borderColor: coloresG,
        borderWidth: 1,
        outlierRadius: 4,
        itemRadius: 3,
        padding: 10
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'Richness index by group'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of genera'
          }
        }
      }
    }
  });
}






/**
 * @brief Carga los metadatos de todas las muestras desde el backend,
 *        llama a 'check()' para seleccionar el sitio en función de la ruta,
 *      y muestra una gráfica inicial si hay canvas disponible
 */
onMounted(() => {
  // 1. Cargar diccionario 'mother'
  axios
    .get(import.meta.env.VITE_API_URL + 'data/mother')
    .then((res) => {
      mother.value = res.data;
    });

  // 2. Cargar diccionario de muestras por site
  axios.get(import.meta.env.VITE_API_URL + 'data/all')
    .then((res) => {
      check();
    })
    .catch((error) => {
      console.error('Error:', error);
  });

  contarTodosLosSitios();
    //Comprobación
    nextTick(() => {

    const canvas = document.getElementById('shannonChart') as HTMLCanvasElement;
    if (canvas) {
      new Chart(canvas, {
        type: 'violinplot',
        data: shannonViolinData.value,
        
        options: chartOptions
      });
    }
    const checks = document.querySelectorAll('.disease-check') as NodeListOf<HTMLInputElement>;
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

/**
 * @brief Watch reactivo para redibujar automaticamente los gráficos por grupos
 */
watch(numGrupos, async () => {
  await nextTick();
  if (selectedSite.value && numGrupos.value > 0) {
    await getAbundanciaPorGrupo(selectedSite.value);
  }
  if (abundanciaData.value.length > 0) {
    drawAbundanciaPorGrupoChartFiltrado();
  }
  if (betaResults.value && betaResults.value["PC1"]) {
    drawPCoAChartPorGrupo();
  }
});
/**
 * @brief watch reactivo para los cambios en los grupos de enfermedades
 */
watch(
  () => diseases.map(d => d.group), // array de grupos actuales
  async () => {
    await nextTick();
    if (numGrupos.value > 0) {
      if (selectedSite.value) {
        await getAbundanciaPorGrupo(selectedSite.value); // Cargar datos antes de pintar
        await getRichnessPorGrupo(selectedSite.value);
        await getBetaDiversity(selectedSite.value);
        await getShannonPValue(selectedSite.value);
        await getRichnessPValue(selectedSite.value);


      }
      drawAbundanciaPorGrupoChartFiltrado();
      drawPCoAChartPorGrupo();
      // Añadimos esta llamada cuando los grupos están definidos
      const hayAlMenosDosGrupos = diseases.some(d => d.group === 1) && diseases.some(d => d.group === 2);
      if (hayAlMenosDosGrupos && selectedSite.value) {
        getBiomarcadores(selectedSite.value);
      }
    }
  },
  { deep: true }
);
/**
 * @brief watch reactivo para los cambios en las checkbox de conditions
 */
watch(myList, async () => {
  await nextTick();
  drawAbundanciaChart();
  if (numGrupos.value > 0) {
    drawAbundanciaPorGrupoChartFiltrado();
    drawPCoAChartPorGrupo();
  } else {
    drawPCoAChart();
  }
}, { deep: true });

watch(myList, async () => {
  await nextTick();
  const canvas = document.getElementById('shannonViolinplotChart') as HTMLCanvasElement;
  if (canvas && Chart.getChart(canvas)) {
    Chart.getChart(canvas)?.destroy();
  }

  new Chart(canvas, {
    type: 'violin',
    data: shannonViolinData.value,
    options: chartOptions
  });
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

async function contarTodosLosSitios() {
  const sitios = ['cervix', 'uterus', 'rectum', 'vagina', 'orine'];
  for (const sitio of sitios) {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + 'data/' + sitio);
      siteCounts.value[sitio] = response.data.length;
    } catch (error) {
      console.warn(`Error in samples --> ${sitio}:`, error);
      siteCounts.value[sitio] = 0;
    }
  }
}

function resetSelections() {
  // Deseleccionar todas las enfermedades
  myList.value = [];

  // Resetear todos los grupos
  diseases.forEach(d => d.group = 0);
  numGrupos.value = 0;

  // Desmarcar todos los site manualmente
  const radios = document.querySelectorAll('input[type="radio"][name="radioButton"]');
  radios.forEach((radio) => {
    (radio as HTMLInputElement).checked = false;
  });

  // Resetear dataset visualizado
  originalItems.value = [];
  items.value = [];
  patiens.value = 0;

    // Limpiar gráficos generales
    drawAbundanciaChart();
  drawPCoAChart();

  // Limpiar gráficos por grupo
  abundanciaPorGrupo.value = [];
  drawAbundanciaPorGrupoChartFiltrado();

  const canvasGrupo = document.getElementById('pcoaChartPorGrupo') as HTMLCanvasElement;
  if (canvasGrupo && Chart.getChart(canvasGrupo)) {
    Chart.getChart(canvasGrupo)?.destroy();
  }

  biomarcadores.value = [];
}

</script>