<template lang="">
  <button @click="clickButton"
    class=" font-acumin bg-red-600 w-fit px-4 pt-2 pb-1 text-white text-sm rounded-lg self-end">
    Reestablecer
  </button>
</template>
<script>
export default {
    methods: {
        clickButton() {
            this.$emit('restore')
        }
    }
}
</script>