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
            <li class="list-group-item list-group-item-dark d-flex justify-content-between align-items-center">
              Groups
            </li>

            <!-- Grupo 1 -->
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <input
                class="form-check-input me-2"
                type="checkbox"
                @click="toggleGroup(1)"
                :checked="selectedGroups.includes(1)"
              />
              1
            </li>
            <ul v-if="selectedGroups.includes(1)" class="list-group">
              <li class="list-group-item text-muted">MALE_FACTOR</li>
              <li class="list-group-item text-muted">TUBAL_FACTOR</li>
            </ul>

            <!-- Grupo 2 -->
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <input
                class="form-check-input me-2"
                type="checkbox"
                @click="toggleGroup(2)"
                :checked="selectedGroups.includes(2)"
              />
              2
            </li>
            <ul v-if="selectedGroups.includes(2)" class="list-group">
              <li class="list-group-item text-muted">RM</li>
              <li class="list-group-item text-muted">ENDOMETRIOSIS</li>
              <li class="list-group-item text-muted">ENDOMETRITIS</li>
              <li class="list-group-item text-muted">MIOMA</li>
              <li class="list-group-item text-muted">RIF</li>
              <li class="list-group-item text-muted">UNEXPLAINED</li>
            </ul>

            <!-- Grupo 3 -->
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <input
                class="form-check-input me-2"
                type="checkbox"
                @click="toggleGroup(3)"
                :checked="selectedGroups.includes(3)"
              />
              3
            </li>
            <ul v-if="selectedGroups.includes(3)" class="list-group">
              <li class="list-group-item text-muted">No conditions available</li>
            </ul>
          </ul>
          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">Condition</li>
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
    <!-- Contenido Principal -->
    <div class="col py-3">
        <h3>Analytics Section</h3>
        <p>Here you can visualize and analyze selected data.</p>
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


      const inputs = document.querySelectorAll('.disease-check');
      inputs.forEach((elem) => {
           (elem as HTMLInputElement).checked = true
      });
      
      
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}

// Cuando selecciona un grupo debería marcar automáticamente las condiciones correspondientes

function toggleGroup(groupNumber: number) {
  if (selectedGroups.value.includes(groupNumber)) {
    // Si el grupo ya está seleccionado, lo quitamos
    selectedGroups.value = selectedGroups.value.filter(g => g !== groupNumber);
  } else {
    // Si no está seleccionado, lo agregamos
    selectedGroups.value.push(groupNumber);

    // Marcar automáticamente las condiciones asociadas al grupo
    if (groupNumber === 1) {
      filterDisease('MALE_FACTOR');
      filterDisease('TUBAL_FACTOR');
    } else if (groupNumber === 2) {
      filterDisease('RM');
      filterDisease('ENDOMETRIOSIS');
      filterDisease('ENDOMETRITIS');
      filterDisease('MIOMA');
      filterDisease('RIF');
      filterDisease('UNEXPLAINED');
    }
  }
}
/*
function filterBySelectedGroups() {
  console.log("Grupos seleccionados:", selectedGroups.value);

  let filteredData = originalItems.value.filter((item) => {
    if (selectedGroups.value.includes(1) && (item.diseases === "MALE_FACTOR" || item.diseases === "TUBAL_FACTOR")) {
      return true;
    }
    if (selectedGroups.value.includes(2) && ["RM", "ENDOMETRIOSIS", "ENDOMETRITIS", "MIOMA", "RIF", "UNEXPLAINED"].includes(item.diseases)) {
      return true;
    }
    if (selectedGroups.value.includes(3) && !item.diseases) {
      return true;
    }
    return false;
  });

  console.log("Datos filtrados:", filteredData);
}*/


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
