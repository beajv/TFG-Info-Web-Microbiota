<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-light">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-5 min-vh-100">
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark custom-header">Taxon level</li>
            <li class="list-group-item">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  :checked="isChecked"
                  id="inputGenus"
                  />
                  <label for="inputGenus">Genus</label>
              Genus
            </li>
            <li class="list-group-item ">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  disabled
                  aria-label="Species checkbox (disabled)"
                  />
              Species
            </li>
          </ul>
          <br />
          <ul class="list-group ">
            <li
                class="list-group-item list-group-item-dark d-flex justify-content-between align-items-center custom-header"
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
                    <label for="inputCervix">Cervix</label>
                <span class="badge badge-pill bg-secondary float-end"> {{ siteCounts.cervix }}</span>
              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputUterus"
                    type="radio"
                    id="inputUterus"
                    name="radioButton"
                    @click="loadData('uterus')"
                    />
                    <label for="inputUterus">Uterus</label>
                <span class="badge badge-pill bg-secondary float-end"> {{ siteCounts.uterus }} </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputRectum"
                    type="radio"
                    id="inputRectum"
                    name="radioButton"
                    @click="loadData('rectum')"
                    />
                    <label for="inputRectum">Rectum</label>
                <span class="badge badge-pill bg-secondary float-end"> {{ siteCounts.rectum }} </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputVagina"
                    type="radio"
                    id="inputVagina"
                    name="radioButton"
                    @click="loadData('vagina')"
                    />
                    <label for="inputVagina">Vagina</label>
                <span class="badge badge-pill bg-secondary float-end"> {{ siteCounts.vagina }} </span>

              </li>
              <li class="list-group-item align-items-center">
                <input
                    class="form-check-input me-1 inputOrine"
                    type="radio"
                    id="inputOrine"
                    name="radioButton"
                    @click="loadData('orine')"
                    />
                    <label for="inputOrine">Urine</label>
                <span class="badge badge-pill bg-secondary float-end"> {{ siteCounts.orine }} </span>

              </li>
          </ul>
          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark custom-header">Project</li>
            <li class="list-group-item">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  :checked="isChecked"
                  id="inputProject"
                  />
              Granada-Junio
            </li>
          </ul>

          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark custom-header">Conditions</li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('RM')" type="checkbox"/>RM <span class="badge badge-pill bg-secondary float-end"> {{ numRM }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('MALE_FACTOR')" type="checkbox"/>MALE_FACTOR<span class="badge badge-pill bg-secondary float-end"> {{ numMALE_FACTOR }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('TUBAL_FACTOR')" type="checkbox"/>TUBAL_FACTOR<span class="badge badge-pill bg-secondary float-end"> {{ numTUBAL_FACTOR }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('ENDOMETRIOSIS')" type="checkbox"/>ENDOMETRIOSIS<span class="badge badge-pill bg-secondary float-end"> {{ numENDOMETRIOSIS }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('ENDOMETRITIS')" type="checkbox"/>ENDOMETRITIS<span class="badge badge-pill bg-secondary float-end"> {{ numENDOMETRITIS }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('MIOMA')" type="checkbox"/>MIOMA<span class="badge badge-pill bg-secondary float-end"> {{ numMIOMA }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('RIF')" type="checkbox"/>RIF<span class="badge badge-pill bg-secondary float-end"> {{ numRIF }} </span></li>
            <li class="list-group-item"> <input class="form-check-input me-1 disease-check" @click="filterDisease('UNEXPLAINED')" type="checkbox"/>UNEXPLAINED<span class="badge badge-pill bg-secondary float-end"> {{ numUNEXPLAINED }} </span></li>
          </ul>
        </div>
      </div>
      <div class="col py-3">
        <h3>Associated species</h3>
        <p>· Number of patients: {{ patiens }}</p>
        <table class="table table-hover aling-middle text-center">
          <thead>
            <tr>
              <th>Genus</th>
              <th>Links to ENA</th>
              <th>Links to NCBI</th>
              <th>Found in Nr. of samples</th>
              <th>Relative abundance (mean, median, SD)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item) in resultItems" >
<td>
  {{
    (() => {
      const micro = item.name;
      const data = (mother as MotherType)[micro];
      return data && data[1] ? data[1] : micro;
    })()
  }}
</td>

<!-- OPCION 1-->
<!--
<td>
    <a
    :href="'https://www.ebi.ac.uk/ena/browser/view/Taxon:' + (mother as MotherType)[item.name.toUpperCase()][2]"
    target="_blank"
    rel="noopener noreferrer"
    class="btn btn-sm btn-outline-primary"
  >
    ENA 
  </a>
</td>
<td>
  <a
    :href="'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=' + (mother as MotherType)[item.name.toUpperCase()][3]"
    target="_blank"
    rel="noopener noreferrer"
    class="btn btn-sm btn-outline-success"
  >
    NCBI
  </a>
</td>
-->
<!-- OPCION 2-->

<td>
    <a
    :href="'https://www.ebi.ac.uk/ena/browser/view/Taxon:' + (mother as MotherType)[item.name][2]"
    target="_blank"
    rel="noopener noreferrer"
    class="btn btn-sm btn-outline-success"
    title="View in ENA"
  >
    <img src="/ENA logo.png" alt="ENA" style="height:22px;"/>
  </a>
</td>
<td>
  <a
    :href="'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=' + (mother as MotherType)[item.name][3]"
    target="_blank"
    rel="noopener noreferrer"
    class="btn btn-sm btn-outline-primary"
    title="View in NCBI"
  >
  <img src="/ncbi logo.png" alt="NCBI" style="height:22px;"/>
  </a>
</td>

              <td>{{ item.countComplete }}</td>
              <td>{{ item.relative }}</td>
            </tr>
          </tbody>
        </table>
<nav aria-label="Page navigation example">
  <ul class="pagination justify-content-center">
    <li class="page-item"  :class="{ 'disabled': pagina === 1 }" v-if="patiens">
      <a class="page-link" href="#"  @click="cambiarPagina(pagina-1)"  aria-label="Página anterior">Previous</a>
    </li>
    <li v-for="i in modulo" :key="i" class="page-item " :class="{ 'active': i === pagina }" @click="cambiarPagina(i)" :aria-label="'Ir a la página ' + i"><a class="page-link" href="#">{{ i }}</a></li>
    <li class="page-item">
      <a class="page-link" v-if="patiens" :class="{ 'disabled': pagina === modulo }" href="#" @click="cambiarPagina(pagina+1)" aria-label="Página siguiente" >Next</a>
    </li>
  </ul>
</nav>
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
/* títulos de columna (thead > th) */
.table thead th {
  background-color: #08c0056f; 
  color: white;              /* Texto en blanco */
  font-weight: bold;
  text-align: center;
  border-bottom: 2px solid #ccc; /* Línea de separación */
}
.custom-header {
  background-color: #4e73df; 
  color: white;
  font-weight: bold;
}

</style>

<script lang="ts" setup>
import { ref, onMounted , watch, nextTick} from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router';
const route = useRoute();


interface Item {
  [key: string]: any;
}

interface MotherType {
  [key: string]: any;
}



const items = ref<Item[]>([])
const originalItems = ref<Item[]>([])
const resultItems = ref<Item[]>([])
const myList = ref<string[]>([])

const patiens = ref(0)
const modulo = ref(0)
const pagina = ref(1)


const numRM = ref(0)
const numMALE_FACTOR = ref(0)
const numTUBAL_FACTOR = ref(0)
const numENDOMETRIOSIS = ref(0)
const numENDOMETRITIS = ref(0)
const numMIOMA = ref(0)
const numRIF = ref(0)
const numUNEXPLAINED = ref(0)

const isChecked = ref(true)
const mother = ref({})

const siteCounts = ref<{ [key: string]: number }>({
  cervix: 0,
  uterus: 0,
  rectum: 0,
  vagina: 0,
  orine: 0
});



function cambiarPagina(pagina_click : number){
   pagina.value = pagina_click
   calculateValues()
  const inputs = document.querySelectorAll('.page-item');
  inputs.forEach((elem) => {
      (elem as HTMLElement).blur()
  });
}

function calculateMedian(numbers : number[]) {
  const sortedNumbers = [...numbers].sort((a, b) => a - b);
  const middle = Math.floor(sortedNumbers.length / 2);

  if (sortedNumbers.length % 2 === 0) {
    // Si la lista tiene un número par de elementos, toma el promedio de los dos valores medios
    const middle1 = sortedNumbers[middle - 1];
    const middle2 = sortedNumbers[middle];
    return ((middle1 + middle2) / 2).toFixed(2);
  } else {
    // Si la lista tiene un número impar de elementos, toma el valor del medio
    return sortedNumbers[middle].toFixed(2);
  }
}

function calculateStandardDeviation(numbers : number[]) {
  // Calcular la media (promedio)
  const mean = numbers.reduce((accumulator, currentValue) => accumulator + currentValue, 0) / numbers.length;

  // Calcular la suma de los cuadrados de las diferencias entre cada número y la media
  const squaredDifferences = numbers.map(number => Math.pow(number - mean, 2));

  // Calcular la varianza dividiendo la suma de los cuadrados de las diferencias por la cantidad de números
  const variance = squaredDifferences.reduce((accumulator, currentValue) => accumulator + currentValue, 0) / numbers.length;

  // Calcular la desviación estándar tomando la raíz cuadrada de la varianza
  const standardDeviation = Math.sqrt(variance);

  return standardDeviation.toFixed(2); // Redondear a tres decimales
}

function countSamplesWithMicrobe(list: number[]) {
  return list.filter(v => v && v > 0).length;
}

function calculateValues() {
  resultItems.value = [];
  if (patiens.value === 0 || items.value.length === 0) {
    console.warn("No hay pacientes o items para calcular.");
    return;
  }

  var resultItemsCalculated: any[] = [];

  const keysStartingWithX = Object.keys(items.value[0] || {}).filter(key => key.toLowerCase().startsWith('x'));

  keysStartingWithX.map(item => {
    const key = item;
    const motherEntry = (mother.value as MotherType)[key];

    if (!motherEntry) {
      console.warn(` Clave '${key}' no encontrada en mother`);
      return;
    }

    if (!motherEntry[1]) {
      console.warn(`Clave '${key}' encontrada, pero no tiene valor en [1]`);
      return;
    }
    if (motherEntry && motherEntry[1]) {
      var values_for_item = items.value
        .map(it => it[item])
        .filter(val => typeof val === 'number' && !isNaN(val));

      var average = (
        values_for_item.reduce((acc, val) => acc + val, 0) / values_for_item.length
      ).toFixed(2);

      var median = calculateMedian(values_for_item);
      var stdDeviation = calculateStandardDeviation(values_for_item);
      var count = countSamplesWithMicrobe(values_for_item);


      var dic = {
        name: item,
        count: count,
        countComplete: count + " (" + ((count / patiens.value) * 100).toFixed(2) + "%)",
        relative: average + "%, " + median + "%, " + stdDeviation + "%"
      };

      resultItemsCalculated.push(dic);
    }
  });

  var resultItemsTmp = resultItemsCalculated.sort((a, b) => b.count - a.count);
  modulo.value = Math.floor(resultItemsTmp.length / 20) + 1;
  var inicio = (pagina.value - 1) * 20;
  var fin = pagina.value * 20;

  resultItems.value = resultItemsTmp.slice(inicio, fin);


}



function countCases(site: string) {
  var filtrados = originalItems.value.filter(item => item.diseases === site) 
  return filtrados.length
}

async function contarTodosLosSitios() {
  const sitios = ['cervix', 'uterus', 'rectum', 'vagina', 'orine'];
  for (const sitio of sitios) {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + 'data/' + sitio);
      siteCounts.value[sitio] = response.data.length;
    } catch (error) {
      console.warn(`Error al contar muestras en ${sitio}:`, error);
      siteCounts.value[sitio] = 0;
    }
  }
}


