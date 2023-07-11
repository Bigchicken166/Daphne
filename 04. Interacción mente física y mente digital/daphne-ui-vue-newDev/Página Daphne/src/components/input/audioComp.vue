<template>
    <div class="flex flex-col">
        <h4 class=" text-2xl text-textGray font-bold my-3">
            Audio
        </h4>
        <div class="flex justify-center gap-6">
            <div class="hidden lg:flex justify-center items-center rounded-full bg-placeHolderGray h-24 w-24 px-8">
                <img class=" w-12 h-12 z-10" src="/res/icon/music.svg" alt="">
            </div>
            <div
                class="flex flex-col justify-center bg-placeHolderGray rounded-xl w-[300px] gap-2 pb-4 overflow-hidden">
                <span v-show="!recordedAudio" class="mx-auto mt-4 px-4 text-center text-textGray">
                    {{ instructionMessage }}
                </span>
                <div v-show="recordedAudio" class="w-fit">
                    <figure>
                        <audio controls :src="recordedAudio" type="audio/mpeg" class="mx-auto">
                            Your browser does not support the
                            <code>audio</code> element.
                        </audio>
                    </figure>
                </div>
                <div class="flex items-center gap-4 self-center">
                    <div>
                        <icon-button :class="buttonClass" v-if="recording" name="stop" @click="toggleRecording" />
                        <icon-button :class="buttonClass" v-else name="mic" @click="toggleRecording" />
                    </div>
                </div>
                <div class="flex flex-col text-center items-center justify-center font-sans mx-auto w-full">
                    <div v-if="recordedTime" class="text-textGray">{{ recordedTime }}</div>
                    <div v-else class="text-textGray">00:00</div>
                    <div v-if="recordedBlob" class="flex gap-4 justify-end mt-4">
                        <restore-button @restore="restore" />
                        <submit-button @submit="submitAudio" class="mx-auto" :color="buttonColor" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Recorder from "../../lib/Recorder";
import convertTimeMMSS from "../../lib/Utils";
import IconButton from "../common/iconButton.vue";
import SubmitButton from "../common/submitButton.vue";
import RestoreButton from "../common/restoreButton.vue";

const INSTRUCTION_MESSAGE = "Presiona el botón para iniciar la grabación.";
const INSTRUCTION_MESSAGE_STOP = "Presiona el botón nuevamente para detener la grabación.";

export default {
    name: "audioComp",
    props: {
        // in minutes
        time: { type: Number, default: 1 },
        bitRate: { type: Number, default: 128 },
        sampleRate: { type: Number, default: 44100 },
        backendEndpoint: { type: String },
        buttonColor: { type: String, default: "green" },

        // callback functions
        afterRecording: { type: Function },
        successfulUpload: { type: Function },
        failedUpload: { type: Function },
        customUpload: { type: Function, default: null }
    },
    components: {
        IconButton,
        SubmitButton,
        RestoreButton
    },
    data() {
        return {
            audioFile: '',
            recordOrLoad: true,
            recording: false,
            recordedAudio: null,
            recordedBlob: null,
            recorder: null,
            successMessage: null,
            errorMessage: null,
            instructionMessage: INSTRUCTION_MESSAGE,
        };
    },
    computed: {
        buttonClass() {
            return "mx-auto cursor-pointer";
        },
        recordedTime() {
            if (this.time && this.recorder?.duration >= this.time * 60) {
                this.toggleRecording();
            }
            return convertTimeMMSS(this.recorder?.duration);
        },
    },
    beforeUnmount() {
        if (this.recording) {
            this.stopRecorder();
        }
    },
    methods: {
        toggleRecording() {
            this.recording = !this.recording;
            if (this.recording) {
                this.initRecorder();
            } else {
                this.stopRecording();
            }
        },
        initRecorder() {
            this.recorder = new Recorder({
                micFailed: this.micFailed,
                bitRate: this.bitRate,
                sampleRate: this.sampleRate,
            });
            this.recorder.start();
            this.successMessage = null;
            this.errorMessage = null;
            this.instructionMessage = INSTRUCTION_MESSAGE_STOP;
        },
        stopRecording() {
            this.recorder.stop()
            const recordList = this.recorder.recordList()
            this.recordedAudio = recordList[0].url
            this.recordedBlob = recordList[0].blob
            if (this.recordedAudio) {
                this.instructionMessage = null
            }
            if (this.afterRecording) {
                this.afterRecording()
            }
        },
        submitAudio() {
            var formdata = new FormData();
            const file = new File([this.recordedBlob], "audio", { type: this.recordedBlob.type, });
            formdata.append("file", file);

            var requestOptions = {
                method: 'POST',
                body: formdata,
                redirect: 'follow'
            };
            this.$emit("loading")

            fetch("https://development.arcaxo.com/uploader", requestOptions)
                .then(response => response.text())
                .then(result => {
                    this.submitText(result)
                })
                .catch(error => console.log('error', error));
        },
        submitText(obj) {
            const transcription = JSON.parse(obj).transcription
            const url = 'https://development.arcaxo.com/api/genimg'
            const myHeaders = new Headers()
            myHeaders.append("Content-Type", "application/json")
            const raw = JSON.stringify({
                "frase": transcription
            });
            const options = {
                method: 'POST',
                mode: 'cors',
                headers: myHeaders,
                body: raw
            }
            fetch(url, options)
                .then(response => response.text())
                .then(result => {
                    this.$emit("response", result)
                    this.$emit("loading")
                })
                .catch(error => console.log('error', error));
        },
        restore() {
            this.recording = false
            this.recordedAudio = null
            this.recordedBlob = null
            this.recorder = null
            this.successMessage = INSTRUCTION_MESSAGE
        }
    },
};
</script>