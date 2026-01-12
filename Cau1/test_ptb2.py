import unittest
import datetime
import html as html_lib

from ptb2 import ptb2


class TestPTB2(unittest.TestCase):
    def test_delta_greater_than_0(self):
        """Δ > 0: Có 2 nghiệm phân biệt (trả về x1, x2)"""
        a, b, c = 1, 5, 6 
        res = ptb2(a, b, c)
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0], -5.5, places=7)
        self.assertAlmostEqual(res[1], -4.5, places=7)

    def test_delta_equal_0(self):
        """Δ = 0: Có nghiệm kép (trả về x)"""
        a, b, c = 1, 2, 1  
        res = ptb2(a, b, c)
        self.assertIsInstance(res, (int, float))
        self.assertAlmostEqual(res, -1.0, places=7)

    def test_delta_less_than_0(self):
        """Δ < 0: Vô nghiệm thực (trả về 'false')"""
        a, b, c = 1, 1, 1  
        res = ptb2(a, b, c)
        self.assertEqual(res, 'false')


class HTMLTestResult(unittest.TextTestResult):
    """Thu kết quả test để xuất HTML (tiếng Việt)."""
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.rows = []  

    def _ten_test_vi(self, test):
        return test.shortDescription() or test._testMethodName

    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append((self._ten_test_vi(test), "ĐẠT", ""))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        detail = self._exc_info_to_string(err, test)
        self.rows.append((self._ten_test_vi(test), "KHÔNG ĐẠT", detail))

    def addError(self, test, err):
        super().addError(test, err)
        detail = self._exc_info_to_string(err, test)
        self.rows.append((self._ten_test_vi(test), "LỖI", detail))


def write_html_report(result: HTMLTestResult, filename="ketqua.html"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = result.testsRun
    so_khong_dat = len(result.failures)
    so_loi = len(result.errors)
    so_dat = total - so_khong_dat - so_loi

    def esc(s):
        return html_lib.escape(s)

    rows_html = []
    for ten_test, trang_thai, chi_tiet in result.rows:
        chi_tiet_html = f"<pre>{esc(chi_tiet)}</pre>" if chi_tiet else ""
        rows_html.append(
            f"<tr>"
            f"<td>{esc(ten_test)}</td>"
            f"<td><b>{esc(trang_thai)}</b></td>"
            f"<td>{chi_tiet_html}</td>"
            f"</tr>"
        )

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Kết quả kiểm thử - ptb2</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 16px; }}
    .sum {{ margin: 12px 0; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 10px; vertical-align: top; }}
    th {{ background: #f5f5f5; }}
    pre {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h2>KẾT QUẢ KIỂM THỬ HÀM ptb2</h2>
  <div class="sum">
    <div><b>Thời gian:</b> {now}</div>
    <div><b>Tổng số kiểm thử:</b> {total} — <b>ĐẠT:</b> {so_dat} — <b>KHÔNG ĐẠT:</b> {so_khong_dat} — <b>LỖI:</b> {so_loi}</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Trường hợp kiểm thử</th>
        <th>Trạng thái</th>
        <th>Chi tiết</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows_html)}
    </tbody>
  </table>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPTB2)
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=HTMLTestResult,
        descriptions=True 
    )
    result = runner.run(suite)

    write_html_report(result, "ketqua.html")
    print("\nĐã xuất báo cáo: ketqua.html")
