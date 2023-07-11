<template lang="">
    <div class="flex flex-col mb-4">
        <label for="textGen" class="text-textGray text-2xl mt-2 font-bold">
        Texto
        </label>
        <!-- <span class=" text-textGray italic text-sm mb-2">en inglés</span> -->
        <textarea v-model="promptText" maxlength="100" placeholder="Si necesita, escriba aquí sus observaciones" class=" bg-gray-200 rounded mb-2 px-4 py-2" type="text" name="text-gen"
        rows="2" id="textGen" />
        <span class=" text-textGray italic text-sm">{{promptText.length}}/100 carácteres</span>
        <div v-if="promptText.length > 0" class="flex gap-4 justify-end">
            <restore-button @restore="restore"/>
            <submit-button @submit="submitText" />
        </div>
    </div>
</template>
<script>
import SubmitButton from '../common/submitButton.vue'
import RestoreButton from '../common/restoreButton.vue'
export default {
    data() {
        return {
            promptText: ''
        }
    },
    components: {
        SubmitButton,
        RestoreButton
    },
    methods: {
        submitText() {
            const url = 'https://development.arcaxo.com/api/genimg'
            const myHeaders = new Headers()
            myHeaders.append("Content-Type", "application/json")
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
            this.promptText = ''
        }
    }
}
</script>