<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import UniDatetimePicker from "@dcloudio/uni-ui/lib/uni-datetime-picker/uni-datetime-picker.vue";
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { UpdateBookJournal, CreateBookJournal, Tags, Books, NamePrompt, asrGenerateUrl, CreateBookJournalByDescribe } from "../../api/index";
import { showT, isLogin, switchTab, toImgBase64SVG } from "../../api/common";
import type * as types from "../../api/types";
import { reactive, ref, onMounted, toRefs } from "vue";
import tagIcon from "../../components/tag_icon/index.vue";
import moment from "moment";
import {useSaveBookStore} from "../../store/saveBook"

const store = useSaveBookStore()
const tags = ref([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any>(null);
const cursorSpacing = ref(100)
const showNamePrompt = ref(false)
const namePrompts = ref<string[]>([])

const starticon = `<svg t="1699798147508" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4924" width="200" height="200"><path d="M512 640c115.2 0 208-92.8 208-208V272c0-115.2-92.8-208-208-208S304 156.8 304 272v160c0 115.2 92.8 208 208 208z m-144-368c0-80 64-144 144-144s144 64 144 144v160c0 80-64 144-144 144s-144-64-144-144V272z" fill="#4A576A" p-id="4925"></path><path d="M844.8 480c0-17.6-14.4-32-32-32-16 0-30.4 12.8-32 28.8C758.4 606.4 646.4 704 512 704s-246.4-97.6-268.8-227.2c-1.6-16-16-28.8-32-28.8-17.6 0-32 14.4-32 32v4.8C204.8 635.2 328 752 480 766.4V928c0 17.6 14.4 32 32 32s32-14.4 32-32V766.4c152-14.4 275.2-131.2 299.2-280 0-1.6 1.6-4.8 1.6-6.4z" fill="#4A576A" p-id="4926"></path></svg>`
const endicon = `<svg t="1699801062386" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="8098" width="200" height="200"><path d="M212.992 526.336 212.992 526.336 212.992 526.336 215.04 526.336 212.992 526.336Z" p-id="8099"></path><path d="M817.152 202.752 817.152 202.752C737.28 122.88 628.736 75.776 509.952 75.776c-118.784 0-229.376 49.152-307.2 126.976l0 0c-77.824 77.824-126.976 186.368-126.976 307.2 0 118.784 49.152 229.376 126.976 307.2 77.824 79.872 188.416 126.976 307.2 126.976 120.832 0 229.376-49.152 307.2-126.976 79.872-77.824 126.976-186.368 126.976-307.2C946.176 389.12 897.024 280.576 817.152 202.752zM770.048 770.048c-65.536 65.536-157.696 108.544-260.096 108.544-102.4 0-194.56-40.96-260.096-108.544C184.32 704.512 141.312 612.352 141.312 509.952s40.96-194.56 108.544-260.096C317.44 184.32 409.6 141.312 509.952 141.312c100.352 0 192.512 40.96 258.048 106.496l2.048 2.048c65.536 65.536 108.544 157.696 108.544 260.096S837.632 704.512 770.048 770.048z" p-id="8100"></path><path d="M724.992 296.96 724.992 296.96 296.96 296.96 296.96 724.992 724.992 724.992 724.992 296.96Z" p-id="8101"></path></svg>`

const iconB64 = ref(toImgBase64SVG(starticon))


const voicePath = ref("")

let recorderManager: any = null;
let socketTask: any = null;
let startRecorder = false
function starRecorderManager() {
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
    console.log('recorder stop' + JSON.stringify(res));
    uni.hideLoading();
    voicePath.value = res.tempFilePath;
    socketTask.send({ data: JSON.stringify({ type: "end" }) })
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
      iconB64.value = toImgBase64SVG(starticon)
      recorderManager.stop();
      console.log('录音结束');
      startRecorder = false
      clearInterval(interva)
    }
  },50)
}

