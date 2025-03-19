import { defineStore } from 'pinia';

interface User {
  user: string;
  password: string;
  active: string;
  email: string;
}


interface UserResponse {
  code: string;
  status: string;
  message: string;
  result:  User;

}

export const useUserStore = defineStore('users', {

  state: () => ({
      data: null as UserResponse | null,
      login: false,
      loading: false,
      error: null as string | null,
  })
})
