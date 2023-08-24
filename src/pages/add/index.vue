<template>
  <view>
    <view class="flex flex-wrap bg-gray-200">
      <view v-for="(item, index) in tags" :key="index" class="w-1/4 text-center px-2 py-4" @click="popAdd(item)">
        <text> {{ item.name }}</text>
      </view>
    </view>

    <view>
      <uni-popup ref="popup" background-color="#fff" @change="change">
        <view class="h-80">
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4">当前标签</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" disabled v-model="createdData.tname" placeholder="tag name" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4">消费金额</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" v-model="createdData.amount" placeholder="消费金额只能是数字哦" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4">消费名称</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" v-model="createdData.name" placeholder="消费名称" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4">备注</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" v-model="createdData.record" placeholder="备注" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-1/4">时间</view>
            <view class="w-3/4">
              <uni-datetime-picker returnType="timestamp" v-model="createdData.date" @change="change($event)" />
            </view>
          </view>
          <button class="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-blue-500 hover:to-purple-500 text-white rounded-lg shadow-md transition duration-300 ease-in-out" @click="createBookJournal">提交</button>
        </view>
      </uni-popup>
    </view>

  </view>
</template>


<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import UniDatetimePicker from "@dcloudio/uni-ui/lib/uni-datetime-picker/uni-datetime-picker.vue";
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { CreateBookJournal, Tags, Books } from "../../api/index";
import { showT, isLogin } from "../../api/common";
import type * as types from "../../api/types";
import { reactive, ref } from "vue";
import moment from "moment";

const tags = ref([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any | null>(null);


const createdData = reactive<types.CreateBookJournalReq>({
  amount: "",
  record: "",
  tid: "",
  tname: "",
  bookID: "",
  name: "",
  date: new Date().getTime()
})

onShow(async () => {
  if (!isLogin())return
  tags.value = await Tags();
  createdData.bookID = (await Books())[0].id

});

const popAdd = (tag: types.Tag) => {
  // 底部弹出
  createdData.tid = tag.id
  createdData.tname = tag.name
  popup.value.open("bottom");
};

const createBookJournal = async () => {
  if (createdData.amount === '' || createdData.name === ''){
    showT("请填写完整")
    return
   }
   await CreateBookJournal(createdData)
   showT("添加成功")
   createdData.amount = ""
   createdData.name = ""
   popup.value.close()
}


const change = (e: any) => {
  console.log(e);
};
</script>
<style></style>
