<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import UniDatetimePicker from "@dcloudio/uni-ui/lib/uni-datetime-picker/uni-datetime-picker.vue";
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { UpdateBookJournal, CreateBookJournal, Tags, Books, NamePrompt, asrGenerateUrl, CreateBookJournalByDescribe } from "../../api/index";
import Recorder from "../../components/recorder/index.vue";
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


const book_id = ref("")

onShow(async () => {
  if (!isLogin()) return
  tags.value = await Tags();
  book_id.value = (await Books())[0].id
  saveData.book_id = book_id.value
  
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
    <view v-if="book_id">
      <Recorder :book_id="book_id" />
      </view>
  </view>
</template>

<style></style>
