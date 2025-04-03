<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-light">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-5 min-vh-100">
          <ul class="list-group">
            <li
                class="list-group-item list-group-item-dark d-flex justify-content-between align-items-center"
                >
                Site
            </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputCervix"
                    type="radio"
                    id="inputCervix"
                    name="radioButton"
                    @click="loadData('cervix')"
                    />
                Cervix<span class="badge badge-pill bg-secondary float-end"> 82 </span>
              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputUterus"
                    type="radio"
                    id="inputUterus"
                    name="radioButton"
                    @click="loadData('uterus')"
                    />
                Uterus<span class="badge badge-pill bg-secondary float-end"> 79 </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputRectum"
                    type="radio"
                    id="inputRectum"
                    name="radioButton"
                    @click="loadData('rectum')"
                    />
                Rectum<span class="badge badge-pill bg-secondary float-end"> 89 </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputVagina"
                    type="radio"
                    id="inputVagina"
                    name="radioButton"
                    @click="loadData('vagina')"
                    />
                Vagina<span class="badge badge-pill bg-secondary float-end"> 89 </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputOrine"
                    type="radio"
                    id="inputOrine"
                    name="radioButton"
                    @click="loadData('orine')"
                    />
                Urine<span class="badge badge-pill bg-secondary float-end"> 86 </span>

              </li>
          </ul>
          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">
              <label for="groupSelector">Groups</label>
              <select class="form-select mt-2" id="groupSelector" @change="handleGroupSelection($event)">
                
                <option value="">-- Select group --</option>
                <option value="1">Grupo 1</option>
                <option value="2">Grupo 2</option>
                <option value="3">Grupo 3</option>
              </select>

            </li>
          </ul>
          <br />
          
          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">Condition</li>
            <li class="list-group-item d-flex justify-content-between flex-wrap align-items-center" v-for="disease in diseases" :key="disease.name">
              <div class="d-flex align-items-center flex-wrap overflow-hidden">
                <input
                  class="form-check-input me-1 disease-check"
                  :id="'check_' + disease.name"
                  type="checkbox"
                  :value="disease.name"
                  v-model="myList"
                />
                {{ disease.name }}
                <span class="badge badge-pill bg-secondary ms-2">{{ getCount(disease.name) }}</span>
              </div>
              <select class="form-select form-select-sm w-auto "  v-model.number="disease.group" @change="updateGroupAssignments">
                <option value="0">Sin grupo</option>
                <option value="1">Grupo 1</option>
                <option value="2">Grupo 2</option>
                <option value="3">Grupo 3</option>
              </select>
            </li>
          </ul>
        </div>
      </div>
    <!-- Contenido Principal -->
    <div class="col py-3">
        <h3>Analytics Section</h3>
        <p>Here you can visualize and analyze selected data.</p>
      </div>
      <div class="mt-4">
        <h5 class="mt-4">Boxplot del índice de Shannon por grupo</h5>
            <canvas id="shannonBoxplotChart" style="max-width: 700px;"></canvas>

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



</style>

<script lang="ts" setup>
import { ref, onMounted, nextTick, reactive, computed} from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router';

//Para boxplot
/*
<VueChart
              :type="'boxplot'"
              :data="shannonBoxData"
              :options="chartOptions"
              style="max-width: 700px;"
            />
            */
/*
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
                <td>{{ row.mean.toFixed(4) }}</td>
                <td>{{ row.std.toFixed(4) }}</td>
                <td>{{ row.count }}</td>
              </tr>
            </tbody>
          </table>
            <div class="Grafico Shannon">
              <canvas id="shannonBoxplotChart" style="max-width: 700px;"></canvas>

          </div>
*/
import { Chart, registerables } from 'chart.js';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';

Chart.register(...registerables, BoxPlotController, BoxAndWiskers);
console.log("✔️ Controladores disponibles:", Object.keys(Chart.registry.controllers))


console.log("Registro completo:", Chart.registry);

console.log("Tipos registrados:", Object.keys(Chart.registry.controllers));

/*
declare module 'chart.js' {
  interface ChartTypeRegistry {
    boxplot: {
      chartOptions: any;
      datasetOptions: any;
      defaultDataPoint: number[];
    };
  }
}
*/


const route = useRoute();

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

interface Item {
  [key: string]: any;
}

interface MotherType {
  [key: string]: any;
}


const selectedGroups = ref<number[]>([]);


const items = ref<Item[]>([])
const originalItems = ref<Item[]>([])
const myList = ref<string[]>([])

const patiens = ref(0)

const numRM = ref(0)
const numMALE_FACTOR = ref(0)
const numTUBAL_FACTOR = ref(0)
const numENDOMETRIOSIS = ref(0)
const numENDOMETRITIS = ref(0)
const numMIOMA = ref(0)
const numRIF = ref(0)
const numUNEXPLAINED = ref(0)

const mother = ref({})
//Guardar resultados Shannon
const shannonResults = ref<any[]>([]);
const shannonSummary = ref<any[]>([]);

////************PARA EL BOXPLOT  *************/////
const shannonBoxData = computed(() => {
  const group1 = diseases
    .filter(d => d.group === 1)
    .map(d => d.name);
  const group2 = diseases
    .filter(d => d.group === 2)
    .map(d => d.name);
  const group3 = diseases
    .filter(d => d.group === 3)
    .map(d => d.name);

  function getShannonForGroup(group: string[]) {
    return shannonResults.value
      .filter(r => group.includes(r.diseases))
      .map(r => r.shannon)
      .filter(val => typeof val === 'number');
  }

  return {
    labels: ['Grupo 1', 'Grupo 2', 'Grupo 3'],
    datasets: [
      {
        label: 'Índice de Shannon',
        data: [
          getShannonForGroup(group1),
          getShannonForGroup(group2),
          getShannonForGroup(group3)
        ]
      }
    ]
  };
});
////************PARA EL BOXPLOT  *************/////


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