let voiceTextStr = ""

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
      // 关闭socket
      uni.hideLoading()
      console.log("关闭socket")
      uni.closeSocket()
    }
    var data = JSON.parse(data.data)
    console.log("读消息读消息读消息")
    if (data?.final === 1) {
      if (voiceTextStr) {
        CreateBookJournalByDescribe({ book_id: saveData.book_id, describe: voiceTextStr }).then((res) => {
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

const saveData = reactive<types.SaveBookJournalReq>({
  id: "",
  amount: "",
  record: "",
  tid: "",
  tname: "",
  book_id: "",
  name: "",
  date: new Date().getTime()
})

const popAdd = (tag: types.Tag) => {
  showNamePrompt.value = false
  // 底部弹出
  saveData.tid = tag.id
  saveData.tname = tag.name

  NamePrompt(tag.id).then((res: string[]) => {
    namePrompts.value = res
    popup.value.open("bottom");
  })
};

const popChange = (e: { show: boolean, type: string }) => {
  console.log(e);
};

const namePromptClick = (item: string) => {
  saveData.name = item
}

const createBookJournal = async () => {
  if (saveData.amount === '' || saveData.name === '') {
    showT("请填写完整")
    return
  }
  // amount 必须是数字
  if (isNaN(Number(saveData.amount))) {
    showT("消费金额只能是数字哦")
    return
  }
  const newData = {
    ...saveData,
    date: moment(saveData.date).format('YYYY-MM-DD HH:mm:ss')
  }
  if (saveData.id !== "") {
    await UpdateBookJournal(newData)
    showT("修改成功")
  } else {
    await CreateBookJournal(newData)
    showT("添加成功")
  }
  switchTab("/pages/book/index")
}

const clean = () => {
  saveData.id = ""
  saveData.amount = ""
  saveData.name = ""
}


onShow(async () => {
  if (!isLogin()) return
  tags.value = await Tags();
  saveData.book_id = (await Books())[0].id
  
  const updateData:any  = store.update
  if (updateData) {
    store.cleanUpdate()
    saveData.book_id = updateData.book_id
    saveData.amount = updateData.amount
    saveData.record = updateData.record
    saveData.tid = updateData.tid
    saveData.tname = updateData.tname
    saveData.name = updateData.name
    saveData.date = updateData.date
    saveData.id = updateData.id
    popup.value.open("bottom");
  } else {
    popup.value.close()
  }
});

onHide(() => {
  clean()
  popup.value.close()
});


</script>

<template>
  <view>
    <view class="flex flex-wrap mx-4 mt-3 border-2 border-gray-50 rounded-md">
      <view v-for="(item, index) in tags" :key="index" class="w-1/4 text-center px-2 py-4" @click="popAdd(item)">
        <tagIcon :data="item.icon || undefined" :imageClass="'w-8 h-8'" :iconName="item.name" class="w-1/3" />
        <!-- <text class="text-xs"> {{ item.name }}</text> -->
      </view>
    </view>

    <view>
      <uni-popup ref="popup" background-color="#fff" @change="popChange">
        <view class="h-80 mx-3 mt-3">
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">当前标签:</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="cursorSpacing" disabled v-model="saveData.tname" placeholder="tag name" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">消费金额:</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="cursorSpacing" type="number" v-model="saveData.amount"
                @focus="showNamePrompt = false" placeholder="消费金额只能是数字哦" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">消费名称:</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="cursorSpacing" v-model="saveData.name" placeholder="消费名称"
                @focus="showNamePrompt = true" @blur="" />
            </view>
          </view>
          <view class="flex overflow-x-auto text-sm p-2" v-show="showNamePrompt && (namePrompts?.length) > 0">
            <view class="flex-shrink-0 px-2 " v-for="(item, index) in namePrompts" :key=index>
              <view class="whitespace-nowrap">
                <view class="px-2 py-1  rounded text-emerald-50 bg-gradient-to-r from-emerald-400 to-green-400"
                  @click="namePromptClick(item)">
                  {{ item }}
                </view>
              </view>
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">备注:</view>
            <view class="w-3/4">
              <uni-easyinput @focus="showNamePrompt = false" :cursorSpacing="cursorSpacing" v-model="saveData.record"
                placeholder="备注" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">时间:</view>
            <view class="w-3/4" @click="showNamePrompt = false">
              <uni-datetime-picker returnType="timestamp" v-model="saveData.date" />
            </view>
          </view>
          <button
            class="py-3 mt-2 mx-2  border-none bg-gradient-to-r  from-emerald-400 to-green-400  text-white rounded-lg shadow-md transition duration-300 ease-in-out"
            @click="createBookJournal">提交</button>
        </view>

      </uni-popup>

    </view>
    <view class="mt-auto fixed bottom-4  w-full">
      <tagIcon :data="iconB64" :imageClass="'w-16 h-16'" class="w-1/3" @touchstart="startRecord" @touchend="endRecord" />
    </view>
  </view>
</template>

<style></style>
