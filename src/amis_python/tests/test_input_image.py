from unittest import TestCase

from amis_python.builder.form.input_image import InputImage


class InputImageTestCase(TestCase):
    """图片上传组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        f = InputImage(name="image", label="image", receiver="/api/upload/file")
        self.assertEqual(f.model_dump(), {
            'type': 'input-image', 
            'name': 'image', 
            'label': 'image',
            'receiver': '/api/upload/file'
        })
    
    def test_accept(self):
        """测试接受的文件类型"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", accept=".jpg,.png")
        self.assertEqual(f.model_dump()['accept'], ".jpg,.png")
    
    def test_multiple(self):
        """测试多选属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", multiple=True)
        self.assertEqual(f.model_dump()['multiple'], True)
    
    def test_auto_upload(self):
        """测试自动上传属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", auto_upload=False)
        self.assertEqual(f.model_dump()['autoUpload'], False)
    
    def test_crop(self):
        """测试裁剪属性"""
        # 简单裁剪
        f1 = InputImage(name="image", label="image", receiver="/api/upload/file", crop=True)
        self.assertEqual(f1.model_dump()['crop'], True)
        
        # 带配置的裁剪
        f2 = InputImage(name="image", label="image", receiver="/api/upload/file", crop={"aspectRatio": 1.7777})
        self.assertEqual(f2.model_dump()['crop'], {"aspectRatio": 1.7777})
    
    def test_max_size(self):
        """测试最大文件大小"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", max_size=1024)
        self.assertEqual(f.model_dump()['maxSize'], 1024)
    
    def test_draggable(self):
        """测试拖拽排序属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", draggable=True)
        self.assertEqual(f.model_dump()['draggable'], True)
    
    def test_hide_upload_button(self):
        """测试隐藏上传按钮属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", auto_upload=False, hide_upload_button=True)
        self.assertEqual(f.model_dump()['hideUploadButton'], True)
    
    def test_init_auto_fill(self):
        """测试初始化自动填充属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", init_auto_fill=True)
        self.assertEqual(f.model_dump()['initAutoFill'], True)
    
    def test_limit(self):
        """测试图片限制属性"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", limit={"minWidth": 1000})
        self.assertEqual(f.model_dump()['limit'], {"minWidth": 1000})
    
    def test_upload_btn_text(self):
        """测试上传按钮文案"""
        f = InputImage(name="image", label="image", receiver="/api/upload/file", upload_btn_text="上传图片")
        self.assertEqual(f.model_dump()['uploadBtnText'], "上传图片")
