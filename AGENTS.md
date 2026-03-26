# AGENTS.md

## Project Structure

- 主代码位于 `src/amis_python`。
- Django 测试入口位于 `src/manage.py`，默认 settings 为 `src/test_settings.py`。
- 测试 URL 挂载走 `src/test_urls.py`，应用以 `/amis/` 前缀接入。
- `test_django` 是示例/集成测试项目，不是默认改动目标。

## Validation

- 涉及 Django 接口、登录态或上传链路时，优先在 `src` 目录执行：
  - `uv run python manage.py test amis_python.tests.test_views -v 2`
- 不要用仓库根目录直接跑 `manage.py test`。
- `unittest discover` 只能用于纯 Python / schema 测试，不适合覆盖 Django API 链路。

## Git

- 用户要求执行 `git push` 时，默认同时推送到 `origin` 和 `gitee`。
- 不要把测试生成的 `src/files/` 或其他临时产物提交到仓库。
