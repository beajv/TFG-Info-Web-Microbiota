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
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    v-model="showSiteCervix"
                    @click="siteFilterCervix"
                    id="inputCervix"
                    type="checkbox"
                    value=""
                    aria-label="..."
                    />
                Cervix
                <span class="badge bg-secondary badge-pill">{{ countCases('Cervix') }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    v-model="showSiteUterus"
                    @click="siteFilterUterus"
                    id="inputUterus"
                    type="checkbox"
                    value=""
                    aria-label="..."
                    />
                Uterus
                <span class="badge bg-secondary badge-pill"> {{ countCases('Uterus') }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    v-model="showSiteRectum"
                    @click="siteFilterRectum"
                    id="inputRectum"
                    type="checkbox"
                    value=""
                    aria-label="..."
                    />
                Rectum
                <span class="badge bg-secondary badge-pill">{{ countCases('Rectum') }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    type="checkbox"
                    @click="siteFilterVagina"
                    v-model="showSiteVagina"
                    id="inputVagina"
                    />
                Vagina
                <span class="badge bg-secondary badge-pill">{{ countCases('Vagina') }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    v-model="showSiteFallopian"
                    @click="siteFilterFallopian"
                    id="inputFallopian"
                    type="checkbox"
                    />
                Fallopian tubes
                <span class="badge bg-secondary badge-pill">{{ countCases('Fallopian tubes') }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <input
                    class="form-check-input me-1"
                    v-model="showSiteOvary"
                    @click="siteFilterOvary"
                    id="inputOvary"
                    type="checkbox"
                    value=""
                    aria-label="..."
                    />
                Ovary
                <span class="badge bg-secondary badge-pill">{{ countCases('Ovary') }}</span>
              </li>
          </ul>
          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">Project</li>
            <li class="list-group-item">
              <input
                  class="form-check-input me-1"
                  type="checkbox"
                  @click.prevent="handleClick"
                  :checked="isChecked"
                  id="inputProject"
                  />
              Granada-Junio
            </li>
          </ul>

          <br />
          <ul class="list-group">
            <li class="list-group-item list-group-item-dark">Diseases</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>
            <li class="list-group-item"> <input class="form-check-input me-1" type="checkbox"/>Granada-Junio</li>



          </ul>


        </div>
      </div>
      <div class="col py-3">
        <h3>Files</h3>
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th>File Name</th>
              <th>Cases</th>
              <th>Site</th>
              <th>Project</th>
              <th>File Size</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id" @click="redirigirFila(item.filename)">
              <td>{{ item.filename }}</td>
              <td>{{ item.report_path }}</td>
              <td>{{ item.site }}</td>
              <td>{{ item.project }}</td>
              <td>{{ item.size }}</td>
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
</style>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router';
const route = useRoute();


interface Item {
  id: number
  filename: string
  report_path: string
  site: string
  project: string
  size: string
}

const items = ref<Item[]>([])
const originalItems = ref<Item[]>([])

const showSiteCervix = ref(false)
const showSiteUterus = ref(false)
const showSiteRectum = ref(false)
const showSiteFallopian = ref(false)
const showSiteOvary = ref(false)
const showSiteVagina = ref(false)

const isChecked = ref(true)

function redirigirFila(id: string) {
 window.location.href = import.meta.env.VITE_API_FILE + id
}


onMounted(() => {
  axios
    .get(import.meta.env.VITE_API_URL)
    .then((response) => {
      originalItems.value = response.data.result
      check()
    })
    .catch((error) => {
      console.error('Error:', error)
    })
})

function countCases(site: String) {
  return originalItems.value
    .filter((item: Item) => item.site === site && !isNaN(parseInt(item.report_path)))
    .reduce((sum: number, item: Item) => sum + parseInt(item.report_path), 0)
}

function check()  {
switch (route.params.site){
    case "cervix":
        showSiteCervix.value = true
        myList.value.push('Cervix')
        break;
    case "uterus":
        showSiteUterus.value = true
        myList.value.push('Uterus')
        break;
    case "rectum":
        showSiteRectum.value = true
        myList.value.push('Rectum')
        break;
    case "vagina":
        showSiteVagina.value = true
        myList.value.push('Vagina')
        break;
    case "fallopian":
        showSiteFallopian.value = true
        myList.value.push('Fallopian tubes')
        break;
    case "ovary":
        showSiteOvary.value = true
        myList.value.push('Uterus')
        break;
}

        updateItems()
}


const myList = ref<string[]>([])
function updateItems() {
  items.value = originalItems.value.filter((item) => myList.value.includes(item.site))
}

function siteFilterCervix() {
  if (!showSiteCervix.value) {
    myList.value.push('Cervix')
  } else {
    myList.value.splice(myList.value.indexOf('Cervix'), 1)
  }
  updateItems()
  const inputCervix = document.getElementById('inputCervix');
  if (inputCervix) {
     inputCervix.blur();
  }  
}

function siteFilterUterus() {
  if (!showSiteUterus.value) {
    myList.value.push('Uterus')
  } else {
    myList.value.splice(myList.value.indexOf('Uterus'), 1)
  }
  updateItems()
  const inputUterus = document.getElementById('inputUterus');
  if (inputUterus) {
     inputUterus.blur();
  }  
}

function siteFilterRectum() {
  if (!showSiteRectum.value) {
    myList.value.push('Rectum')
  } else {
    myList.value.splice(myList.value.indexOf('Rectum'), 1)
  }
  updateItems()
  const inputRectum = document.getElementById('inputRectum');
  if (inputRectum) {
     inputRectum.blur();
  }  
}

function siteFilterVagina() {
  if (!showSiteVagina.value) {
    myList.value.push('Vagina')
  } else {
    myList.value.splice(myList.value.indexOf('Vagina'), 1)
  }
  updateItems()
  const inputVagina = document.getElementById('inputVagina');
  if (inputVagina) {
     inputVagina.blur();
  }  
}

function siteFilterFallopian() {
  if (!showSiteFallopian.value) {
    myList.value.push('Fallopian tubes')
  } else {
    myList.value.splice(myList.value.indexOf('Fallopian tubes'), 1)
  }
  updateItems()
  const inputFallopian = document.getElementById('inputFallopian');
  if (inputFallopian) {
     inputFallopian.blur();
  }  
}

function siteFilterOvary() {
  if (!showSiteOvary.value) {
    myList.value.push('Ovary')
  } else {
    myList.value.splice(myList.value.indexOf('Ovary'), 1)
  }
  updateItems()
  const inputOvary = document.getElementById('inputOvary');
  if (inputOvary) {
     inputOvary.blur();
  }  
}

const handleClick = () => {
  isChecked.value = true
  const inputProject = document.getElementById('inputProject');
  if (inputProject) {
     inputProject.blur();
  }  
}
</script>
