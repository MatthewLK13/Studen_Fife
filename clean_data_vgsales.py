import pandas as pd
import numpy as np

def clean_vgsales(input_file, output_file):
    print(f"--- ĐỌC VÀ KHÁM PHÁ DỮ LIỆU ---")
    df = pd.read_csv(input_file)
    print(f"Kích thước ban đầu: {df.shape}")
    
    # 1. Kiểm tra khóa chính (Quang's strength)
    print(f"\n--- KIỂM TRA DỮ LIỆU ---")
    if 'Rank' in df.columns:
        duplicate_ranks = df.duplicated(subset=['Rank']).sum()
        print(f"Số dòng trùng Rank (Primary Key): {duplicate_ranks}")
    
    print(f"Missing values ban đầu:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    # 2. Xử lý kiểu dữ liệu an toàn (Quang & Danh's strength)
    print(f"\n--- XỬ LÝ KIỂU DỮ LIỆU & MISSING VALUES ---")
    # Sử dụng errors='coerce' để test Year
    year_test = pd.to_numeric(df['Year'], errors='coerce')
    invalid_year_count = year_test.isnull().sum() - df['Year'].isnull().sum()
    if invalid_year_count > 0:
        print(f"Phát hiện {invalid_year_count} giá trị Year bị lỗi định dạng.")
    
    # Ép kiểu an toàn
    df['Year'] = year_test
    
    # Xóa missing Year (Khoi's logic for vgsales)
    initial_len = len(df)
    df = df.dropna(subset=['Year'])
    print(f"Đã xóa {initial_len - len(df)} dòng bị thiếu năm phát hành.")
    df['Year'] = df['Year'].astype(int)
    
    # Điền Missing cho Publisher
    df['Publisher'] = df['Publisher'].fillna('Unknown')
    
    # 3. Chuẩn hóa chuỗi (Khoi's strength)
    print(f"\n--- CHUẨN HÓA ĐỊNH DẠNG CHUỖI ---")
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
    
    # 4. Xử lý trùng lặp chuyên sâu (Khoi's strength)
    print(f"\n--- XỬ LÝ TRÙNG LẶP ---")
    dups = df[df.duplicated(subset=['Name', 'Platform'], keep=False)]
    print(f"Phát hiện {len(dups)} dòng trùng lặp (Cùng Game & Platform).")
    
    agg_funcs = {
        'Year': 'first',
        'Genre': 'first',
        'Publisher': 'first',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum',
        'Global_Sales': 'sum'
    }
    df = df.groupby(['Name', 'Platform'], as_index=False).agg(agg_funcs)
    print("Đã gộp thành công các dòng trùng lặp bằng cách cộng dồn doanh thu.")
    
    # 5. Tính toán lại tổng doanh thu (Khoi's strength)
    print(f"\n--- TÍNH TOÁN LẠI TỔNG DOANH THU ---")
    df['Global_Sales'] = df['NA_Sales'] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales']
    
    # Sắp xếp và cấp lại Rank
    df = df.sort_values('Global_Sales', ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1
    
    # Căn chỉnh lại cột
    cols = ['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    df = df[cols]
    
    # 6. Kiểm tra lại và phân tích nhanh (Quang's strength)
    print(f"\n--- KIỂM TRA LẠI DỮ LIỆU SAU KHI CLEAN ---")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Kích thước sau cùng: {df.shape}")
    
    print(f"\n--- EDA CƠ BẢN ---")
    print(f"Số lượng Genre: {df['Genre'].nunique()}")
    print(f"Top 3 Platform:\n{df['Platform'].value_counts().head(3)}")
    
    # Lưu file
    df.to_csv(output_file, index=False)
    print(f"\n✅ Đã lưu file sạch tại: {output_file}")

if __name__ == '__main__':
    clean_vgsales('vgsales.csv', 'vgsales-clean.csv')
