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
        </ul>
    </div>
  </nav>
  <router-view></router-view>
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
</script>
