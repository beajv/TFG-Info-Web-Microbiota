<template>
    <Upload v-if="userStore.login" />
    <Login v-else />
</template>

<script lang="ts" setup>
import Upload from '../components/forms/Upload.vue'
import Login from '../components/forms/Login.vue'

import { useUserStore } from '../stores/users'
const userStore = useUserStore()


</script>
