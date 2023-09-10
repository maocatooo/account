<template>
  <view class="p-5">
    <view class="flex flex-row items-center h-12" @click="login">
      <view >
        <img class="w-16 h-16" :src="user.avatarUrl" alt="">
      </view>
      <view class=" ml-5">
        {{ user.name }}
      </view>
    </view>
    <view  class="flex flex-row items-center h-12" @click="navigateTo('/pages/home_book/index')">
      <view class="w-1/2">
        account books
      </view>
      <view class="w-1/2 text-right">
        {{ info.books.length.toString() }} >
      </view>
    </view>
    <view class="flex flex-row items-center  h-12" @click="navigateTo('/pages/home_tag/index')">
      <view class="w-1/2">
        tags
      </view>
      <view class="w-1/2 text-right">
        {{ info.tags.length.toString() }} >
      </view>
    </view>
    <view class="flex flex-row items-center  h-12">
      <view class="w-1/2">
        book show tag name
      </view>
      <view class="w-1/2 text-right">
        <switch :checked="showTagNameFlag" style="transform:scale(0.7)" @change="showTagName" />
      </view>
    </view>
  </view>
</template>

<script setup  lang="ts">
import { reactive } from "vue";
import { navigateTo } from "../../api/common";
import { Login, Books, Tags } from "../../api/index";
import type * as types from "../../api/types";
import { onShow } from "@dcloudio/uni-app";

const user = reactive({
  name: "未登录,点击登录",
  avatarUrl: "",
});

const info = reactive({
  books: [] as types.Book[],
  tags: [] as types.Tag[],
});

const login = () => {
  uni.login({
    provider: "weixin", //使用微信登录
    success: async function (loginRes) {
      const res: types.LoginRsp = await Login({ code: loginRes.code });
      user.name = res.name;
      user.avatarUrl = res.avatarUrl;
      uni.setStorageSync("token", res.accessToken);

      info.books = await Books();
      info.tags = await Tags();
    },
  });
};

let showTagNameFlag = false

onShow(() => {
  // 每次进来页面重新登录一下,反正是静默登录
  login();
  showTagNameFlag = uni.getStorageSync('showTagName')|| false
});

const showTagName = (e:any)=>{
  showTagNameFlag = e.detail.value
  uni.setStorageSync("showTagName",e.detail.value)  
}

</script>

<style></style>
