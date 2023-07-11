<template>
  <button @click="clickButton"
    class=" font-acumin bg-buttonGreen w-fit px-6 pt-2 pb-1 text-white text-sm rounded-lg self-end">
    Generar
  </button>
</template>

<script>
export default {
  emits: ['submit'],
  props: {
    color: {
      type: String,
    },
  },
  methods: {
    clickButton() {
      this.$emit("submit");
    },
  },
};
</script>