function getCount(disease: string) {
  return eval('num' + disease);
}

const filteredShannonResults = computed(() => {
  if (selectedGroups.value.length === 0) return shannonResults.value;

  const selectedConditions = diseases
    .filter(d => selectedGroups.value.includes(d.group))
    .map(d => d.name);

  return shannonResults.value.filter(item =>
    selectedConditions.includes(item.diseases)
  );
});




/*
function updateGroupAssignments() {
  // Cuando el usuario cambia el grupo desde el desplegable, actualizamos los grupos seleccionados si aplica
  selectedGroups.value = [...new Set(diseases.value.map(d => d.group).filter(g => g > 0))];
  updateItems();
}*/
function countCases(site: string) {
  var filtrados = originalItems.value.filter(item => item.diseases === site) 
  return filtrados.length
}



function updateGroupAssignments() {
  if (selectedGroups.value.length === 1) {
    const selected = selectedGroups.value[0];

    // Recalcular qué enfermedades pertenecen a ese grupo
    const selectedDiseases = diseases
      .filter(d => d.group === selected)
      .map(d => d.name);

    // Actualizar la lista de seleccionados
    myList.value = [...selectedDiseases];
    console.log("Enfermedades que pertenecen al grupo seleccionado:", selectedDiseases);
    console.log("Estado de diseases:", JSON.stringify(diseases, null, 2));

    updateItems();
  }
}


function loadData(site: string){

  originalItems.value = []
  updateItems()
  axios
    .get(import.meta.env.VITE_API_URL + site)
    .then((response) => {

      originalItems.value = response.data
      
      console.log("Datos cargados:", originalItems.value);
      console.log("Ejemplo de dato:", originalItems.value[0]);

      myList.value = ['RM', 'MALE_FACTOR', 'TUBAL_FACTOR', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'] 
      numRM.value = countCases('RM')
      numMALE_FACTOR.value = countCases('MALE_FACTOR')
      numTUBAL_FACTOR.value = countCases('TUBAL_FACTOR')
      numENDOMETRIOSIS.value = countCases('ENDOMETRIOSIS')
      numENDOMETRITIS.value = countCases('ENDOMETRITIS')
      numMIOMA.value = countCases('MIOMA')
      numRIF.value = countCases('RIF')
      numUNEXPLAINED.value = countCases('UNEXPLAINED')
      updateItems()
      //Llamada al endpoint de Shannon
      getShannonDiversity(site);
      /*  **No es necesario porque usamos v-model="myList"
      const inputs = document.querySelectorAll('.disease-check');
      inputs.forEach((elem) => {
           (elem as HTMLInputElement).checked = true
      });
      */
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}
//Función para conectar con backend
async function getShannonDiversity(site: string) {
  try {
    const response = await axios.get(`http://localhost:8000/shannon?site=${site}`);
    shannonResults.value = response.data.resumen_muestra;
    shannonSummary.value = response.data.resumen_enfermedad;
    await nextTick()  // Espera a que el DOM esté actualizado

    const ctx = document.getElementById('shannonBoxplotChart') as HTMLCanvasElement
    if (ctx) {
      new Chart(ctx, {
        type: 'boxplot',
        data: shannonBoxData.value,  // 👈 esto ya lo tienes definido
        options: chartOptions        // 👈 esto también lo tienes definido
      })
    }


    console.log("Shannon por muestra:", shannonResults.value);
    console.log("Resumen por enfermedad:", shannonSummary.value);
  } catch (error) {
    console.error("Error al obtener índice de Shannon:", error);
  }
}



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

    console.log("myList después de asignar:", myList.value);

    // Recorre los checkbox del DOM
    const checkboxes = document.querySelectorAll('.disease-check');
    checkboxes.forEach((c) => {
      console.log("Checkbox ID:", c.id, " Value:", (c as HTMLInputElement).value);
    });

    updateItems();
  });
}


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
    //COmprobación
    nextTick(() => {
      console.log("Boxplot data:", shannonBoxData.value);

    const canvas = document.getElementById('shannonChart') as HTMLCanvasElement;
    if (canvas) {
      new Chart(canvas, {
        type: 'boxplot',
        data: shannonBoxData.value,
        
        options: chartOptions
      });
    }
    const checks = document.querySelectorAll('.disease-check') as NodeListOf<HTMLInputElement>;
    checks.forEach(c => {
      console.log("Checkbox ID:", c.id, " Value:", c.value);
    });
  });
  
})

////************PARA EL BOXPLOT INI *************/////

import { watch } from 'vue';

watch(shannonBoxData, async (newData) => {
  await nextTick(); // Espera a que el DOM esté actualizado
  const canvas = document.getElementById('shannonBoxplotChart') as HTMLCanvasElement;

  if (canvas) {
    // Destruir el gráfico anterior si existe
    if (Chart.getChart(canvas)) {
      Chart.getChart(canvas)?.destroy();
    }

    new Chart(canvas, {
      type: 'boxplot',
      data: newData,
      options: chartOptions
    });
  }
});

////************PARA EL BOXPLOT  FIN *************/////

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