<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-light">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-5 min-vh-100">
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">Taxon level</li>
            <li class="list-group-item">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  :checked="isChecked"
                  id="inputProject"
                  />
              Genus
            </li>
            <li class="list-group-item">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  disabled
                  />
              Species
            </li>
          </ul>
          <br />
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
            <li class="list-group-item list-group-item-dark">Project</li>
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
            <li class="list-group-item list-group-item-dark">Diseases</li>
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
        <table class="table table-hover">
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
<td>{{ (mother as MotherType)[item.name.toUpperCase()][1] }}</td>
              <td>
<a :href="'https://www.ebi.ac.uk/ena/browser/view/Taxon:' + (mother as MotherType)[(item.name as string).toUpperCase()][2]"
     target="_blank"
     rel="noopener noreferrer">
    {{ (mother as MotherType)[(item.name as string).toUpperCase()][2] }}
  </a>


</td>
<td>{{ (mother as MotherType)[item.name.toUpperCase()][3] }}</td>
              <td>{{ item.countComplete }}</td>
              <td>{{ item.relative }}</td>
            </tr>
          </tbody>
        </table>
<nav aria-label="Page navigation example">
  <ul class="pagination justify-content-center">
    <li class="page-item"  :class="{ 'disabled': pagina === 1 }" v-if="patiens">
      <a class="page-link" href="#"  @click="cambiarPagina(pagina-1)">Previous</a>
    </li>
    <li v-for="i in modulo" :key="i" class="page-item " :class="{ 'active': i === pagina }" @click="cambiarPagina(i)"><a class="page-link" href="#">{{ i }}</a></li>
    <li class="page-item">
      <a class="page-link" v-if="patiens" :class="{ 'disabled': pagina === modulo }" href="#" @click="cambiarPagina(pagina+1)">Next</a>
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
</style>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
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

function countDistinctValues(list : number[]) {
  // Use a Set to store distinct values
  var distinctValues = new Set();

  // Iterate through the list and add values distinct from 0 or -1 to the Set
  for (var i = 0; i < list.length; i++) {
    if (list[i] !== 0 && list[i] !== -1) {
      distinctValues.add(list[i]);
    }
  }

  // Return the count of distinct values found
  return distinctValues.size;
}

function calculateValues() {
      resultItems.value = [] 
      if (patiens.value !== 0) {
      var resultItemsCalculated: any[] = []; 

      const keysStartingWithX = Object.keys(items.value[0]).filter(key => key.startsWith('x'));
      keysStartingWithX.map(item=> {
         if( (mother.value as MotherType)[ item.toUpperCase() ][1] ){ 

         var values_for_item: any[] = [];
         for( var i = 0; i < items.value.length; i++){
            values_for_item.push(items.value[i][item])
         }
         var average = (values_for_item.map(num => num).reduce((accumulator, currentValue) => accumulator + currentValue, 0) / values_for_item.length).toFixed(2);

         var median = calculateMedian(values_for_item)
         var stdDeviation = calculateStandardDeviation(values_for_item)           

         var count = countDistinctValues(values_for_item)

         var dic = { 
            name: item,
            count: count,
            countComplete: count + " (" + ((count/patiens.value) * 100).toFixed(2) + "%)",
            relative: average + "%, " +  median + "%, " + stdDeviation + "%"
         }
         
         resultItemsCalculated.push(dic) 

         }

      })
      
      var resultItemsTmp = resultItemsCalculated.sort((a, b) => b.count - a.count);  
      modulo.value = Math.floor(resultItemsTmp.length / 20) + 1
      var inicio = (pagina.value - 1) * 20
      var fin = pagina.value * 20

      resultItems.value =  resultItemsTmp.slice(inicio, fin)
      
      }
}


function countCases(site: string) {
  var filtrados = originalItems.value.filter(item => item.diseases === site) 
  return filtrados.length
}

function loadData(site: string){

  originalItems.value = []
  updateItems()
  axios
    .get(import.meta.env.VITE_API_URL + site)
    .then((response) => {

      originalItems.value = response.data
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


      const inputs = document.querySelectorAll('.disease-check');
      inputs.forEach((elem) => {
           (elem as HTMLInputElement).checked = true
      });
      
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
    cambiarPagina(1)
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

})



function updateItems() {
  items.value = originalItems.value.filter((item) => myList.value.includes(item.diseases))
  patiens.value = items.value.length
  calculateValues()
}

function filterDisease(disease: string) {
  
  var index = myList.value.indexOf(disease)
  console.log(index)
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
