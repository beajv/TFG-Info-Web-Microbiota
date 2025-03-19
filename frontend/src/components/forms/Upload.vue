<template>
    <form class="form-signin">
        <h1 class="h3 mb-3 font-weight-normal">Upload File</h1>
        <label for="inputDOI" class="sr-only">DOI</label>
        <input type="text" id="inputDOI" class="form-control" placeholder="DOI" required />
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required />
        <label for="inputFile" class="sr-only">Site</label>
        <select class="form-select" aria-label="Default select example">
            <option selected>Cervix</option>
            <option value="1">Uterus</option>
            <option value="2">Rectum</option>
            <option value="3">Vagina</option>
            <option value="3">Fallopian tubes</option>
            <option value="3">Ovary</option>
        </select>
        <label for="inputProject" class="sr-only">Project</label>
        <select
            class="form-select"
            id="selectProject"
            aria-label="Default select example"
            v-model="selectedOption"
            :disabled="isChecked"
        >
            <option value="0" :selected="isChecked">Granada-Junio</option>
        </select>
        <div class="form-check">
            <input
                class="form-check-input d-none"
                type="checkbox"
                value=""
                id="flexCheckDefault"
                v-model="isChecked"
                @change="handleChange"
            />
            <label class="form-check-label d-none" for="flexCheckDefault"> New Project </label>
        </div>
        <input
            type="text"
            ref="inputNewProject"
            id="inputNewProject"
            class="form-controli d-none"
            placeholder="New Project"
            :disabled="!isChecked"
        />

        <label for="inputFile" class="sr-only">File</label>
        <input type="file" id="inputFile" class="form-control" required />
        <div class="position-relative">
            <button class="btn btn-lg btn-primary position-absolute start-0" type="submit">Submit</button>
            <button class="btn btn-lg btn-primary position-absolute end-0" @click="handleLogOut" >Log Out</button>
        </div>
    </form>
</template>

<style>
input,
textarea,
fieldset,
select,
button {
    margin: 5px 0 10px 0;
}

.form-signin {
    width: 100%;
    max-width: 900px;
    padding: 15px;
    padding-top: 100px;
    margin: 0 auto;
}

.form-signin .form-control {
    position: relative;
    box-sizing: border-box;
    height: auto;
    padding: 10px;
    font-size: 16px;
}
.form-signin .form-control:focus {
    z-index: 2;
}
</style>

<script lang="ts" setup>
import { ref } from 'vue'
import { useUserStore } from '../../stores/users'
const userStore = useUserStore()

const isChecked = ref(false)
const selectedOption = ref('0')
const previousSelectedOption = ref('0')
const inputNewProject = ref<HTMLInputElement | null>(null)

const handleChange = (): void => {
    if (isChecked.value) {
        previousSelectedOption.value = selectedOption.value
        inputNewProject.value?.focus()
    } else {
        const selectProject = document.getElementById('selectProject')
        if (selectProject) {
            selectProject.focus()
        }
    }
}

function handleLogOut() {
   userStore.login = false
}
</script>
