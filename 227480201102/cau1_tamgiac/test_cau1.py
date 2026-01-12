import unittest
import datetime
from cau1 import tamgiac 


class HTMLResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.rows = [] 

    def get_test_name(self, test):
        
        return test._testMethodName

    def addSuccess(self, test):
        self.rows.append((self.get_test_name(test), "ĐẠT", ""))

    def addFailure(self, test, err):
        
        full_msg = str(err[1])
        short_msg = full_msg.split('\n')[0].replace("AssertionError: ", "")
        self.rows.append((self.get_test_name(test), "KHÔNG ĐẠT", short_msg))

    def addError(self, test, err):
        self.rows.append((self.get_test_name(test), "LỖI", str(err[1])))


class TestTamGiac(unittest.TestCase):
    
    def test_tam_giac_deu(self):
        self.assertEqual(tamgiac(3, 9, 3), 'Tam giác đều')

    def test_tam_giac_can(self):
        self.assertEqual(tamgiac(3, 3, 4), 'Tam giác cân')
        self.assertEqual(tamgiac(3, 4, 3), 'Tam giác cân')
        self.assertEqual(tamgiac(4, 3, 3), 'Tam giác cân')

    def test_tam_giac_thuong(self):
        self.assertEqual(tamgiac(3, 4, 5), 'Tam giác thường')

    def test_khong_phai_tam_giac_bang(self):
        self.assertEqual(tamgiac(1, 2, 3), 'Không phải là tam giác')

    def test_khong_phai_tam_giac_nho_hon(self):
        self.assertEqual(tamgiac(1, 2, 10), 'Không phải là tam giác')

    def test_canh_am_hoac_khong(self):
        self.assertEqual(tamgiac(0, 1, 2), 'Không phải là tam giác')
        self.assertEqual(tamgiac(-1, 2, 3), 'Không phải là tam giác')


if __name__ == '__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTamGiac)
    result_capturer = HTMLResult()
    suite.run(result_capturer)

    
    total = len(result_capturer.rows)
    passed = sum(1 for r in result_capturer.rows if r[1] == "ĐẠT")
    fails = sum(1 for r in result_capturer.rows if r[1] == "KHÔNG ĐẠT")
    errors = sum(1 for r in result_capturer.rows if r[1] == "LỖI")
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    table_rows_html = ""
    for name, status, detail in result_capturer.rows:
        if status == "ĐẠT":
            color = "green"
        elif status == "KHÔNG ĐẠT":
            color = "red"
        else:
            color = "orange"
            
        table_rows_html += f"""
        <tr>
            <td>{name}</td>
            <td style="color: {color}; font-weight: bold;">{status}</td>
            <td>{detail}</td> 
        </tr>"""

    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Kết quả kiểm thử Tam Giác</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9; }}
    h2 {{ color: #333; }}
    .sum {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; background: #fff; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }}
    th {{ background-color: #007bff; color: white; }}
    tr:nth-child(even) {{ background-color: #f9f9f9; }}
  </style>
</head>
<body>
  <h2>KẾT QUẢ KIỂM THỬ: BÀI TOÁN TAM GIÁC</h2>
  
  <div class="sum">
    <p><b>Thời gian chạy:</b> {now}</p>
    <p>
        <b>Tổng số test:</b> {total} &nbsp;|&nbsp; 
        <b style="color:green">ĐẠT: {passed}</b> &nbsp;|&nbsp; 
        <b style="color:red">KHÔNG ĐẠT: {fails}</b> &nbsp;|&nbsp; 
        <b style="color:orange">LỖI: {errors}</b>
    </p>
  </div>

  <table>
    <thead>
      <tr>
        <th width="35%">Tên hàm test</th>
        <th width="15%">Trạng thái</th>
        <th>Chi tiết lỗi</th>
      </tr>
    </thead>
    <tbody>
      {table_rows_html}
    </tbody>
  </table>
</body>
</html>
"""

    with open('ketqua.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Đã xuất file ketqua.html với giao diện bảng đẹp.")