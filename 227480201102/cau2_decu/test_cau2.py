import pytest
from unittest.mock import MagicMock
from cau2 import GioHang

@pytest.fixture
def gio_hang():
    gh = GioHang()
    return gh

def test_them_va_dem_sp(gio_hang):
    gio_hang.them_sp("Iphone 15", 30000)
    gio_hang.them_sp("Samsung S24", 25000)
    
    assert gio_hang.dem_sp() == 2

def test_xem_gio_hang(gio_hang):
    gio_hang.them_sp("Laptop Dell", 15000)
    danh_sach = gio_hang.xem_gio()
    
    assert len(danh_sach) == 1
    assert danh_sach[0]["ten"] == "Laptop Dell"

def test_xoa_sp(gio_hang):
    gio_hang.them_sp("Chuot Logitech", 500)
    gio_hang.them_sp("Ban phim Co", 1000)
    
    gio_hang.xoa_sp("Chuot Logitech")
    
    assert gio_hang.dem_sp() == 1
    assert gio_hang.xem_gio()[0]["ten"] == "Ban phim Co"

def test_tinh_tong_tien(gio_hang):
    gio_hang.them_sp("Sach", 100)
    gio_hang.them_sp("Vo", 50)
    
    assert gio_hang.tinh_tong() == 150

def test_mock_tinh_tong(gio_hang):
    gio_hang.tinh_tong = MagicMock(return_value=999999)
    
    ket_qua = gio_hang.tinh_tong()
    
    assert ket_qua == 999999
    gio_hang.tinh_tong.assert_called_once()

if __name__ == "__main__":
    pytest.main(["-v", "test_cau2.py"])