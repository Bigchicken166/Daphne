<template lang="">
    <div class="flex flex-col w-fit h-fit">
        <div class="flex items-center justify-center bg-gray-300 rounded-lg w-80 h-80 m-auto lg:w-96 lg:h-96 overflow-hidden">
            <span v-if="!imgSrc" class=" text-textGray">Introduce un enunciado para generar un arte</span>
            <img v-else :src="imgSrc" alt="">
        </div>
        <div v-if="imgSrc" class="flex gap-4 self-end noPrint">
        <button @click="clickedDownload" 
            class="bg-buttonBlue w-fit px-6 pt-2 pb-1 text-white text-2xl font-bold rounded-lg my-4 self-end noPrint"
            type="button">
            Ampliar
        </button>
        <!-- Content -->
        <button @click="print"
            class=" bg-buttonBlue w-fit px-6 pt-2 pb-1 text-white text-2xl font-bold rounded-lg my-4 self-end noPrint"
            type="button">
            Imprimir
        </button>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        imgSrc: String,
    },
    methods: {
        sendSave() {
            this.$emit("save");
        },
        clickedDownload() {
            const link = document.createElement('a')
            link.href = this.imgSrc
            link.setAttribute('download', 'file.png')
            link.setAttribute('target', '_blank')
            document.body.appendChild(link)
            link.click()
        },
        print() {
            window.print()
        }
    }
}
</script>