<template>
  <view>
    <view>
      <view v-for="(item, index) in tags" :key="index" class="p-3">
        <text> {{ item.name }}</text>
      </view>
      <button @click="popAdd">新建</button>
    </view>

    <view>
      <uni-popup ref="popup" background-color="#fff" @change="change">
      <view class="p-3 h-60">
        <uni-easyinput cursorSpacing="100" v-model="addTagName" placeholder="tag name" />
        <button class="my-1" @click="addTag">提交</button>
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

const tags = reactive([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any | null>(null);

const addTagName = ref("");

onShow(async () => {
  const res = await Tags();
  res.map((item) => {
    tags.push(item);
  });
});

const popAdd = () => {
  // 底部弹出
  popup.value.open("bottom");
};

const change = (e: any) => {
  console.log(e);
};
const addTag = () => {
  // 判断是否为空
  if (addTagName.value == ""){
    showT("tag name can not be empty")
    return
  }
  // 判断是否已经存在
  for (let i = 0; i < tags.length; i++) {
    if (tags[i].name == addTagName.value) {
      showT("tag name already exists")
      return;
    }
  }

  CreateTag({name:addTagName.value}).then((res) => {
    tags.push(res)
    popup.value.close()
  });
  
};
</script>
<style>
</style>
