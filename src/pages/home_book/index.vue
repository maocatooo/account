<template>
    <view>
        <view v-for="(item,index) in books" :key="index" class="p-3">
            <text> {{ item.name }}</text>
        </view> 
    </view>
</template>


<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { Login, Books, Tags } from '../../api/index'
import type * as types from '../../api/types'
import {ref} from 'vue'

const books = ref([] as types.Book[])

onShow(async() => {
    books.value = await Books()
});


</script>
<style>

</style>
