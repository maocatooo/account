import * as types from "./types";

interface requestInfo {
  url: string
  method: 'OPTIONS' | 'GET' | 'HEAD' | 'POST' | 'PUT' | 'DELETE' | 'TRACE' | 'CONNECT'
  data?: object
  header?: {
    Authorization?: string
  }
}

// const api_url = "https://ac.maocat.cc"
const api_url = "http://127.0.0.1:8888"

async function request(info: requestInfo): Promise<any> {
  try {
    if (!info.header) {
      info.header = {}
    }
    info.header["Authorization"] = uni.getStorageSync("token")
    var res = await uni.request({
      url: api_url + info.url,
      method: info.method,
      header: info.header,
      data: info.data
    });
    // 此处的 res 参数，与使用默认方式调用时 success 回调中的 res 参数一致
    return res.data
  } catch (err) {
    // 此处的 err 参数，与使用默认方式调用时 fail 回调中的 err 参数一致
    console.error(err);
  }
}


export const Login = async (req: types.LoginReq): Promise<types.LoginRsp> => {
  return await request({
    url: "/login",
    method: "POST",
    data: req
  })
}

export const Books = async (): Promise<types.Book[]> => {
  return await request({
    url: "/book",
    method: "GET"
  })
}

export const Tags = async (): Promise<types.Tag[]> => {
  return await request({
    url: "/tag",
    method: "GET"
  })
}

export const CreateTag = async (c: types.SaveTagReq) : Promise<types.Tag> => {
  return await request({
    url: "/tag", method: "POST", data: c
  })
}

export const UpdateTag = async (c: types.SaveTagReq) : Promise<types.Tag> => {
  return await request({
    url: "/tag", method: "PUT", data: c
  })
}


export const BookJournals = async (c:types.BookJournalsReq):Promise<types.BookJournal[]> => {
  return await request({
    url:"/journal", 
    method: "GET",
    data: c
  })
}

export const CreateBookJournal = async (c: types.SaveBookJournalReq) => {
  return await request({
    url:"/journal",
    method: "POST",
    data:c
  })
}

export const UpdateBookJournal = async (c: types.SaveBookJournalReq) => {
  return await request({
    url:"/journal",
    method: "PUT",
    data:c
  })
}

export const DeleteBookJournal = async (id: string) => {
  return await request({
    url:"/journal",
    method: "DELETE",
    data:{id}
  })
}


export const NamePrompt = async (tid: string) => {
  return await request({
    url:"/name_prompt",
    method: "GET",
    data:{tid}
  })
}
