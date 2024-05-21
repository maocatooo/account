export interface LoginReq {
  code: string
  avatarUrl?: string
  name?: string
}


export interface LoginRsp {
  id: string
  name: string
  access_token: string
  avatar: string
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
  icon:string
  createdTime: number
  priority: number
}

export interface SaveTagReq {
  id?: string
  name: string
  icon?:string
}

export interface BookJournalsReq {
  book_id: string
  date: string
}

export interface BookJournal {
  id: string
  name: string
  date: number
  tid: string
  tname: string
  amount: string
  record: string
  book_id: string
  uid: string
}


export interface SaveBookJournalReq {
  id?:string
  date:string|number
  amount:string
  record:string
  tid: string
  tname :string
  book_id :string
  name :string
}

export interface CreateBookJournalByDescribe {
  describe :string
  book_id :string
}