export interface LoginReq {
  code: string
  cavatarUrlode?: string
  name?: string
}


export interface LoginRsp {
  id: string
  name: string
  accessToken: string
  avatarUrl: string
  accessxpire: number
  refreshAfter: number
}

export interface Book {
  id: string
  name: string
  createdTime: number
  tp: number
  uid: string
}

export interface Tag {
  id: string
  name: string
  createdTime: number
  priority: number
}

export interface CreateTagReq {
  name: string
}

export interface BookJournalsReq {
  bookID: string
  date: number
}

export interface BookJournal {
  id: string
  name: string
  date: number
  tid: string
  tname: string
  amount: string
  record: string
  bookID: string
  uid: string
}


export interface CreateBookJournalReq {
  date:number
  amount:string
  record:string
  tid: string
  tname :string
  bookID :string
  name :string
}