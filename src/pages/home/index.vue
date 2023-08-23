<template>
  <uni-list>
    <uni-list-item
      :title="user.name"
      note="--"
      :thumb="user.avatarUrl"
      thumb-size="lg"
      rightText=""
      clickable
      @click="login"
    />
    <uni-list-item
      title="account books"
      showArrow
      clickable
      @click="navigateTo('/pages/home_book/index')"
      :rightText="info.books.length.toString()"
    />
    <uni-list-item
      title="tags"
      showArrow
      clickable
      @click="navigateTo('/pages/home_tag/index')"
      :rightText="info.tags.length.toString()"
    />
  </uni-list>
</template>

<script setup  lang="ts">
import uniList from "@dcloudio/uni-ui/lib/uni-list/uni-list.vue";
import uniListItem from "@dcloudio/uni-ui/lib/uni-list-item/uni-list-item.vue";
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

onShow(() => {
  // 每次进来页面重新登录一下,反正是静默登录
  login();
});
</script>

<style>
</style>
