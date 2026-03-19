# 错误处理规范

## 1. 基本原则
- Fail Fast：配置缺失、方法不支持、字段类型错误应立即抛出异常。
- Fail Visible：运行失败必须写入结果产物，不允许静默吞掉。

## 2. 约束
- 禁止使用 `except: pass`
- `except Exception` 必须记录上下文：任务名、方法名、seed、阶段
- 错误信息应可直接定位到配置字段或函数入口

## 3. 建议实践
- 配置读取阶段做结构校验（参考 `validate_config`）
- 批量运行阶段将异常转为结构化字段输出：`status` + `error_message`

