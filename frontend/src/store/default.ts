import { defineStore } from 'pinia'

export const useDefaultStore = defineStore('default', {
  state: () => ({
    count: 0,
  }),
})
