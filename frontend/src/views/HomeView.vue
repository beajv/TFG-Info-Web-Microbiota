<template>
  <div class="background-image">
  </div>
  <div class="contenedor1">
    <div class="card" style="width: 25rem">
      <div class="card-body">
        <h5 class="card-title">Data Portal Summary</h5>
        <h6 class="card-subtitle mb-2 text-muted">Data Release 1.0 - September 20, 2023</h6>
        <div class="row justify-content-start">
          <div class="col-4">PROJECT</div>
          <div class="col-4">SITES</div>
        </div>
        <div class="row justify-content-start">
          <div class="col-4">1</div>
          <div class="col-4">6</div>
        </div>
        <br />
        <div class="row justify-content-start">
          <div class="col-4">MICROBE</div>
          <div class="col-4">CONDITIONS</div>
        </div>
        <div class="row justify-content-start">
          <div class="col-4">33</div>
          <div class="col-4">-</div>
        </div>
      </div>
    </div>
  </div>

  <div class="contenedor2">
    <Endomap />
  </div>

  <div class="contenedor3">
    <BarChart />
  </div>

  <div class="contenedor4">
    <center>
      <h3>ReproMB Atlas</h3>
      <p>
      The ReproMB is a robust data-driven platform that allows researchers and bioinformaticians to search
      and download data for analysis.
      </p>
    </center>
  </div>
</template>

<script lang="ts" setup>
import BarChart from '../components/charts/BarChart.vue'
import Endomap from '../components/home/Endomap.vue'


</script>

<style>
.body {
  width: 500px; /* Ancho de la página en píxeles */
  margin: 0; /* Elimina los márgenes predeterminados del cuerpo del documento */
  padding: 0; /* Elimina el relle */
  font-family: Arial, Helvetica, sans-serif;
}

.background-image {
  background: url('../assets/fondo.png');
  width: 1425px;
  height: 600px; /* Altura de la página en píxeles */
  background-repeat: repeat-x;
  background-size: cover;
}

.contenedor1 {
  width: 200px;
  height: 200px;
  position: absolute;
  left: 90px;
  top: 320px;
}

.contenedor2 {
  
}

.contenedor3 {
  width: 400px;
  height: 600px;
  position: absolute;
  left: 1000px;
  top: 340px;
}

.contenedor4 {
  width: 850px;
  height: 95px;
  position: absolute;
  left: 300px;
  top: 660px;
  bottom: 10px;
}

</style>