<template>
  <view :class="viewClass">
    <view class=" flex items-center justify-center">
      <img :src="data" :class="imageClass">
    </view>
    <view v-if="iconName">
       <text class="text-xs">{{ iconName }}</text> 
     </view>
  </view>
</template>


<script lang="ts">
import { defineComponent } from 'vue'
import { defaultBase64SVG } from "../../api/common";

export default defineComponent({
  props: {
    data: {
      type: String,
      default: defaultBase64SVG
    },
    iconName: {
      type: String,
      default: ""
    },
    imageClass: {
      type: String,
      default: "w-8 h-8"
    },
    viewClass: {
      type: String,
      default: ""
    }
  },

  setup: (props, { emit }) => {
    return {
        
    }
  }
})

</script>
<style></style>
