# OCR功能使用指南

## 概述

本项目已集成SimpleTex OCR API，支持图片文字识别功能。用户可以通过上传图片或粘贴图片到输入区域，然后使用OCR识别功能提取图片中的文字。

## 功能特性

- **多格式支持**: 支持PNG、JPG、JPEG、BMP、TIFF、WEBP等常见图片格式
- **文件大小限制**: 最大支持10MB的图片文件
- **拖拽上传**: 支持拖拽图片到上传区域
- **图片预览**: 上传后显示图片预览和文件信息
- **任务队列**: OCR识别任务集成到任务队列系统中
- **错误处理**: 完善的错误处理和用户提示

## 使用方法

### 1. 切换到图片输入模式

在输入区域顶部，点击"图片上传"按钮切换到图片输入模式。

### 2. 上传图片

有两种方式上传图片：

- **点击上传**: 点击上传区域选择图片文件
- **拖拽上传**: 直接将图片文件拖拽到上传区域

### 3. 执行OCR识别

上传图片后，点击"OCR识别"按钮开始识别。识别结果将显示在"处理结果"区域。

### 4. 查看任务进度

OCR识别任务会添加到任务队列中，可以在"任务队列"选项卡中查看处理进度和结果。

## 配置说明

### 环境变量配置

OCR功能使用以下环境变量进行配置：

```bash
# SimpleTex API配置
SIMPLETEX_APP_ID=*
SIMPLETEX_APP_SECRET=*

# 可选配置
SIMPLETEX_API_URL=https://server.simpletex.cn/api/simpletex_ocr
OCR_MAX_FILE_SIZE=10485760  # 10MB in bytes
OCR_TIMEOUT=30  # 请求超时时间（秒）
OCR_MAX_RETRIES=3  # 最大重试次数
```

### 默认配置

如果不设置环境变量，系统将使用以下默认配置：

- **App ID**: `*`
- **App Secret**: `*`
- **API URL**: `https://server.simpletex.cn/api/simpletex_ocr`
- **最大文件大小**: 10MB
- **超时时间**: 30秒
- **最大重试次数**: 3次

## API接口

### OCR识别接口

**POST** `/api/ocr`

**请求格式**: `multipart/form-data`

**参数**:
- `file`: 图片文件

**响应示例**:
```json
{
  "success": true,
  "data": {
    "ocr_text": "识别出的文字内容",
    "request_id": "tr_xxxxxxxxxx",
    "file_info": {
      "filename": "test.png",
      "size": 1024,
      "format": "png"
    }
  }
}
```

### 测试连接接口

**GET** `/api/ocr/test`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "message": "API连接正常",
    "request_id": "tr_xxxxxxxxxx"
  }
}
```

### 获取支持格式接口

**GET** `/api/ocr/formats`

**响应示例**:
```json
{
  "success": true,
  "data": {
    "supported_formats": ["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
    "max_file_size_mb": 10
  }
}
```

## 错误处理

### 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|----------|
| `api_not_find` | API或对应版本未找到 | 检查API URL配置 |
| `req_unauthorized` | 认证失败 | 检查App ID和App Secret |
| `resource_no_valid` | 没有可用的资源包或账户余额不足 | 检查SimpleTex账户状态 |
| `image_missing` | 未上传图片文件 | 确保上传了图片文件 |
| `image_oversize` | 图片文件过大 | 压缩图片或使用更小的文件 |
| `exceed_max_qps` | 超出最大QPS限制 | 稍后重试 |
| `exceed_max_ccy` | 超出最大并发请求数 | 稍后重试 |

### 错误响应格式

```json
{
  "success": false,
  "error": "错误描述信息",
  "error_code": "错误代码"
}
```

## 开发说明

### 文件结构

```
src/
├── config/
│   └── ocr_config.py          # OCR配置管理
├── services/
│   └── ocr_service.py         # OCR服务实现
└── api/
    └── routes.py              # OCR API路由
```

### 核心类

#### OCRConfig

OCR配置管理类，负责加载和管理OCR相关配置。

#### SimpleTexOCRService

SimpleTex OCR API的封装类，提供OCR识别功能。

#### OCRService

OCR服务主类，提供统一的OCR服务接口。

### 测试

运行测试脚本验证OCR功能：

```bash
python test_ocr.py
```

## 注意事项

1. **API限制**: SimpleTex API有QPS和并发请求限制，请合理使用
2. **文件格式**: 确保上传的图片格式在支持列表中
3. **文件大小**: 图片文件不能超过10MB
4. **网络连接**: OCR识别需要网络连接，请确保网络通畅
5. **账户状态**: 确保SimpleTex账户有足够的资源包或余额

## 故障排除

### 常见问题

1. **OCR识别失败**
   - 检查网络连接
   - 验证API配置
   - 确认图片格式和大小

2. **上传图片失败**
   - 检查文件格式是否支持
   - 确认文件大小不超过限制
   - 检查浏览器是否支持文件上传

3. **任务队列显示错误**
   - 刷新页面重新加载
   - 检查浏览器控制台错误信息
   - 确认JavaScript功能正常

### 调试模式

在浏览器控制台中设置调试模式：

```javascript
app.debugMode = true;
```

这将显示更详细的OCR处理信息。

## 更新日志

- **v1.0.0**: 初始版本，支持基本的OCR识别功能
- 支持图片上传和预览
- 集成任务队列系统
- 完善的错误处理机制
