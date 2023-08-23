import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import { resolve } from 'node:path'
import AutoImport from 'unplugin-auto-import/vite'
import {UnifiedViteWeappTailwindcssPlugin as uvwt} from 'weapp-tailwindcss/vite'
import postcss from './postcss.config'

console.log(process.env.UNI_PLATFORM === 'mp-weixin')
export default defineConfig({
  plugins: [
    AutoImport({
      imports: ['vue', 'uni-app'],
      dts: true,
      eslintrc: {
        enabled: true
      }
    }),
    uni(),
    uvwt({disabled:process.env.UNI_PLATFORM !== 'mp-weixin'})
  ],
  css: {
    postcss
  },
  resolve: {
    alias: {
      '@': `${resolve(__dirname)}/`
    }
  }
})
