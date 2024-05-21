<template>
  <view class="p-5">
    <view class="flex flex-row items-center h-12" @click="popSave">
      <view >
        <img class="w-12 h-12" :src="user.avatarUrl" alt="">
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

      <view>
        <uni-popup ref="popup" background-color="#fff" @change="">
          <view class="p-3 h-60">
              <view class=" text-center">
                <button type="balanced" open-type="chooseAvatar" @chooseavatar="onChooseavatar">
                  <img class="w-12 h-12" :src="user.avatarUrl" alt="">
                </button>
                
              </view>
              <view class="flex flex-row items-center p-2">
                      <uni-easyinput :cursorSpacing="100" @blur="getnickname" v-model="user.name" type="nickname" placeholder="nickname" />
              </view>
              <button
                      class="py-3 mt-2 mx-2  border-none bg-gradient-to-r  from-emerald-400 to-green-400  text-white rounded-lg shadow-md transition duration-300 ease-in-out"
                      @click="login">提交</button>
          </view>
      </uni-popup>
      </view>
  </view>
</template>

<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import { reactive } from "vue";
import {defaultIcons, navigateTo, toImgBase64SVG, toImgSVGByBase64} from "../../api/common";
import { Login, Books, Tags, uploadAvatar } from "../../api/index";
import type * as types from "../../api/types";
import { onShow } from "@dcloudio/uni-app";
import {ref} from "vue";

const user = reactive({
  name: "",
  avatarUrl: "",
});

const info = reactive({
  books: [] as types.Book[],
  tags: [] as types.Tag[],
});

const getnickname=(e:any)=>{
  user.name = e.detail.value
}

const login = () => {
  uni.login({
    provider: "weixin", //使用微信登录
    success: async function (loginRes) {
      console.log(loginRes);
      
      const res: types.LoginRsp = await Login({ code: loginRes.code, avatarUrl:user.avatarUrl, name:user.name });
      user.name = res.name || "匿名用户";
      user.avatarUrl = res.avatar || "https://thirdwx.qlogo.cn/mmopen/vi_32/POgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg/132";
      uni.setStorageSync("token", "Bearer "+ res.access_token);

      info.books = await Books();
      info.tags = await Tags();
      popup.value.close()
    },
  });
};

let showTagNameFlag = false

onShow(() => {
  // 每次进来页面重新登录一下,反正是静默登录
  login();
  showTagNameFlag = uni.getStorageSync('showTagName')|| false
});
let popup = ref<any | null>(null);
const popSave = () => {
    // 底部弹出
    popup.value.open("top");
};

const onChooseavatar = (e:any) => {
  let {
    avatarUrl
  } = e.detail;
  user.avatarUrl = avatarUrl
  console.log(typeof avatarUrl);
  uploadAvatar(avatarUrl, function(res:string){
    user.avatarUrl = res
  })
}

const showTagName = (e:any)=>{
  showTagNameFlag = e.detail.value
  uni.setStorageSync("showTagName",e.detail.value)  
}

</script>

<style></style>
