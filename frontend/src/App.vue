<template>
  <nav class="navbar navbar-expand-lg bg-light">
      <span class="navbar-brand mb-0 h1">ReproMB</span>
      <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
          >
          <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/data/all">Data</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/analytic/all">Analytic</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/Search/all">Search</router-link>
          </li>
        </ul>
    </div>
  </nav>

  <router-view></router-view>
    <!-- Modal de Términos y Condiciones -->
<div
  class="modal fade"
  id="termsModal"
  tabindex="-1"
  aria-labelledby="termsModalLabel"
  aria-hidden="true"
  data-bs-backdrop="static"
  data-bs-keyboard="false"
  ref="modalElement"
>
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="termsModalLabel">Términos y Condiciones de Uso de Datos</h5>
      </div>
      <div class="modal-body" style="max-height: 60vh; overflow-y: auto;">
        <p><strong>Al hacer clic en “Aceptar”, confirmas que has leído y estás de acuerdo con los siguientes términos:</strong></p>
        <ul>
          <li>:)</li>
        </ul>
        <p></p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" @click="aceptarCondiciones">Aceptar</button>
      </div>
    </div>
  </div>
</div>
</template>

<style>
.navbar {
  background-color: #f1fdff !important;
  width: 100vw;
  padding-left: 20px;
}
</style>

<script setup lang="ts">
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import { ref, onMounted, nextTick } from 'vue'
import { Modal } from 'bootstrap'

const modalElement = ref<HTMLElement | null>(null);
let modalInstance: Modal | null = null;

function aceptarCondiciones() {
  if (modalInstance) modalInstance.hide();
}

onMounted(() => {
  if (modalElement.value) {
    modalInstance = new Modal(modalElement.value);
    modalInstance.show();
  }
});

</script>
