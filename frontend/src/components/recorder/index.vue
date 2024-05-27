<script setup lang="ts" >
import { reactive, ref, onMounted, toRefs } from "vue";
import { showT, switchTab, toImgBase64SVG } from "../../api/common";
import { asrGenerateUrl, CreateBookJournalByDescribe } from "../../api/index";
import tagIcon from "../../components/tag_icon/index.vue";
const props = defineProps({
    book_id: String
}) as {book_id: string}
const starticon = `<svg t="1699798147508" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4924" width="200" height="200"><path d="M512 640c115.2 0 208-92.8 208-208V272c0-115.2-92.8-208-208-208S304 156.8 304 272v160c0 115.2 92.8 208 208 208z m-144-368c0-80 64-144 144-144s144 64 144 144v160c0 80-64 144-144 144s-144-64-144-144V272z" fill="#4A576A" p-id="4925"></path><path d="M844.8 480c0-17.6-14.4-32-32-32-16 0-30.4 12.8-32 28.8C758.4 606.4 646.4 704 512 704s-246.4-97.6-268.8-227.2c-1.6-16-16-28.8-32-28.8-17.6 0-32 14.4-32 32v4.8C204.8 635.2 328 752 480 766.4V928c0 17.6 14.4 32 32 32s32-14.4 32-32V766.4c152-14.4 275.2-131.2 299.2-280 0-1.6 1.6-4.8 1.6-6.4z" fill="#4A576A" p-id="4926"></path></svg>`
const endicon = `<svg t="1699801062386" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="8098" width="200" height="200"><path d="M212.992 526.336 212.992 526.336 212.992 526.336 215.04 526.336 212.992 526.336Z" p-id="8099"></path><path d="M817.152 202.752 817.152 202.752C737.28 122.88 628.736 75.776 509.952 75.776c-118.784 0-229.376 49.152-307.2 126.976l0 0c-77.824 77.824-126.976 186.368-126.976 307.2 0 118.784 49.152 229.376 126.976 307.2 77.824 79.872 188.416 126.976 307.2 126.976 120.832 0 229.376-49.152 307.2-126.976 79.872-77.824 126.976-186.368 126.976-307.2C946.176 389.12 897.024 280.576 817.152 202.752zM770.048 770.048c-65.536 65.536-157.696 108.544-260.096 108.544-102.4 0-194.56-40.96-260.096-108.544C184.32 704.512 141.312 612.352 141.312 509.952s40.96-194.56 108.544-260.096C317.44 184.32 409.6 141.312 509.952 141.312c100.352 0 192.512 40.96 258.048 106.496l2.048 2.048c65.536 65.536 108.544 157.696 108.544 260.096S837.632 704.512 770.048 770.048z" p-id="8100"></path><path d="M724.992 296.96 724.992 296.96 296.96 296.96 296.96 724.992 724.992 724.992 724.992 296.96Z" p-id="8101"></path></svg>`
console.log("book_id", props.book_id)
const iconB64 = ref(toImgBase64SVG(starticon))
let socketTask: any = null;
let recorderManager: any = null;
let startRecorder = false
let voiceTextStr = ""
const voicePath = ref("")
const startRecord = async () => {
  console.log('开始录音');
  uni.showLoading({ "title": "开始录音" })
  const data = await asrGenerateUrl()
  socketTask = uni.connectSocket({
    url: data.url, //
    complete: () => {
      starRecorderManager()
    }
  });
  socketTask.onMessage(function (data: any) {
    if (!startRecorder){
      try {
        console.log("关闭socket")
        uni.hideLoading()
        iconB64.value = toImgBase64SVG(starticon)
        uni.closeSocket()
      }catch (e){
        console.log(e)
      }
    }
    var data = JSON.parse(data.data)
    console.log("读消息读消息读消息")
    if (data?.final === 1) {
      if (voiceTextStr) {
        CreateBookJournalByDescribe({ book_id: props.book_id, describe: voiceTextStr }).then((res) => {
          if (res?.id) {
            switchTab("/pages/book/index")
          } else {
            showT("添加失败,请重试")
          }
        })
      } else {
        showT("添加失败,请重试")
      }
    } else {
      voiceTextStr = data.result?.voice_text_str
    }

  })

}

function starRecorderManager() {
  if (startRecorder){
    try{
        recorderManager.stop();
      }catch{
    }
  }

  iconB64.value = toImgBase64SVG(endicon)
  recorderManager = uni.getRecorderManager()
  recorderManager.onFrameRecorded(async function (res: any) {
    socketTask.send({ data: res.frameBuffer })
  });

  recorderManager.onStart(async (res: any) => { });
  recorderManager.onError(async (res: any) => {
    console.log("err", res);
  });
  recorderManager.onStop(function (res: any) {
    console.log('录音结束');
    voicePath.value = res.tempFilePath;
    socketTask.send({ data: JSON.stringify({ type: "end" }) })
    startRecorder = false
  });
  recorderManager.start({
    frameSize: 10,
    format: "PCM",
    sampleRate: 16000,
    numberOfChannels: 1,
    duration: 10 * 1000
  });
  
  startRecorder = true
}

let interva :any = null
const endRecord = async () => {
  interva = setInterval(()=>{
    if (startRecorder){
      try{
        recorderManager.stop();
      }catch{
      }
      clearInterval(interva)
    }
  },50)
}

</script>
<template>
    <view v-if="props.book_id"  class="flex fixed bottom-4 w-10 h-10 right-4">
        <tagIcon :data="iconB64"  :imageClass="'w-10 h-10'" @touchstart="startRecord" @touchend="endRecord" class="w-full" />
  </view>
   
</template>


<style></style>
