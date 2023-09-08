import { uniPostcssPlugin } from '@dcloudio/uni-cli-shared'
// @ts-ignore
import postcssImport from 'postcss-import'
import tailwindcss from 'tailwindcss'
// @ts-ignore
import postcssClassRename from 'postcss-class-rename'
// @ts-ignore
import cssByebye from 'css-byebye'
import autoprefixer from 'autoprefixer'
// import path from 'path'
import { resolve } from 'node:path'
const uniInputDir: string = process.env.UNI_INPUT_DIR as string
console.log(process.env.UNI_PLATFORM)
export default {
    plugins: [
        // postcssImport({
        //     resolve(id:string) {
        //         if (id.startsWith('~@/')) {
        //             return path.resolve(uniInputDir, id.substr(3))
        //         } else if (id.startsWith('@/')) {
        //             return path.resolve(uniInputDir, id.substr(2))
        //         } else if (id.startsWith('/') && !id.startsWith('//')) {
        //             return path.resolve(uniInputDir, id.substr(1))
        //         }
        //         return id
        //     }
        // }),
        tailwindcss(),
        // 根据平台差异进行不同的样式处理
        // ...(process.env.UNI_PLATFORM !== 'h5'
        //   ? [
        //       // 使用postcss-class-name 包将小程序不支持的类名转换为支持的类名
        //       postcssClassRename({
        //           '\\\\:': '--',
        //           '\\\\/': '--',
        //           '\\\\.': '--',
        //           // '.:': '--',
        //           '\\*': '--'
        //       }),
        //       cssByebye({
        //           rulesToRemove: [/\*/],
        //           map: false
        //       })
        //   ]
        //   : []),
        uniPostcssPlugin(),
        autoprefixer({
            remove: true
        })
    ]
}