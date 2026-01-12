class GioHang:
    def __init__(self):
        self.danh_sach_sp = []

    def them_sp(self, ten, gia):
        san_pham = {"ten": ten, "gia": gia}
        self.danh_sach_sp.append(san_pham)

    def dem_sp(self):
        return len(self.danh_sach_sp)

    def xem_gio(self):
        return self.danh_sach_sp

    def xoa_sp(self, ten):
        self.danh_sach_sp = [sp for sp in self.danh_sach_sp if sp["ten"] != ten]

    def tinh_tong(self):
        tong = 0
        for sp in self.danh_sach_sp:
            tong += sp["gia"]
        return tong