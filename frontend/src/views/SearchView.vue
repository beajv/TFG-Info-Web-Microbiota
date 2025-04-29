<template>
  <div class="search-container">
  <div class="search-box p-4">
    <!-- Encabezado con título, icono e inputs -->
  <div class="search-header d-flex align-items-center justify-content-center mb-4">
    <!-- Parte izquierda: botón + icono -->
    <div class="title-icon d-flex align-items-center me-4">
      <button class="btn btn-success fw-bold fs-4 px-4 py-2 me-3">SEARCH</button>
      <img src="/search-logo1.png" alt="search icon" style="height: 60px;" />
    </div>

  <!-- Parte derecha: inputs -->
  <div class="search-controls d-flex flex-column gap-2">
    <div class="search-wrapper">
      <i class="bi bi-search search-icon"></i>
      <input
        type="text"
        v-model="selectedBacteriaInput"
        placeholder="Buscar bacteria..."
        @input="updateFilteredBacteria"
        class="styled-search-input"
      />
      <ul class="list-group mt-1" v-if="filteredBacteriaList.length > 0">
        <li
          v-for="bacteria in filteredBacteriaList"
          :key="bacteria"
          class="list-group-item list-group-item-action"
          @click="selectBacteria(bacteria)"
          style="cursor: pointer"
        >
          {{ bacteria }}
        </li>
      </ul>
    </div>

    <select v-model="selectedSite" class="styled-search-input">
      <option disabled value="">Selecciona un sitio anatómico</option>
      <option v-for="site in sites" :key="site" :value="site">
        {{ site }}
      </option>
    </select>
  </div>
</div>


    <!--Mostramos lo seleccionado-->
    <div v-if="selectedBacteria && selectedSite" class="mt-4">
      <strong>Seleccionado:</strong> {{ selectedBacteria }} en {{ selectedSite }}
    </div>
  </div>
</div>
    <!-- Tabla de resultados -->
    <div v-if="Array.isArray(abundanciaData) && abundanciaData.length > 0" class="mt-5">
      <h5>Resultados de Abundancia</h5>
      <table class="table table-striped text-center">
        <thead>
          <tr>
            <th>Condition</th>
            <th>Abundancia (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in abundanciaData.filter(r => r.disease !== 'SOP' && r.disease !== 'ARTERIOVENOUS_MALFORMATION')" :key="index">
            <td>{{ row.disease }}</td>
            <td>{{ (row.abundancia).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  
  
</template>

<script setup lang="ts">

import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

// Variables
const selectedBacteriaInput = ref(''); // Lo que escribe el usuario
const selectedBacteria = ref('');       // La bacteria seleccionada
const filteredBacteriaList = ref<string[]>([]); // Lista de sugerencias
const selectedSite = ref('');
const sites = ['cervix', 'uterus', 'rectum', 'vagina', 'orine'];
const abundanciaData = ref<any[]>([]); // Guarda el resultado del backend

const allBacteria = ref<string[]>([]);
const bacteriaToX = ref<Record<string, string>>({});
// Cargar mother al montar el componente


onMounted(async () => {
  const response = await axios.get(`${import.meta.env.VITE_API_URL}data/mother`);
  const mother = response.data;

  const map: Record<string, string> = {};
  for (const key in mother) {
    const genero = mother[key][1]?.trim();
    if (genero) {
      map[genero] = key;  // Lactobacillus → x17
    }
  }

  bacteriaToX.value = map;
  allBacteria.value = Object.keys(map).sort();
});


// Función que actualiza las sugerencias
function updateFilteredBacteria() {
  const query = selectedBacteriaInput.value.toLowerCase();

  if (!allBacteria.value.length) return;  // Evita filtrar si aún no se ha cargado

  filteredBacteriaList.value = allBacteria.value.filter(bacteria =>
    bacteria.toLowerCase().includes(query)
  );
}


// Función que selecciona una bacteria
async function selectBacteria(bacteria: string) {
  selectedBacteria.value = bacteria;
  selectedBacteriaInput.value = bacteria; 
  filteredBacteriaList.value = [];

  // Hacemos la llamada al backend
  if (selectedSite.value && selectedBacteria.value) {
    await getAbundancia(selectedBacteria.value, selectedSite.value);
  }
}

async function getAbundancia(bacteria: string, site: string) {
  try {
    const microId = bacteriaToX.value[bacteria]?.toLowerCase();  // "x17"
    //Prueba
    if (!microId) {
    console.warn(` No se encontró el ID para la bacteria ${bacteria}`);
    abundanciaData.value = [];
    return;
  }
    const response = await axios.get(`${import.meta.env.VITE_API_URL}search_abundancia`, {
      params: {
        columna_micro: microId,
        site: site
      }
    });
    console.log(' Respuesta del backend:', response.data); 

    abundanciaData.value = response.data;
    console.log('Abundancia recibida:', abundanciaData.value);
  } catch (error) {
    console.error('Error al obtener abundancia:', error);
    abundanciaData.value = [];
  }
}

watch(selectedSite, async (newSite) => {
  if (selectedBacteria.value && newSite) {
    console.log("Site cambiado, llamando a getAbundancia...");
    await getAbundancia(selectedBacteria.value, newSite);
  }
});

</script>

<style scoped>
.search-container {
  max-width: 400px;
  margin: 20px auto;
}
.search-wrapper {
  position: relative;
  z-index: 2; /* asegura que esté por encima del select */
}
.search-box .btn-success {
  border-radius: 12px;
  font-size: 20px;
  padding: 12px 32px;
}

.list-group {
  position: absolute;
  z-index: 3;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
}

.search-box {
  border: 5px solid #69B56C;
  border-radius: 10px;
  padding: 80px;
  max-width: 700px;
  margin: 0 auto;
  background-color: white;
}

.table th, .table td {
  vertical-align: middle;
}
.search-container {
  display: flex;
  justify-content: center;
  padding: 30px 0;
}

</style>
