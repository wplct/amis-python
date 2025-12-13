from unittest import TestCase
from amis_python.builder import Tabs, TabsItem, TabsMode


class TabsTestCase(TestCase):
    """
    Tabs组件测试用例
    """
    
    def test_serialize_basic(self):
        """
        测试基本序列化功能
        """
        tabs = Tabs(
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1"),
                TabsItem(title="Tab 2", tab="Content 2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['type'], 'tabs')
        self.assertEqual(len(result['tabs']), 2)
        self.assertEqual(result['tabs'][0]['title'], 'Tab 1')
        self.assertEqual(result['tabs'][0]['tab'], 'Content 1')
        self.assertEqual(result['tabs'][1]['title'], 'Tab 2')
        self.assertEqual(result['tabs'][1]['tab'], 'Content 2')
    
    def test_serialize_with_mode(self):
        """
        测试带有模式的序列化
        """
        tabs = Tabs(
            tabs_mode=TabsMode.LINE,
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1"),
                TabsItem(title="Tab 2", tab="Content 2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['tabsMode'], 'line')
    
    def test_serialize_with_active_key(self):
        """
        测试带有激活键的序列化
        """
        tabs = Tabs(
            active_key="tab2",
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1", hash="tab1"),
                TabsItem(title="Tab 2", tab="Content 2", hash="tab2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['activeKey'], 'tab2')
    
    def test_serialize_with_closable(self):
        """
        测试带有可关闭选项的序列化
        """
        tabs = Tabs(
            closable=True,
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1", closable=False),
                TabsItem(title="Tab 2", tab="Content 2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['closable'], True)
        self.assertEqual(result['tabs'][0]['closable'], False)
        self.assertEqual(result['tabs'][1]['closable'], False)
    
    def test_serialize_with_body(self):
        """
        测试使用body字段的序列化
        """
        tabs = Tabs(
            tabs=[
                TabsItem(
                    title="Tab 1",
                    body={
                        "type": "tpl",
                        "tpl": "Content 1"
                    }
                )
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['tabs'][0]['body']['type'], 'tpl')
        self.assertEqual(result['tabs'][0]['body']['tpl'], 'Content 1')
    
    def test_serialize_with_icon(self):
        """
        测试带有图标的序列化
        """
        tabs = Tabs(
            tabs=[
                TabsItem(
                    title="Tab 1",
                    icon="fa fa-home",
                    tab="Content 1"
                )
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['tabs'][0]['icon'], 'fa fa-home')
    
    def test_serialize_with_toolbar(self):
        """
        测试带有工具栏的序列化
        """
        tabs = Tabs(
            toolbar=[
                {
                    "type": "button",
                    "label": "按钮"
                }
            ],
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(len(result['toolbar']), 1)
        self.assertEqual(result['toolbar'][0]['type'], 'button')
        self.assertEqual(result['toolbar'][0]['label'], '按钮')
    
    def test_serialize_with_addable(self):
        """
        测试带有可添加选项的序列化
        """
        tabs = Tabs(
            addable=True,
            add_btn_text="新增Tab",
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['addable'], True)
        self.assertEqual(result['addBtnText'], '新增Tab')
    
    def test_serialize_with_draggable(self):
        """
        测试带有可拖拽选项的序列化
        """
        tabs = Tabs(
            draggable=True,
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1"),
                TabsItem(title="Tab 2", tab="Content 2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['draggable'], True)
    
    def test_serialize_with_show_tip(self):
        """
        测试带有显示提示选项的序列化
        """
        tabs = Tabs(
            show_tip=True,
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1", tip="提示信息")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['showTip'], True)
        self.assertEqual(result['tabs'][0]['tip'], '提示信息')
    
    def test_serialize_with_on_select(self):
        """
        测试带有选择事件的序列化
        """
        tabs = Tabs(
            on_select="alert(key)",
            tabs=[
                TabsItem(title="Tab 1", tab="Content 1"),
                TabsItem(title="Tab 2", tab="Content 2")
            ]
        )
        
        result = tabs.model_dump(mode='json')
        self.assertEqual(result['onSelect'], 'alert(key)')
