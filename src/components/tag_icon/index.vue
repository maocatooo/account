<template>
  <view :class="viewClass">
    <img :src="data" :class="imageClass">
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
    imageClass: {
      type: String,
      default: ""
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
