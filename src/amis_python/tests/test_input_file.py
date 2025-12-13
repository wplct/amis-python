from unittest import TestCase

from amis_python.builder.form.input_file import InputFile


class InputFileTestCase(TestCase):
    """文件上传组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        f = InputFile(name="file", label="File", receiver="/api/upload/file")
        self.assertEqual(f.model_dump(), {
            'type': 'input-file', 
            'name': 'file', 
            'label': 'File',
            'receiver': '/api/upload/file'
        })
    
    def test_accept(self):
        """测试接受的文件类型"""
        f = InputFile(name="file", label="File", receiver="/api/upload/file", accept=".csv,.md")
        self.assertEqual(f.model_dump()['accept'], ".csv,.md")
    
    def test_multiple(self):
        """测试多选属性"""
        f = InputFile(name="file", label="File", receiver="/api/upload/file", multiple=True)
        self.assertEqual(f.model_dump()['multiple'], True)
    
    def test_auto_upload(self):
        """测试自动上传属性"""
        f = InputFile(name="file", label="File", receiver="/api/upload/file", auto_upload=False)
        self.assertEqual(f.model_dump()['autoUpload'], False)
    
    def test_as_blob(self):
        """测试作为Blob上传"""
        f = InputFile(name="file", label="File", as_blob=True)
        self.assertEqual(f.model_dump()['asBlob'], True)
    
    def test_as_base64(self):
        """测试作为Base64上传"""
        f = InputFile(name="file", label="File", as_base64=True)
        self.assertEqual(f.model_dump()['asBase64'], True)
    
    def test_drag(self):
        """测试拖拽上传属性"""
        f = InputFile(name="file", label="File", receiver="/api/upload/file", drag=True)
        self.assertEqual(f.model_dump()['drag'], True)
    
    def test_max_size(self):
        """测试最大文件大小"""
        f = InputFile(name="file", label="File", receiver="/api/upload/file", max_size=1048576)
        self.assertEqual(f.model_dump()['maxSize'], 1048576)
    
    def test_chunk_upload(self):
        """测试分块上传"""
        f = InputFile(
            name="file",
            label="File",
            receiver="/api/upload/file",
            use_chunk=True,
            start_chunk_api="/api/upload/start",
            chunk_api="/api/upload/chunk",
            finish_chunk_api="/api/upload/finish",
            concurrency=3,
            chunk_size=5242880
        )
        self.assertEqual(f.model_dump()['useChunk'], True)
        self.assertEqual(f.model_dump()['startChunkApi'], "/api/upload/start")
        self.assertEqual(f.model_dump()['chunkApi'], "/api/upload/chunk")
        self.assertEqual(f.model_dump()['finishChunkApi'], "/api/upload/finish")
        self.assertEqual(f.model_dump()['concurrency'], 3)
        self.assertEqual(f.model_dump()['chunkSize'], 5242880)
    
    def test_file_fields(self):
        """测试文件字段配置"""
        f = InputFile(
            name="file",
            label="File",
            receiver="/api/upload/file",
            file_field="upload_file",
            name_field="filename",
            value_field="file_url",
            url_field="download_url"
        )
        self.assertEqual(f.model_dump()['fileField'], "upload_file")
        self.assertEqual(f.model_dump()['nameField'], "filename")
        self.assertEqual(f.model_dump()['valueField'], "file_url")
        self.assertEqual(f.model_dump()['urlField'], "download_url")
