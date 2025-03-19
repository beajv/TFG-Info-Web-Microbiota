<template>
    <form class="form-signin" @submit="handleSubmit">
        <h1 class="h3 mb-3 font-weight-normal">Login</h1>
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" v-model="formData.email" class="form-control" placeholder="Email address" required autofocus />
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" v-model="formData.password"  class="form-control" placeholder="Password" autocomplete="on" required />
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>
</template>

<style>
.form-signin {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    padding-top: 200px;
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
.form-signin input[type='email'] {
    margin-bottom: -1px;
    margin-bottom: 10px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}
.form-signin input[type='password'] {
    margin-bottom: 20px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>

<script lang="ts" setup>
import { ref  } from 'vue'
import { useUserStore } from '../../stores/users'

const userStore = useUserStore()
interface FormData {
    email: string;
    password: string;
}

const formData = ref<FormData>({
      email: '',
      password: '',
})


function handleSubmit() {
  if ( formData.value.email == import.meta.env.VITE_EMAIL && formData.value.password == import.meta.env.VITE_PASSWORD ){

    userStore.login = true
  }


}


</script>
