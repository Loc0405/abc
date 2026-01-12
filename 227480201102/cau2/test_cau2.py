import sqlite3
import os
import pytest

# 1. Thiết lập đường dẫn (Giữ nguyên logic xác định vị trí file)
cau2_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(cau2_dir, "QuanLyDiem.db")
file_cau1 = os.path.join(cau2_dir, "Ketqua_cau2.txt")
file_22 = os.path.join(cau2_dir, "Ketqua_22.txt")

# 2. Fixture khởi tạo Database (Giữ nguyên logic tạo bảng và chèn dữ liệu mẫu)
@pytest.fixture(scope="module")
def conn():
    # Khởi tạo tiêu đề cho các file kết quả
    with open(file_cau1, "w", encoding="utf-8") as f: f.write("1/- KẾT QUẢ KIỂM TRA TRÙNG MÃ SV\n")
    with open(file_22, "w", encoding="utf-8") as f: f.write("2/- KẾT QUẢ KIỂM THỬ STORE PROCEDURE\n")
    
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    
    cur.executescript("""
        DROP TABLE IF EXISTS KETQUA; DROP TABLE IF EXISTS SINHVIEN;
        DROP TABLE IF EXISTS LOP; DROP TABLE IF EXISTS MOHOC;
        
        CREATE TABLE LOP(MALOP TEXT PRIMARY KEY, TENLOP TEXT, SISO INTEGER);
        CREATE TABLE SINHVIEN(MASV TEXT PRIMARY KEY, HOTEN TEXT, NGAYSINH TEXT, TINH TEXT, MALOP TEXT);
        CREATE TABLE MOHOC(MAMH TEXT PRIMARY KEY, TENMH TEXT, SOTC INTEGER);
        CREATE TABLE KETQUA(MASV TEXT, MAMH TEXT, LANTHI INTEGER, DIEM REAL, PRIMARY KEY(MASV, MAMH, LANTHI));
        
        INSERT INTO LOP VALUES ('L01','16DTH3',40);
        INSERT INTO MOHOC VALUES ('MH01','Cơ sở dữ liệu',3);
        INSERT INTO SINHVIEN VALUES ('SV01','Nguyen A','2001-01-01','CT','L01');
        INSERT INTO SINHVIEN VALUES ('SV02','Tran B','2001-02-02','AG','L01');
        
        -- Nhập điểm: SV02 cao nhất (9.5), SV01 thấp hơn (7.0)
        INSERT INTO KETQUA VALUES ('SV01','MH01',1,7.0);
        INSERT INTO KETQUA VALUES ('SV02','MH01',1,9.5);
    """)
    connection.commit()
    yield connection
    connection.close()

# 3. Hàm xử lý chính (Giữ nguyên logic truy vấn tìm SV điểm cao nhất)
def exec_sp(conn, tenlop='16DTH3', tenmh='Cơ sở dữ liệu'):
    cur = conn.cursor()
    cur.execute("SELECT MAMH FROM MOHOC WHERE TENMH=?", (tenmh,))
    row = cur.fetchone()
    if not row: return []
    mamh = row[0]
    
    cur.execute("""
        SELECT SV.MASV, SV.HOTEN, L.TENLOP, KQ.DIEM
        FROM SINHVIEN SV, LOP L, KETQUA KQ
        WHERE SV.MALOP = L.MALOP AND SV.MASV = KQ.MASV
        AND L.TENLOP = ? AND KQ.MAMH = ?
        AND KQ.DIEM = (
            SELECT MAX(KQ2.DIEM) FROM KETQUA KQ2 
            JOIN SINHVIEN SV2 ON KQ2.MASV = SV2.MASV JOIN LOP L2 ON SV2.MALOP = L2.MALOP
            WHERE L2.TENLOP = ? AND KQ2.MAMH = ?
        )
    """, (tenlop, mamh, tenlop, mamh))
    
    cols = [column[0] for column in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]

# 4. Các bài kiểm thử (Giữ nguyên logic assert và ghi file)
def test_duplicate_primary_key(conn):
    """Câu 1: Test trùng khóa chính"""
    cursor = conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO SINHVIEN(MASV) VALUES ('SV01')")
        conn.commit()
    with open(file_cau1, "a", encoding="utf-8") as f:
        f.write("PASS: Đã bắt được lỗi trùng mã SV thành công.\n")

def test_thanh_cong(conn):
    """Câu 2: Test đúng dữ liệu"""
    result = exec_sp(conn, '16DTH3', 'Cơ sở dữ liệu')
    assert len(result) == 1
    assert result[0]['MASV'] == 'SV02'
    with open(file_22, "a", encoding="utf-8") as f:
        f.write(f"- Đúng: Tìm thấy SV {result[0]['MASV']} điểm cao nhất.\n")

def test_Lopkhongtontai(conn):
    """Câu 2: Test tên lớp không tồn tại"""
    result = exec_sp(conn, 'LOP_SAI', 'Cò sở dữ liệu')
    assert len(result) == 0
    with open(file_22, "a", encoding="utf-8") as f:
        f.write("- Sai lớp: PASS (Không có dữ liệu)\n")

def test_sp_nhieussvcodiemcao(conn):
    """Câu 2: Test nhiều SV điểm cao bằng nhau"""
    cursor = conn.cursor()
    cursor.execute("UPDATE KETQUA SET DIEM=9.5 WHERE MASV='SV01'")
    conn.commit()
    
    result = exec_sp(conn, '16DTH3', 'Cơ sở dữ liệu')
    assert len(result) == 2
    with open(file_22, "a", encoding="utf-8") as f:
        f.write(f"- Trùng điểm: PASS (Tìm thấy {len(result)} SV cùng điểm cao nhất).\n")
if __name__ == "__main__":
    pytest.main([__file__])