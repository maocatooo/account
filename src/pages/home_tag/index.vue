<template>
  <view>
    <uni-swipe-action>
      <view class="p-4 border-b-2 border-gray-100 shadow-md  rounded-md">
          <swipe v-for="(item, index) in tags" :key="index" :data="item" @btn1="btn1" @btn2="btn2(item)">
            <view class="flex flex-row items-center px-4 py-2 border-b-2 shadow-md border-gray-200">
              <view  class="w-1/3" >
                <tagIcon :data="item.icon || undefined"/>
              </view>
              <view class="w-2/3 text-center"> {{ item.name }}</view>
            </view>
          </swipe>

        <button
          class="py-3 mt-2 mx-2 border-none bg-gradient-to-r  from-emerald-400 to-green-400  text-white rounded-lg shadow-md transition duration-300 ease-in-out"
          @click="popSave">新建</button>
      </view>

    </uni-swipe-action>
    <view>
      <uni-popup ref="popup" background-color="#fff" @change="change">
        <view class="p-3 h-60">
          <view class="flex flex-row items-center p-2">
            <view class="w-4/12">标签:</view>
            <view class="w-8/12">
              <uni-easyinput :cursorSpacing="100" v-model="saveTagName" placeholder="tag name" />
            </view>
          </view>
          <view class="flex flex-row items-center p-2">
            <view class="w-2/12">
              icon:
            </view>
            <view class="w-2/12 text-center">
              <tagIcon :data="toImgBase64SVG(saveTagIcon)" :viewClass="'flex items-center'" />
            </view>
            <view class="w-8/12">
              <uni-easyinput :cursorSpacing="100" v-model="saveTagIcon" @input="iconInputing" :maxlength="-1"
                placeholder="icon svg" />
            </view>
          </view>

          <view class="flex overflow-x-auto text-sm p-2">
            <view class="flex-shrink-0 px-2 " v-for="(item, index) in defaultIcons" :key="index" @click="setIcon(item)">
              <view class="whitespace-nowrap">
                <tagIcon :data="item" />
              </view>
            </view>
          </view>
          <button
            class="py-3 mt-2 mx-2  border-none bg-gradient-to-r  from-emerald-400 to-green-400  text-white rounded-lg shadow-md transition duration-300 ease-in-out"
            @click="saveTag">提交</button>
        </view>
      </uni-popup>
    </view>

  </view>
</template>


<script setup lang="ts">
import uniEasyinput from "@dcloudio/uni-ui/lib/uni-easyinput/uni-easyinput.vue";
import tagIcon from "../../components/tag_icon/index.vue";
import swipe from "../../components/swipe/index.vue";
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { CreateTag, Tags, UpdateTag } from "../../api/index";
import { showT, toImgBase64SVG, toImgSVGByBase64, defaultIcons } from "../../api/common";
import type * as types from "../../api/types";
import { reactive, ref } from "vue";

const tags = reactive([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any | null>(null);

const saveTagName = ref("");
const saveTagIcon = ref("");
const updateTagNameId = ref("");

const popSave = (item?: types.Tag) => {
  // 底部弹出

  saveTagName.value = item?.name || ""
  saveTagIcon.value = toImgSVGByBase64(item?.icon || "") || ""
  updateTagNameId.value = item?.id || ""

  popup.value.open("bottom");
};


const change = (e: any) => {
  console.log(e);
};

const iconInputing = (e: any) => {
  console.log(e);
};

const btn1 = (e: types.Tag) => {
  console.log("btn1");
  console.log(e);
};


const btn2 = (e: types.Tag) => {
  popSave(e)
};


const saveTag = () => {
  // 判断是否为空
  if (saveTagName.value == "") {
    showT("tag name can not be empty")
    return
  }
  // 判断是否已经存在
  for (let i = 0; i < tags.length; i++) {
    if (tags[i].name == saveTagName.value && (updateTagNameId.value === "" || tags[i].id != updateTagNameId.value)) {
      showT("tag name already exists")
      return;
    }
  }

  if (updateTagNameId.value !== "") {
    UpdateTag({ id: updateTagNameId.value, name: saveTagName.value, icon: toImgBase64SVG(saveTagIcon.value) }).then((res) => {
      for (let i = 0; i < tags.length; i++) {
        if (tags[i].id == updateTagNameId.value) {
          tags[i].icon = res.icon
          tags[i].name = res.name
        }
      }

      popup.value.close()
    });
  } else {
    CreateTag({ name: saveTagName.value, icon: toImgBase64SVG(saveTagIcon.value) }).then((res) => {
      tags.push(res)
      popup.value.close()
    });
  }
};


const setIcon = (icon: string) => {
  saveTagIcon.value = toImgSVGByBase64(icon)
}

onShow(async () => {
  const res = await Tags();
  res.map((item) => {
    tags.push(item);
  });
});
</script>
<style></style>
