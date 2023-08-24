<template>
  <view>
    <view>
      <picker
        mode="date"
        fields="month"
        start="2000-01-01"
        end="2100-12-31"
        @change="handleDateChange"
      >
        <view class="picker">
          <slot ></slot>
        </view>
      </picker>
    </view>
  </view>
</template>


<script lang="ts">
import { defineComponent} from 'vue'

export default defineComponent({
setup: (props, {emit}) => {
  const handleDateChange = (event: any) => {
    const [year, month] = event.detail.value.split("-");
    // 传递给父组件
    emit("changeDate", { year:parseInt(year), month:parseInt(month) });
  };
  return {
    handleDateChange
  }}
})

</script>
<style>
</style>
