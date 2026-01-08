import request from '@/utils/http'

/**
 * 列出目录下的文件和文件夹
 */
export function fetchListFiles(path: string = '') {
  return request.get({
    url: '/api/files/list',
    params: { path }
  })
}

/**
 * 读取文件内容
 */
export function fetchReadFile(path: string) {
  return request.get({
    url: '/api/files/read',
    params: { path }
  })
}

/**
 * 写入文件内容
 */
export function fetchWriteFile(path: string, content: string) {
  return request.post({
    url: '/api/files/write',
    data: { path, content }
  })
}

/**
 * 删除文件或目录
 */
export function fetchDeleteFile(path: string) {
  return request.delete({
    url: '/api/files/delete',
    data: { path }
  })
}

/**
 * 创建文件或目录
 */
export function fetchCreateFile(path: string, isDir: boolean = false) {
  return request.post({
    url: '/api/files/create',
    data: { path, is_dir: isDir }
  })
}
