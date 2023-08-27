<template>
  <view>
    <uni-swipe-action>
    <view >
      <swipe v-for="(item, index) in tags" :key="index" :data="item" @btn1="btn1" @btn2="btn2(item)">
        <view class="flex flex-row items-center px-4  py-4">
          <tagIcon :data="item.icon || undefined" :imageClass="'w-4 h-4'"  class="w-1/3" />  
          <text  class="w-2/3" > {{ item.name }}</text>
        </view>
      </swipe>
      <button class="py-3 mt-2 mx-2 border-none bg-gradient-to-r  from-emerald-400 to-green-400  text-white rounded-lg shadow-md transition duration-300 ease-in-out"
            @click="popSave">新建</button>
    </view>
   
  </uni-swipe-action>
    <view>
      <uni-popup ref="popup" background-color="#fff" @change="change">
      <view class="p-3 h-60">
        <view class="flex flex-row items-center p-2">
            <view class="w-1/4 text-right pr-2">标签:</view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" v-model="saveTagName" placeholder="tag name" />
            </view>
        </view>
        <view class="flex flex-row items-center p-2">
            <view class="w-1/8 text-right pr-2">
              icon:
            </view>
            <view class="w-1/8 text-right pr-2">
              <tagIcon :data="toImgBase64SVG(saveTagIcon)" :imageClass="'w-4 h-4'"  :viewClass="'flex items-center'" />  
            </view>
            <view class="w-3/4">
              <uni-easyinput :cursorSpacing="100" v-model="saveTagIcon" @input="iconInputing"  :maxlength="-1"  placeholder="icon svg" />
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
import { showT, toImgBase64SVG, toImgSVGByBase64 } from "../../api/common";
import type * as types from "../../api/types";
import { reactive, ref } from "vue";

const tags = reactive([] as types.Tag[]);
// 对应uni-popup ref="popup" 里面的ref
const popup = ref<any | null>(null);

const saveTagName = ref("");
const saveTagIcon = ref("");
const updateTagNameId = ref("");

const popSave = (item?:types.Tag ) => {
  // 底部弹出
  
  saveTagName.value = item?.name || ""
  saveTagIcon.value = toImgSVGByBase64(item?.icon || "") || ""
  updateTagNameId.value = item?.id || ""

  popup.value.open("bottom");
};

const saveTagIconComputed = computed(() => {
  console.log("saveTagIconComputed");
  console.log(saveTagIcon.value.slice(0, 100))
  console.log(toImgBase64SVG(saveTagIcon.value));
  return toImgBase64SVG(saveTagIcon.value)
})

const change = (e: any) => {
  console.log(e);
};

const iconInputing = (e: any) => {
  console.log(e);
};

const btn1 = (e: types.Tag ) => {
  console.log("btn1");
  console.log(e);
};


const btn2 = (e: types.Tag) => {
  popSave(e)
};


const saveTag = () => {
  // 判断是否为空
  if (saveTagName.value == ""){
    showT("tag name can not be empty")
    return
  }
  // 判断是否已经存在
  for (let i = 0; i < tags.length; i++) {
    if (tags[i].name == saveTagName.value && (updateTagNameId.value ==="" ||tags[i].id != updateTagNameId.value)) {
      showT("tag name already exists")
      return;
    }
  }

  if (updateTagNameId.value !== "")  {
    UpdateTag({id: updateTagNameId.value,name:saveTagName.value, icon:toImgBase64SVG(saveTagIcon.value) }).then((res) => {
      for (let i = 0; i < tags.length; i++) {
      if (tags[i].id == updateTagNameId.value) {
        tags[i].icon = res.icon
        tags[i].name = res.name
      }
  }
      
      popup.value.close()
    });
  }else{
    CreateTag({name:saveTagName.value, icon: toImgBase64SVG(saveTagIcon.value)}).then((res) => {
    tags.push(res)
    popup.value.close()
  });
  }

  
};

onShow(async () => {
  const res = await Tags();
  res.map((item) => {
    tags.push(item);
  });
});
</script>
<style>
</style>
