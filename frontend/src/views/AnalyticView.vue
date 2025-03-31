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
import { ref, onMounted, nextTick, reactive} from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router';



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



function getCount(disease: string) {
  return eval('num' + disease);
}
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

function toggleDisease(disease: string) {
  const index = myList.value.indexOf(disease);
  if (index === -1) {
    myList.value.push(disease);
  } else {
    myList.value.splice(index, 1);
  }
  updateItems();
}
/*
function updateGroupAssignments() {
  // Actualizamos los grupos seleccionados para reflejar los usados actualmente
  selectedGroups.value = [...new Set(diseases.value.map(d => d.group).filter(g => g > 0))];

  // Si ya hay un grupo seleccionado, actualizamos myList para reflejar las enfermedades de ese grupo
  if (selectedGroups.value.length === 1) {
    const selected = selectedGroups.value[0];

    const selectedDiseases = diseases.value
      .filter(d => d.group === selected)
      .map(d => d.name);

    myList.value = [...selectedDiseases];

    // Esto es clave para que los ticks se actualicen visualmente
    /*nextTick(() => {
      selectedDiseases.forEach(disease => {
        const checkbox = document.getElementById('check_' + disease) as HTMLInputElement;
        if (checkbox) checkbox.checked = true;
      });
    });

    updateItems();
  }
}*/
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

// Cuando selecciona un grupo debería marcar automáticamente las condiciones correspondientes
/*
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
}*/
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
/*
function handleGroupSelection(event: Event) {
  const selected = parseInt((event.target as HTMLSelectElement).value);
  if (!selected) return;

  if (!selectedGroups.value.includes(selected)) {
    selectedGroups.value.push(selected);
  }

  if (selected === 1) {
    filterDisease('MALE_FACTOR');
    filterDisease('TUBAL_FACTOR');
  } else if (selected === 2) {
    filterDisease('RM');
    filterDisease('ENDOMETRIOSIS');
    filterDisease('ENDOMETRITIS');
    filterDisease('MIOMA');
    filterDisease('RIF');
    filterDisease('UNEXPLAINED');
  } else if (selected === 3) {
    // Este grupo representa sin condición
    myList.value = myList.value.filter(val =>
      !['RM', 'MALE_FACTOR', 'TUBAL_FACTOR', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'].includes(val)
    );
    updateItems();
  }
}

function handleGroupSelection(event: Event) {
  const selected = Array.from((event.target as HTMLSelectElement).selectedOptions).map(option =>
    parseInt(option.value)
  );
  selectedGroups.value = selected;

  myList.value = [];

  const diseaseGroups: { [key: number]: string[] } = {
    1: ['MALE_FACTOR', 'TUBAL_FACTOR'],
    2: ['RM', 'ENDOMETRIOSIS', 'ENDOMETRITIS', 'MIOMA', 'RIF', 'UNEXPLAINED'],
  };

  // Reset checkboxes visuales
  const inputs = document.querySelectorAll('.disease-check') as NodeListOf<HTMLInputElement>;
  inputs.forEach(elem => (elem.checked = false));

  selectedGroups.value.forEach(group => {
    if (diseaseGroups[group]) {
      diseaseGroups[group].forEach(disease => {
        if (!myList.value.includes(disease)) {
          myList.value.push(disease);

          const checkbox = document.getElementById('check_' + disease) as HTMLInputElement;
          if (checkbox) checkbox.checked = true;
        }
      });
    } else if (group === 3) {
      const known = Object.values(diseaseGroups).flat();
      const noCondition = originalItems.value.filter(item => !known.includes(item.diseases));
      const unique = [...new Set(noCondition.map(i => i.diseases))].filter(Boolean);
      myList.value.push(...unique);
    }
  });

  updateItems();
}
*/
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
    const checks = document.querySelectorAll('.disease-check') as NodeListOf<HTMLInputElement>;
    checks.forEach(c => {
      console.log("Checkbox ID:", c.id, " Value:", c.value);
    });
  });

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