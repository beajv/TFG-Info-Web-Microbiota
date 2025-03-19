
<!--VERSIÓN INICIAL DE VICENTE

template>
  <div id="uno">
    <img src="../../assets/main.png" class="carta" />
  </div>
  <div id="dos">
    <a href="/data/all">
      <img src="../../assets/vagina.png"  />
    </a>
  </div>
</template> 


.carta {
  position: absolute;
  float: left;
}

#uno {
  position: absolute;
  left: 600px;
  top: 150px;
  transition: opacity 0.3s ease;
  float: left;
}


#dos {
  position: absolute;
  left: 600px;
  top: 150px;
  border-color: red;
  border: 1px solid #000;
  z-index: 2;
  transition: box-shadow 0.3s, transform 0.3s;
  background-color: transparent;
  opacity: 0;
  float: left;
}





</style>


<script lang="ts" setup>
</script>
-->

<!--VERSIÓN CON IMAGEN DE VICENTE PUNTITOS--> 

<!--template>
  
  <div id="uno">
    <img src="../../assets/main.png" class="carta" />
  </div>

  <div id="dos" @mouseenter="hover = true" @mouseleave="hover = false">
    <a href="/data/all">
      <img src="../../assets/vagina_nueva.png" class="vagina" :class="{ visible: hover }" />
    </a>
  </div>
</template>

<style>
/* Imagen principal */
.carta {
  position: absolute;
  float: left;
}

/* Contenedor de la imagen principal */
#uno {
  position: absolute;
  left: 600px;
  top: 150px;
  transition: opacity 0.3s ease;
  float: left;
}

/* Contenedor de la imagen de la vagina */
#dos {
  position: absolute;
  left: 745px;
  top: 175px;
  z-index: 2;
  transition: box-shadow 0.3s, transform 0.3s;
  background-color: transparent;
  opacity: 1;
  float: left;
}

/* Imagen de la vagina (resaltado) */
.vagina {
  opacity: 0; /* Inicialmente invisible */
  transition: opacity 0.3s ease-in-out;
  
}

/* Se vuelve visible al pasar el ratón */
.vagina.visible {
  opacity: 1;
}
</style>

<script lang="ts" setup>
import { ref } from "vue";

const hover = ref(false);
</script>
-->



<!-- VERSIÓN SÓLO ILUMINA APARATO REPRODUCTOR -->
 
<!--template>
  <div id="svg-container">
    <svg 
      v-if="svgContent" 
      v-html="svgContent" 
      @mouseover="resaltarParte" 
    ></svg>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';

// Estado para almacenar el contenido del SVG
const svgContent = ref<string | null>(null);

// Objeto para almacenar el color original de cada parte
const coloresOriginales = ref<Map<HTMLElement, string>>(new Map());

// Cargar el archivo SVG dinámicamente al montar el componente
onMounted(async () => {
  try {
    const response = await fetch('/src/assets/main-resaltado.svg');  // Ruta del archivo
    svgContent.value = await response.text();
  } catch (error) {
    console.error('Error cargando el SVG:', error);
  }
});

// Función para resaltar una parte específica del SVG
const resaltarParte = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (target.tagName === 'path' || target.tagName === 'polygon') {
    // Guardamos el color original antes de cambiarlo
    if (!coloresOriginales.value.has(target)) {
      coloresOriginales.value.set(target, target.style.fill || ''); // Usamos el color actual o vacío
    }

    target.style.fill = 'rgba(255, 0, 0, 0.5)'; // Cambia el color al pasar el mouse
    // Agregar evento específico para el "mouseleave" del mismo elemento
    target.addEventListener('mouseleave', () => {
      // Restauramos el color original
      const colorOriginal = coloresOriginales.value.get(target);
      target.style.fill = colorOriginal || ''; // Si no hay color guardado, lo dejamos vacío
    });
  }
};
</script>

<style>
#svg-container {
  position: absolute;
  left: 600px; /* Misma posición que antes */
  top: 150px;
  width: 1000px;  /* Ajusta al tamaño deseado */
  height: 1000px;
}

svg {
  width: 100%;
  height: 100%;
  display: block;
}
</style>

-->

<!-- VERSIÓN SÓLO ILUMINA APARATO REPRODUCTOR no pone etiqueta -->

<template>
  <div id="svg-container">
    <svg 
      v-if="svgContent" 
      v-html="svgContent" 
      @mouseover="resaltarParte"
      role="img" 
      aria-labelledby="titulo-svg descripcion-svg"
    ></svg>
    <div style="display: none">
      <h1 id="titulo-svg">Diagrama del aparato reproductor femenino</h1>
      <p id="descripcion-svg">Este diagrama interactivo muestra las principales partes del aparato reproductor femenino. Pase el ratón sobre cada zona para resaltarla.</p>
    </div>
  </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue';
/** Parte de arriba para poder añadir texto a la imagen sin que se muestre para mejorar accesibilidad
 * role="img": Indica que el SVG es una imagen.
 * aria-labelledby: Asocia la imagen con los elementos de texto ocultos que describen su contenido.
 * Elemento oculto <div>: Proporciona el título y la descripción sin mostrarlos visualmente.
 */
// Estado para almacenar el contenido del SVG

const svgContent = ref<string | null>(null);

// Objeto para almacenar el color original de cada parte
const coloresOriginales = ref<Map<HTMLElement, string>>(new Map());

// Cargar el archivo SVG dinámicamente al montar el componente
onMounted(async () => {
  try {
    const response = await fetch('/src/assets/main-resaltado.svg');  // Ruta del archivo
    svgContent.value = await response.text();
  } catch (error) {
    console.error('Error cargando el SVG:', error);
  }
});

// Función para resaltar una parte específica del SVG
const resaltarParte = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (target.tagName === 'path' || target.tagName === 'polygon') {
    // Guardamos el color original antes de cambiarlo
    if (!coloresOriginales.value.has(target)) {
      coloresOriginales.value.set(target, target.style.fill || ''); // Usamos el color actual o vacío
    }

    target.style.fill = 'rgba(255, 0, 0, 0.5)'; // Cambia el color al pasar el mouse
    // Agregar evento específico para el "mouseleave" del mismo elemento
    target.addEventListener('mouseleave', () => {
      // Restauramos el color original
      const colorOriginal = coloresOriginales.value.get(target);
      target.style.fill = colorOriginal || ''; // Si no hay color guardado, lo dejamos vacío
    });
  }
};
</script>

<style>
#svg-container {
  position: absolute;
  left: 600px; /* Misma posición que antes */
  top: 150px;
  width: 1000px;  /* Ajusta al tamaño deseado */
  height: 1000px;
}

svg {
  width: 100%;
  height: 100%;
  display: block;
}
</style>