async function loadData(site: string) {
  originalItems.value = [];  // reset inicial
  patiens.value = 0;
  items.value = [];
  resultItems.value = [];

  try {
    const response = await axios.get(import.meta.env.VITE_API_URL + 'data/' + site);

    originalItems.value = response.data.map(item => ({
      ...item,
      diseases: Array.isArray(item.diseases)
        ? item.diseases.map((d: string) => d.trim())
        : item.diseases?.trim()
    }));

    // Actualizar conteo dinámico del sitio actual
    siteCounts.value[site] = originalItems.value.length;

    myList.value = ['RM', 'MALE_FACTOR', 'TUBAL_FACTOR', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'];
    await nextTick();
    numRM.value = countCases('RM');
    numMALE_FACTOR.value = countCases('MALE_FACTOR');
    numTUBAL_FACTOR.value = countCases('TUBAL_FACTOR');
    numENDOMETRIOSIS.value = countCases('ENDOMETRIOSIS');
    numENDOMETRITIS.value = countCases('ENDOMETRITIS');
    numMIOMA.value = countCases('MIOMA');
    numRIF.value = countCases('RIF');
    numUNEXPLAINED.value = countCases('UNEXPLAINED');

    const checks = document.querySelectorAll('.disease-check');
    checks.forEach((elem) => {
      (elem as HTMLInputElement).checked = true;
    });

    updateItems();
    cambiarPagina(1);

  } catch (error) {
    console.error('Error al cargar datos:', error);
  }
}


onMounted(() => {

  axios
    .get(import.meta.env.VITE_API_URL + 'data/all')
    .then((response) => {

      mother.value = response.data
      check()
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
    contarTodosLosSitios()
})


function updateItems() {

  items.value = originalItems.value.filter((item) => {
    const enfermedades = Array.isArray(item.diseases)
      ? item.diseases.map((d: string) => d.trim())
      : [item.diseases?.trim()];
    
    return enfermedades.some((d: string) => myList.value.includes(d));
  });

  patiens.value = items.value.length;

  calculateValues();
}



function filterDisease(disease: string) {
  
  var index = myList.value.indexOf(disease)
  if (index == -1) {
    myList.value.push(disease)
  } else {
    myList.value.splice(index, 1)
  }

  updateItems()
  cambiarPagina(1)
  const inputs = document.querySelectorAll('.form-check-input');
  inputs.forEach((elem) => {
      (elem as HTMLElement).blur()
  });
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
