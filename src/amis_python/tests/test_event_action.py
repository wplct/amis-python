from __future__ import annotations
import unittest
from amis_python.builder import ButtonBuilder, EventAction


class TestEventAction(unittest.TestCase):
    """测试事件动作功能"""
    
    def test_event_action_creation(self):
        """测试EventAction模型创建"""
        event_action = EventAction(
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "info",
                        "msg": "点击事件触发"
                    }
                }
            ]
        )
        
        self.assertIsNotNone(event_action)
        self.assertEqual(len(event_action.actions), 1)
        self.assertEqual(event_action.actions[0]["actionType"], "toast")
        
        # 测试序列化
        event_dict = event_action.model_dump()
        self.assertIsNotNone(event_dict["actions"])
        self.assertEqual(len(event_dict["actions"]), 1)
    
    def test_button_with_event(self):
        """测试带事件动作的按钮创建"""
        # 创建事件动作配置
        event_action = EventAction(
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "info",
                        "msg": "点击事件触发"
                    }
                }
            ]
        )
        
        # 创建带有事件动作的按钮
        button = ButtonBuilder(
            label="测试按钮",
            on_event={"click": event_action}
        )
        
        # 生成schema
        schema = button.to_schema()
        
        # 验证结果
        self.assertEqual(schema["type"], "button")
        self.assertIn("onEvent", schema)  # 验证snake_case转camelCase
        self.assertIn("click", schema["onEvent"])
        self.assertEqual(len(schema["onEvent"]["click"]["actions"]), 1)
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["actionType"], "toast")
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["args"]["msg"], "点击事件触发")
    
    def test_multiple_events(self):
        """测试多个事件配置"""
        # 创建点击事件
        click_event = EventAction(
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "info",
                        "msg": "点击事件触发"
                    }
                }
            ]
        )
        
        # 创建鼠标移入事件
        mouseenter_event = EventAction(
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "warning",
                        "msg": "鼠标移入事件触发"
                    }
                }
            ]
        )
        
        # 创建带有多个事件的按钮
        button = ButtonBuilder(
            label="测试按钮",
            on_event={
                "click": click_event,
                "mouseenter": mouseenter_event
            }
        )
        
        # 生成schema
        schema = button.to_schema()
        
        # 验证结果
        self.assertEqual(schema["type"], "button")
        self.assertIn("onEvent", schema)
        self.assertIn("click", schema["onEvent"])
        self.assertIn("mouseenter", schema["onEvent"])
        self.assertEqual(len(schema["onEvent"]["click"]["actions"]), 1)
        self.assertEqual(len(schema["onEvent"]["mouseenter"]["actions"]), 1)
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["args"]["msg"], "点击事件触发")
        self.assertEqual(schema["onEvent"]["mouseenter"]["actions"][0]["args"]["msg"], "鼠标移入事件触发")
    
    def test_add_action_method(self):
        """测试add_action方法"""
        # 创建按钮
        button = ButtonBuilder(label="测试按钮")
        
        # 使用add_action方法添加点击事件
        button.add_action(
            event_name="click",
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "success",
                        "msg": "add_action方法测试成功"
                    }
                }
            ]
        )
        
        # 生成schema
        schema = button.to_schema()
        
        # 验证结果
        self.assertEqual(schema["type"], "button")
        self.assertIn("onEvent", schema)
        self.assertIn("click", schema["onEvent"])
        self.assertEqual(len(schema["onEvent"]["click"]["actions"]), 1)
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["actionType"], "toast")
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["args"]["msg"], "add_action方法测试成功")
    
    def test_add_action_chaining(self):
        """测试add_action方法的链式调用"""
        # 创建按钮并链式添加多个事件
        button = ButtonBuilder(label="测试按钮")
        button.add_action(
            event_name="click",
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "success",
                        "msg": "点击事件"
                    }
                }
            ]
        ).add_action(
            event_name="mouseenter",
            actions=[
                {
                    "actionType": "toast",
                    "args": {
                        "msgType": "info",
                        "msg": "鼠标移入事件"
                    }
                }
            ]
        )
        
        # 生成schema
        schema = button.to_schema()
        
        # 验证结果
        self.assertEqual(schema["type"], "button")
        self.assertIn("onEvent", schema)
        self.assertIn("click", schema["onEvent"])
        self.assertIn("mouseenter", schema["onEvent"])
        self.assertEqual(len(schema["onEvent"]["click"]["actions"]), 1)
        self.assertEqual(len(schema["onEvent"]["mouseenter"]["actions"]), 1)
        self.assertEqual(schema["onEvent"]["click"]["actions"][0]["args"]["msg"], "点击事件")
        self.assertEqual(schema["onEvent"]["mouseenter"]["actions"][0]["args"]["msg"], "鼠标移入事件")


if __name__ == '__main__':
    unittest.main()

