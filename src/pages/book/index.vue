<template>
  <view>
    <view
      v-for="(item, index) in groupBookJournals?.groupData"
      :key="index"
      class="p-3"
    >
      <view class="flex flex-row items-center p-2">
        <text class="w-1/2">{{ item.date }}</text>
        <text class="w-1/2 text-right">{{ item.allAmount }}</text>
      </view>
      <view
        v-for="i2 in item.data"
        :key="i2.id"
        class="flex flex-row items-center p-2 font-thin"
      >
      <view class="w-1/4 text-center">{{ i2.tname }}</view>
      <view class="w-1/4 text-center font-thin text-sm">{{ formatTime(i2.date) }}</view>
      <view class="w-1/4 text-center">{{ i2.name }}</view>
      <view class="w-1/4 text-center">{{ i2.amount }}</view>
      </view>
    </view>
  </view>
</template>


<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { Login, Books, BookJournals } from "../../api/index";
import type * as types from "../../api/types";
import { ref, computed } from "vue";
import moment from "moment";
import Decimal from "decimal.js";

const books = ref([] as types.Book[]);

const bookJournals = ref([] as types.BookJournal[]);

const groupBookJournals = computed(() => {
  const bjs = bookJournals.value;
  let allAmount = new Decimal(0);
  if (!bjs || bjs.length === 0) {
    return;
  }
  let groupData: {
    data: types.BookJournal[];
    allAmount: Decimal;
    date: string;
  }[] = [];
  // 日期分组
  let c: any = {};
  bjs.map((obj) => {
    const date = moment(obj.date);
    const day = date.format("D");
    if (!c[day]) {
      c[day] = {
        data: [],
        allAmount: new Decimal(0),
        date: date.format("MM-DD"),
      };
      groupData.push(c[day]);
    }
    c[day].data.push(obj);
    c[day].allAmount = c[day].allAmount.add(new Decimal(obj.amount));
    allAmount = allAmount.add(new Decimal(obj.amount));
  });
  return {
    groupData,
    allAmount,
  };
});


const formatTime = (t :number) => {
  // 时分秒
  return moment(t).format("HH:mm");
}


onShow(async () => {
  const res = await Books();
  books.value = res;

  if (books.value.length === 0) {
    return;
  }
  const bgs = await BookJournals({
    bookID: books.value[0].id,
    date: parseInt(moment(moment().format("YYYY-MM")).format("x")),
  });
  bookJournals.value = bgs;
});
</script>
<style>
</style>
