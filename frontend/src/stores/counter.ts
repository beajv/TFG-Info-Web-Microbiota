import { defineStore } from 'pinia';


export const useCounterStore = defineStore('counter', {

    state: () => ({
        index: 0,
    }),

    actions: {
        changeIndex( value: number ) {
            this.index += value;
        }

    }
})

