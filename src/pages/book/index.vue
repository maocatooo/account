<template>

  <dateMonthPicker :month="selector.selectedMonth" :year="selector.selectedYear" @changeDate="change">
    <view class="picker">
        {{ selector.selectedYear }}年{{ selector.selectedMonth }}月
    </view>
  </dateMonthPicker>

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
import { isLogin } from "../../api/common";
import dateMonthPicker from "../../components/date_month_picker/index.vue";
import type * as types from "../../api/types";
import { ref, computed } from "vue";
import moment from "moment";
import Decimal from "decimal.js";

const selector = reactive({
  selectedYear: new Date().getFullYear(),
  selectedMonth: new Date().getMonth() + 1,
})

const change = ({year, month}:{year:number, month:number}) => {
  selector.selectedYear = year
  selector.selectedMonth = month
  initPage()
}

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


const initPage =async () => {
  const res = await Books();
  books.value = res;

  if (books.value.length === 0) {
    return;
  }
  const bgs = await BookJournals({
    bookID: books.value[0].id,
    date: parseInt(moment(new Date(selector.selectedYear, selector.selectedMonth-1)).format("x")),
  });
  bookJournals.value = bgs;
}

onShow(async () => {
  if (!isLogin()) {
    return;
  }
  await initPage()
});
</script>
<style>
</style>
