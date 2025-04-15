<template>
    <div class="container mt-5">
      <h2 class="mb-4 text-center">Microbiome Search</h2>
  
      <div class="mb-4">
        <input
          v-model="searchTerm"
          class="form-control"
          type="text"
          placeholder="Search for a microbe, disease, or sample ID..."
        />
      </div>
  
      <div v-if="filteredResults.length > 0">
        <h5>Results:</h5>
        <ul class="list-group">
          <li v-for="(item, index) in filteredResults" :key="index" class="list-group-item">
            {{ item }}
          </li>
        </ul>
      </div>
      <div v-else-if="searchTerm" class="text-muted">No results found.</div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  
  const searchTerm = ref('')
  const allItems = ref<string[]>([
    'Lactobacillus',
    'Gardnerella',
    'Bifidobacterium',
    'ENDOMETRIOSIS',
    'MIOMA',
    'UNEXPLAINED',
    'SAMPLE_001',
    'SAMPLE_002'
  ])
  
  const filteredResults = computed(() =>
    allItems.value.filter(item =>
      item.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  )
  </script>
  