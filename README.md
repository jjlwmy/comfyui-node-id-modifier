# ComfyUI Node ID Modifier

![ComfyUI Node ID Modifier](https://img.shields.io/badge/ComfyUI-Custom%20Node-blue)
![License](https://img.shields.io/badge/License-MIT-green)

一个用于修改 ComfyUI 工作流中节点 ID 的自定义节点插件。

## ✨ 功能

### 1. 右键菜单直接修改（推荐）

在 ComfyUI 画布上直接操作：

- **Change Node ID**: 右键点击单个节点，选择此选项修改节点 ID
- **Normalize All Node IDs**: 右键空白处，将所有节点 ID 重新排列为连续的数字序列（从 1 开始）

### 2. 键盘快捷键

- `Ctrl/Cmd + I`: 选中节点后按此快捷键快速打开修改 ID 对话框

### 3. 处理工作流 JSON 文件

提供三个处理节点：

- **Modify Node ID**: 修改单个节点 ID
- **Batch Modify Node IDs**: 通过 JSON 映射批量修改多个节点 ID
- **Normalize Workflow IDs**: 将工作流中的节点 ID 规范化

支持两种工作流格式：
- **API 格式**: `{"10": {"inputs": {...}}, "11": {...}}`
- **UI 格式**: `{"nodes": [...], "links": [...]}`

## 📦 安装

### 方法一：手动安装

1. 下载或克隆此仓库
2. 将 `comfyui-node-id-modifier` 文件夹复制到 ComfyUI 的 `custom_nodes` 目录下
3. 重启 ComfyUI

### 方法二：通过 ComfyUI Manager

在 ComfyUI Manager 中搜索 "Node ID Modifier" 并安装。

## 🚀 使用方法

### 方法一：画布上直接修改（推荐）

1. 在 ComfyUI 画布中选中一个节点
2. 右键点击节点，选择 "Change Node ID"
3. 在弹出的对话框中输入新的 ID
4. 点击 OK 或按 Enter 确认

### 方法二：规范化所有节点 ID

1. 在 ComfyUI 画布中右键点击空白处
2. 选择 "Normalize All Node IDs"
3. 所有节点 ID 将自动重新排列为连续的数字序列

### 方法三：处理工作流 JSON 文件

#### 修改单个节点 ID

1. 添加 "Modify Node ID" 节点到工作流
2. 在 `workflow_json` 输入框中粘贴工作流 JSON 内容
3. 在 `old_node_id` 中输入要修改的旧节点 ID
4. 在 `new_node_id` 中输入新的节点 ID
5. 执行节点，结果将显示在 `modified_workflow` 输出中

#### 批量修改节点 ID

1. 添加 "Batch Modify Node IDs" 节点到工作流
2. 在 `workflow_json` 输入框中粘贴工作流 JSON 内容
3. 在 `id_mapping` 输入框中输入 JSON 格式的 ID 映射，例如：
   ```json
   {
     "10": "100",
     "11": "101",
     "12": "102"
   }
   ```
4. 执行节点，结果将显示在 `modified_workflow` 输出中

#### 规范化工作流 ID

1. 添加 "Normalize Workflow IDs" 节点到工作流
2. 在 `workflow_json` 输入框中粘贴工作流 JSON 内容
3. 设置 `start_id`（起始 ID，默认为 1）
4. 设置 `step`（步长，默认为 1）
5. 执行节点，结果将显示在 `normalized_workflow` 输出中

### 前端快捷按钮

所有处理节点都提供了以下快捷按钮：

- **Load Workflow**: 从文件加载工作流 JSON
- **Save Workflow**: 将修改后的工作流保存到文件
- **Clear**: 清空所有输入

## ⚠️ 注意事项

1. 节点 ID 在 ComfyUI 工作流中必须是唯一的整数
2. 修改节点 ID 时会自动更新所有连接关系
3. 建议在修改前备份工作流
4. 使用画布直接修改功能时，修改会立即生效

## 🛠️ 技术说明

该插件基于 ComfyUI 自定义节点 API 开发，包含：

- **Python 后端**: 处理工作流 JSON 的节点 ID 重命名逻辑
- **JavaScript 前端**: 提供右键菜单、键盘快捷键和文件操作功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 GitHub Issues 联系。