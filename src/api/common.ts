

export function isLogin():boolean{
  return uni.getStorageSync("token") && true
} 


export function showT (title :string, duration:number = 2000) {
  uni.showToast({
    title: title,
    icon: "none",
    duration: duration
  });
}

export function navigateTo(url:string){
  uni.navigateTo({
    url: url
  });
}