def tamgiac(a, b, c):
    if a+b>c and a+c>b and b+c>a:
        if a==b and b==c:
            loaiTamGiac = 'Tam giác đều'
        elif a==b or a==c or b==c:
            loaiTamGiac = 'Tam giác cân'
        else:
            loaiTamGiac = 'Tam giác thường'
    else:
        loaiTamGiac = 'Không phải là tam giác'
    return loaiTamGiac