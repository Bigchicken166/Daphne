<template lang="">
    <div class="flex w-full">
        <div class="flex flex-col items-start justify-start w-full">
            <h4 class=" text-2xl text-textGray font-bold my-3">
                Imagen
            </h4>
            <div class="flex mx-auto">
                <div class="bg-placeHolderGray rounded h-28 w-28">
                    <img v-if="imgSrc" :src="imgSrc" class="rounded object-cover h-full" />
                </div>
                <div class="mx-4">
                <p class=" text-textGray my-2">Sube la imagen que deseas generar</p>
                <div class=" flex justify-evenly">
                    <label for="fileSubmit"
                    class="bg-placeHolderGray text-textGray font-bold rounded px-2 pt-2 pb-1 cursor-pointer">
                    Examinar
                    </label>
                    <input @change="onFile" class="hidden" type="file" name="fileSubmit" id="fileSubmit"
                    accept="image/png, image/jpeg">
                </div>
                </div>
            </div>
            <div v-show="imgSrc.length > 0" class="flex gap-4 justify-end">
                <restore-button @restore="restore"/>
                <submit-button @submit="sendData"/>
            </div>
        </div>
    </div>
</template>

<script>
import SubmitButton from '../common/submitButton.vue';
import RestoreButton from '../common/restoreButton.vue'
export default {
    data() {
        return {
            imgSrc: '',
        }
    },
    components: {
        SubmitButton,
        RestoreButton
    },
    methods: {
        sendData() {
            const url = 'http://137.184.177.230:8080/api/genimg'
            const myHeaders = new Headers()
            const imgExtension = this.imgSrc.split(';')[0].split(':')[1]
            const formData = new FormData()

            myHeaders.append("Content-Type", imgExtension)
            formData.append('file', this.imgSrc)

            const raw = JSON.stringify({
                "frase": this.promptText
            });

            const options = {
                method: 'POST',
                mode: 'cors',
                headers: myHeaders,
                body: raw
            }

            this.$emit("loading")

            fetch(url, options)
                .then(response => response.text())
                .then(result => {
                    this.$emit("response", result)
                    this.$emit("loading")
                })
                .catch(error => console.log('error', error));
        },
        restore() {
            this.imgSrc = ''
        },
        onFile(e) {
            const files = e.target.files
            if (!files.length) return

            const reader = new FileReader()
            reader.readAsDataURL(files[0])
            reader.onload = () => (this.imgSrc = reader.result)
        },
    }
}
</script>
<style lang="">
    
</style>