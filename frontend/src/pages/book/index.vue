<template>

  <view class="px-4 pt-4 flex flex-row items-center">
    <view class="w-1/2">
      <view class="w-28 ">
        <dateMonthPicker :month="selector.selectedMonth" :year="selector.selectedYear" @changeDate="change">
          <view class="picker">
            {{ selector.selectedYear }}年{{ selector.selectedMonth }}月
          </view>
        </dateMonthPicker>
      </view>
    </view>
    <view class="w-1/2 text-right">
      {{ groupBookJournals?.allAmount }}
    </view>
  </view>

  <view class="p-4">
    <uni-swipe-action>

    <view v-for="(item, index) in groupBookJournals?.groupData" :key="index"
      class="pb-3 mb-3 border-b-2 border-gray-100 shadow-md  rounded-md">
      <view
        class="rounded-t-md  flex flex-row items-center  py-4 text-emerald-50 bg-gradient-to-r from-emerald-400 to-green-400 text-xl">
        <text class="w-1/2 px-2 ">{{ item.date }}</text>
        <text class="w-1/2 px-2  text-right">{{ item.allAmount }}</text>
      </view>
        <swipe v-for="i2 in item.data" :key="i2.id" :data="i2" @btn1="deleteItem" @btn2="updateItem">
          <view class="flex flex-row items-center px-4  py-4 ">
            <tagIcon :data="tagMap[i2.tid]?.icon || undefined" :iconName="showTagName? i2.tname:''" :imageClass="'w-7 h-7'" class="w-1/4 text-center" /> 
            <!-- <view class="w-1/4 text-left">{{ i2.tname }}</view> -->
            <view class="w-1/4 text-center text-sm">{{ formatTime(i2.date) }}</view>
            <view class="w-1/4 text-center">{{ i2.name }}</view>
            <view class="w-1/4 text-center">{{ i2.amount }}</view>
          </view>
        </swipe>
    </view>
  </uni-swipe-action>
  </view>

  <view>
    <view v-if="books" >
      <Recorder :book_id="book_id" class="mt-auto fixed bottom-4  w-full"/>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLaunch, onShow, onHide, onLoad } from "@dcloudio/uni-app";
import { DeleteBookJournal, Books,Tags, BookJournals } from "../../api/index";
import { isLogin, showT,switchTab } from "../../api/common";
import dateMonthPicker from "../../components/date_month_picker/index.vue";
import tagIcon from "../../components/tag_icon/index.vue";
import swipe from "../../components/swipe/index.vue";
import Recorder from "../../components/recorder/index.vue";
import type * as types from "../../api/types";
import { ref, computed } from "vue";
import moment from "moment";
import Decimal from "decimal.js";
import {useSaveBookStore} from "../../store/saveBook"

const store = useSaveBookStore()

const selector = reactive({
  selectedYear: new Date().getFullYear(),
  selectedMonth: new Date().getMonth() + 1,
})

const change = ({ year, month }: { year: number, month: number }) => {
  selector.selectedYear = year
  selector.selectedMonth = month
  initPage()
}

const books = ref([] as types.Book[]);

const book_id = ref("")

const tagMap = {} as { [key: string]: types.Tag };

const bookJournals = ref([] as types.BookJournal[]);

const deleteItem = async (item:types.BookJournal)=>{
  await DeleteBookJournal(item.id)
  showT("删除成功")
  await initPage()
}


const updateItem = async (item:types.BookJournal)=>{
  store.setUpdate(item)
  switchTab("/pages/save/index")
}


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

const formatTime = (t: number) => {
  // 时分秒
  return moment(t).format("HH:mm");
}

let showTagName = false

const initPage = async () => {
  const res = await Books();
  console.log("books",res)
  books.value = res;

  if (books.value.length === 0) {
    return;
  }
  book_id.value  = books.value[0].id
  const tags = await Tags();
    tags.map((item) => {
      tagMap[item.id] = item
    })

  const bgs = await BookJournals({
    book_id: books.value[0].id,
    date: moment(new Date(selector.selectedYear, selector.selectedMonth - 1)).format('YYYY-MM'),
  });
  bookJournals.value = bgs;

  showTagName = uni.getStorageSync("showTagName")  
  console.log(showTagName);
  
}

onShow(async () => {
  if (!isLogin()) {
    return;
  }
  await initPage()
});

</script>
<style></style>
