"""示例代码：Smali 基础语法与修改示例"""


SAMPLE_SMALI = """
.method public onCreate(Landroid/os/Bundle;)V
    .locals 2
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    const-string v0, "APP_DEBUG"
    const-string v1, "App started"
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    return-void
.end method
"""


def patch_debug_log(smali_code: str) -> str:
    """移除 Smali 中的调试日志调用。"""
    import re
    # 移除 Log.d 调用
    patched = re.sub(
        r"invoke-static\s+\{[^}]+\},\s*Landroid/util/Log;->d\([^)]+\)\n",
        "",
        smali_code,
    )
    return patched


if __name__ == "__main__":
    print("Smali 逆向示例")
