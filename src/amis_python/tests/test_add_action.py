from unittest import TestCase

from amis_python.builder import Button, EventAction


class AddActionTestCase(TestCase):
    """add_action 方法测试"""
    
    def test_add_single_action(self):
        """测试添加单个动作到事件"""
        # 创建按钮组件
        button = Button(label="点击我")
        
        # 创建 toast 动作
        toast_action = EventAction(
            action_type="toast",
            args={
                "msgType": "success",
                "msg": "点击成功！"
            }
        )
        
        # 添加动作到点击事件
        button.add_action("click", toast_action)
        
        # 验证结果
        result = button.model_dump()
        self.assertIn("onEvent", result)
        self.assertIn("click", result["onEvent"])
        self.assertIn("actions", result["onEvent"]["click"])
        self.assertEqual(len(result["onEvent"]["click"]["actions"]), 1)
        
        action = result["onEvent"]["click"]["actions"][0]
        self.assertEqual(action["actionType"], "toast")
        self.assertEqual(action["args"]["msgType"], "success")
        self.assertEqual(action["args"]["msg"], "点击成功！")
    
    def test_add_multiple_actions(self):
        """测试添加多个动作到同一个事件"""
        # 创建按钮组件
        button = Button(label="点击我")
        
        # 创建 toast 动作
        toast_action = EventAction(
            action_type="toast",
            args={
                "msgType": "success",
                "msg": "点击成功！"
            }
        )
        
        # 创建 dialog 动作
        dialog_action = EventAction(
            action_type="dialog",
            dialog={
                "title": "提示",
                "body": "这是一个提示对话框"
            }
        )
        
        # 添加动作到点击事件
        button.add_action("click", toast_action)
        button.add_action("click", dialog_action)
        
        # 验证结果
        result = button.model_dump()
        self.assertEqual(len(result["onEvent"]["click"]["actions"]), 2)
        
        # 验证第一个动作
        action1 = result["onEvent"]["click"]["actions"][0]
        self.assertEqual(action1["actionType"], "toast")
        
        # 验证第二个动作
        action2 = result["onEvent"]["click"]["actions"][1]
        self.assertEqual(action2["actionType"], "dialog")
        self.assertEqual(action2["dialog"]["title"], "提示")
    
    def test_chain_calling(self):
        """测试链式调用"""
        # 创建按钮组件并链式添加动作
        button = Button(label="点击我")\
            .add_action(
                "click",
                EventAction(
                    action_type="toast",
                    args={"msgType": "success", "msg": "第一个动作"}
                )
            )\
            .add_action(
                "click",
                EventAction(
                    action_type="toast",
                    args={"msgType": "info", "msg": "第二个动作"}
                )
            )\
            .add_action(
                "mouseenter",
                EventAction(
                    action_type="toast",
                    args={"msgType": "warning", "msg": "鼠标移入"}
                )
            )
        
        # 验证结果
        result = button.model_dump()
        self.assertEqual(len(result["onEvent"]["click"]["actions"]), 2)
        self.assertEqual(len(result["onEvent"]["mouseenter"]["actions"]), 1)
    
    def test_ajax_action(self):
        """测试 ajax 动作"""
        # 创建按钮组件
        button = Button(label="提交")
        
        # 创建 ajax 动作
        ajax_action = EventAction(
            action_type="ajax",
            api="/api/save",
            method="post",
            data={"name": "test"},
            messages={"success": "保存成功", "failed": "保存失败"}
        )
        
        # 添加动作到点击事件
        button.add_action("click", ajax_action)
        
        # 验证结果
        result = button.model_dump()
        action = result["onEvent"]["click"]["actions"][0]
        self.assertEqual(action["actionType"], "ajax")
        self.assertEqual(action["api"], "/api/save")
        self.assertEqual(action["messages"]["success"], "保存成功")
    
    def test_dialog_action(self):
        """测试 dialog 动作"""
        # 创建按钮组件
        button = Button(label="打开弹窗")
        
        # 创建 dialog 动作
        dialog_action = EventAction(
            action_type="dialog",
            dialog={
                "title": "测试弹窗",
                "body": "这是一个测试弹窗内容"
            }
        )
        
        # 添加动作到点击事件
        button.add_action("click", dialog_action)
        
        # 验证结果
        result = button.model_dump()
        action = result["onEvent"]["click"]["actions"][0]
        self.assertEqual(action["actionType"], "dialog")
        self.assertEqual(action["dialog"]["title"], "测试弹窗")
        self.assertEqual(action["dialog"]["body"], "这是一个测试弹窗内容")
    
    def test_toast_action(self):
        """测试 toast 动作"""
        # 创建按钮组件
        button = Button(label="提示")
        
        # 创建 toast 动作
        toast_action = EventAction(
            action_type="toast",
            args={
                "msgType": "success",
                "msg": "操作成功！",
                "position": "top-right"
            }
        )
        
        # 添加动作到点击事件
        button.add_action("click", toast_action)
        
        # 验证结果
        result = button.model_dump()
        action = result["onEvent"]["click"]["actions"][0]
        self.assertEqual(action["actionType"], "toast")
        self.assertEqual(action["args"]["msgType"], "success")
        self.assertEqual(action["args"]["msg"], "操作成功！")
        self.assertEqual(action["args"]["position"], "top-right")