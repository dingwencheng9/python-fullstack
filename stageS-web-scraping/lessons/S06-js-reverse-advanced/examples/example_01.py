"""示例代码：控制流平坦化检测与绕过"""
from dataclasses import dataclass


@dataclass
class ControlFlowResult:
    is_flattened: bool
    dispatcher_var: str | None
    state_vars: list[str]


class ControlFlowAnalyzer:
    """控制流平坦化分析器。"""
    
    def detect(self, js_code: str) -> ControlFlowResult:
        """检测代码是否使用控制流平坦化。
        
        特征模式：
        1. 大的 switch-case 结构
        2. 状态变量控制分发
        3. 无意义的函数调用链
        """
        has_switch = "switch" in js_code and "case" in js_code
        has_state_var = "while" in js_code and ("--x" in js_code or "-x" in js_code)
        
        return ControlFlowResult(
            is_flattened=has_switch and has_state_var,
            dispatcher_var="x" if has_state_var else None,
            state_vars=[],  # TODO: 提取所有 case 对应的状态值
        )
    
    def bypass(self, js_code: str) -> str:
        """绕过控制流平坦化。"""
        # TODO: 实现平坦化还原逻辑
        return js_code


if __name__ == "__main__":
    print("控制流平坦化示例")
