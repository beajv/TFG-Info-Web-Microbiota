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
            <router-link class="nav-link" to="/analytic/all">Analytics</router-link>
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
        <h5 class="modal-title" id="termsModalLabel">TERMS AND CONDITIONS OF DATA USE</h5>
      </div>
      <div class="modal-body" style="max-height: 60vh; overflow-y: auto;">
        <p><strong>ReproMB – Microbial Atlas for Female Reproductive Health</strong></p>
        <p>By accessing, using, or downloading any portion of the ReproMB platform ("Platform"), you acknowledge and accept the following Terms and Conditions and agree to abide by them in full.</p>
        
        <h6>1. Use and Scope of the Platform</h6>
        <p>ReproMB provides access to visualized microbiome data from the female reproductive tract and gut, including associated metadata (e.g., clinical status, sample origin, age range), and derived metrics (e.g., community structures, diversity indices). These data are intended solely for non-commercial, academic, and research purposes.</p>
        
        <h6>2. User Responsibilities</h6>
        <ul>
          <li><strong>Eligibility:</strong> You confirm that you are at least 18 years old and legally authorized to agree to and comply with these terms.</li>
          <li><strong>Data Handling:</strong> The data must only be used within the bounds of this Platform and its stated objectives. Redistribution, external storage, or integration with other datasets is prohibited without explicit written consent from the ReproMB team.</li>
          <li><strong>Privacy and Security:</strong> You agree to handle the data in a way that upholds data protection standards in accordance with applicable laws and best practices. This includes implementing technical, administrative, and physical safeguards to prevent unauthorized access or misuse. If data are stored on portable devices, encryption complying with recognized standards (e.g., FIPS 140-2 or EU equivalents) must be employed.</li>
          <li><strong>Non-Commercial Use:</strong> The data may not be sold, leased, or used for profit-generating purposes. </li>
          <li><strong>Non-Identification Clause:</strong> You must not attempt to identify, contact, or re-identify any individual whose information is part of the Platform. Nor may you combine the data with external sources to infer identities. If identification occurs or is suspected, you must notify the ReproMB team immediately.</li>
          <li><strong>Academic Attribution:</strong> You are encouraged to publish and present findings based on ReproMB data, provided proper citation is given to the ReproMB platform and associated contributors, following standard scientific practices.</li>
        </ul>
        
        <h6>3. Breach Notification and Remedies</h6>
        <p>Reporting Obligations:Any actual or suspected breach must be reported to the ReproMB team (contact: igarach@ugr.es ) within two (2) business days of its discovery. Reports should include:</p>
        <ul>
          <li>Nature of the breach (e.g., unauthorized access or misuse)</li>
          <li>Specific data involved</li>
          <li>Individuals involved or affected</li>
          <li>Mitigation measures taken</li>
          <li>Corrective steps implemented to prevent recurrence</li>
        </ul>
        <p>You are required to cooperate in any investigations and maintain regular communication until the issue is resolved.
          Liability: You agree to indemnify and hold harmless the ReproMB project team, its affiliated institutions (e.g., University of Granada, University of Tartu), and collaborators from any claims or losses resulting from your use of the data in violation of these terms.</p>

        <h6>4. Name and Branding Usage</h6>
        <p>You may not use the names, logos, or affiliations of the ReproMB project, its research team, or collaborating institutions in publicity or promotional material without prior written approval.</p>
        
        <h6>5. Disclaimers and Limitations</h6>
        <p>The ReproMB data and visualizations are provided “as is” without warranties of any kind, including merchantability, accuracy, or fitness for a specific purpose. The Platform does not guarantee that use of the data will be free from intellectual property claims by third parties.
          To the maximum extent permitted by law, you assume full responsibility for any consequences arising from the use, storage, or handling of the data. ReproMB and its affiliates are not liable for any damages, losses, or claims related to your use of the Platform, except in cases of willful misconduct or gross negligence by the ReproMB team.</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" @click="aceptarCondiciones">Accept</button>
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
