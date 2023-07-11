<template>

  <body>
    <header class="relative flex  w-full h-16 noPrint">
      <img class=" my-2 mx-4" src="/res/hader_logo.svg" alt="">
    </header>

    <div v-show="loading" class="h-[83vh] flex flex-col justify-center items-center noPrint">
      <div class="flex justify-center items-center space-x-2 ">
        <div class="spinner-border animate-spin inline-block w-16 h-16 border-4 rounded-full text-purple-500"
          role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <p class=" text-sm text-gray-500 italic my-6">Inspirándome...</p>
    </div>

    <main v-show="!loading" class="flex flex-col lg:flex-row w-full items-center font-acumin 2xl:px-48 2xl:my-24">
      <div class=" w-full lg:w-1/2 xl:w-2/3 px-6 lg:p-8 lg:px-16 overflow-y-auto noPrint">
        <div class="flex flex-col xl:flex-row py-12 md:py-8 xl:py-0 justify-center items-center gap-4">
          <h1 class="text-4xl text-textGray lg:w-96 font-acuminBold xl:border-r-2 xl:pr-6 xl:my-8 xl:border-r-gray-600">
            The Daphne Algorithm
          </h1>
          <p class=" text-textGray xl:w-11/12">
            El IA está entrenado con el estilo artístico de Daphne Anastassiou. Puedes agregar una
            descripción de contenido de manera escrita, por voz o una imágen o fotografía; a partir de allí, se
            desarrolla una pieza única dentro de los parámetros del estilo.
          </p>
        </div>
        <textComp @loading="loadState" @response="loadResponse" />
        <div class="flex flex-col xl:flex-row gap-12">
          <musicPlayer @loading="loadState" @response="loadResponse"
            backendEndpoint="http://137.184.177.230:8080/uploader" />
          <!-- <pictureComp @loading="loadState" @response="loadResponse" /> -->
        </div>
      </div>
      <div class="flex items-center justify-center lg:w-1/2 xl:w-1/3 p-12 lg:py-0">
        <artComp :imgSrc="imgSrc" />
      </div>
    </main>
    <footer class="flex w-full h-16 justify-end font-acumin fixed bottom-0">
      <p class=" self-center text-white font-bold px-24">
        Creado por:
      </p>
    </footer>
  </body>
</template>

<script>
import textComp from '../components/input/textComp.vue'
import musicPlayer from '../components/input/audioComp.vue'
import pictureComp from '../components/input/pictureComp.vue'
import SubmitButton from '../components/common/submitButton.vue'
import artComp from '../components/output/artComp.vue'

export default {
  components: {
    musicPlayer,
    textComp,
    SubmitButton,
    pictureComp,
    artComp
  },
  data() {
    return {
      loading: false,
      imgSrc: null,
      promptText: null,
      userAudio: null
    }
  },
  methods: {
    loadState() {
      this.loading = !this.loading
    },
    loadResponse(e) {
      const response = JSON.parse(e)
      // this.imgSrc = 'http://137.184.177.230' + response.path
      this.imgSrc = response.path
    },
  }
}
</script>

<style>
@media print {
  .noPrint {
    display: none;
  }
}

header {
  background-image: url('/res/banner.png');
}

footer {
  background-image: url('/res/banner footer.png');
}
</style>