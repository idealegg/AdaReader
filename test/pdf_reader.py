#-- *coding: utf8*--
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import chardet


def pdfParse(path):
  """
  pdf文字提取
  :param path:文件路径
  :return: 每页结果列表
  """
  fp = open(path, 'rb') # 以二进制读模式打开
  # 用文件对象来创建一个pdf文档分析器
  praser = PDFParser(fp)
  # 创建一个PDF文档
  doc = PDFDocument(praser)
  # 连接分析器 与文档对象
  praser.set_document(doc)
  #doc.set_parser(praser)

  # 提供初始化密码
  # 如果没有密码 就创建一个空的字符串
  #doc._initialize_password()

  # 检测文档是否提供txt转换，不提供就忽略
  if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
  else:
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #每页文字内容
    results = []
    # 循环遍历列表，每次处理一个page的内容
    for page in PDFPage.get_pages(fp):  # doc.get_pages() 获取page列表
      interpreter.process_page(page)
      # 接受该页面的LTPage对象
      layout = device.get_result()
      # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
      for x in layout:
        if isinstance(x, LTTextBoxHorizontal):
          txt = x.get_text()
          if type(txt) is not unicode:
            txt_char = chardet.detect(txt)
            txt = txt.decode(txt_char['encoding'])
          print txt
          results.append(txt)
    with open("result.txt", "wb") as out_f:
      out_f.write("\n".join(results).encode('utf8'))
    return results


if __name__ == "__main__":
    pdfParse('ada95RM.pdf')
