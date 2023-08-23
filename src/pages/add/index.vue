<template>
  <view>
    <view class="flex flex-wrap bg-gray-200">
      <view v-for="(item, index) in tags" :key="index" class="w-1/8 text-center p-3" @click="popAdd">
        <text> {{ item.name }}</text>
      </view>
    </view>

    <view>
      <uni-popup ref="popup" background-color="#fff" @change="change">
      <view class="p-3 h-60">
        <uni-easyinput :cursorSpacing="100" v-model="addTagName" placeholder="tag name" />
        <button class="my-1" click="">提交</button>
      </view>
    </uni-popup>
    </view>
    
  </view>
</template>


<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { CreateTag, Tags } from "../../api/index";
import { showT } from "../../api/common";
import type * as types from "../../api/types";
import { reactive, ref } from "vue";

const tags = ref([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any | null>(null);

const addTagName = ref("");

onShow(async () => {
  tags.value = await Tags(); 
});

const popAdd = () => {
  // 底部弹出
  popup.value.open("bottom");
};

const change = (e: any) => {
  console.log(e);
};
</script>
<style>
/* .flex-wrap{
  flex-wrap: wrap;
} */
</style>
