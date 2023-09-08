<template>
    <uni-swipe-action-item
          :right-options="options2"
			    :left-options="options1"
			    :threshold="0"
			    @click="bindClick"
			>
          <slot ></slot>
    </uni-swipe-action-item>
</template>


<script lang="ts">
import { defineComponent} from 'vue'

export default defineComponent({
  props:{
    data:{
      type:Object,
      default:{}
    }
  },

setup: (props, {emit}) => {
  const bindClick = (e: any) => {
    if (e.position === "right") {
      if (e.index === 0){
        emit("btn1", props.data);
      }else if (e.index === 1){
        emit("btn2", props.data);
      }
    }
  };
 
  return {
    bindClick,
    options1: [
      // {
      //   text: "取消置顶",
      // },
    ],
    options2: [
      {
        text: "删除",
        style: {
          backgroundColor: "#F56C6C",
        },
      },
      {
        text: "修改",
        style: {
          backgroundColor: "#007aff",
        },
        class: "text-white",
      },
    ]
  }}
})

</script>
<style>
</style>
