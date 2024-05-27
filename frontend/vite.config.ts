import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import { resolve } from 'node:path'
import AutoImport from 'unplugin-auto-import/vite'
import {UnifiedViteWeappTailwindcssPlugin as uvwt} from 'weapp-tailwindcss/vite'
import postcss from './postcss.config'

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // 指定输出路径
        dir: 'dist/dev/mp-weixin', // 你想要的输出路径
      },
    },
  },
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
