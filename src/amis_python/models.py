import datetime
import os
import uuid


def uuid_filename(instance, filename):
    """
    为历史 migration 保留的 upload_to 回调。

    当前上传实现已经不再依赖 Django model；这里只保留路径生成逻辑，
    避免旧 migration 引用 `amis_python.models.uuid_filename` 时失效。
    """

    ext = os.path.splitext(filename)[1] or ".ext"
    key = getattr(instance, "key", None) or uuid.uuid4().hex
    now = datetime.datetime.now()
    return f"files/{now:%Y/%m/%d}/{key}{ext}"
