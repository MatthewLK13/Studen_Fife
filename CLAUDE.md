# CLAUDE.md - Báo Cáo Quá Trình Xử Lý & Khám Phá Dataset

## 1. Tổng quan Dataset (Dataset Overview)
- **Tên file gốc**: `example-dataset.csv`
- **Tên file sau làm sạch**: `example-dataset-clean.csv`
- **Tổng số dòng (Rows)**: 8,807 dòng
- **Tổng số cột (Columns)**: 12 cột

---

## 2. Danh sách các cột chính, kiểu dữ liệu và ý nghĩa

| Tên cột | Kiểu dữ liệu (Dtype) | Mô tả ý nghĩa |
| :--- | :--- | :--- |
| `show_id` | `object` (string) | Mã định danh duy nhất cho từng bộ phim / chương trình |
| `type` | `object` (categorical) | Phân loại nội dung (`Movie` hoặc `TV Show`) |
| `title` | `object` (string) | Tên bộ phim / chương trình |
| `director` | `object` (string) | Tên đạo diễn sản xuất |
| `cast` | `object` (string) | Danh sách diễn viên tham gia |
| `country` | `object` (string) | Quốc gia sản xuất |
| `date_added` | `object` (datetime string) | Ngày nội dung được cập nhật lên hệ thống |
| `release_year` | `int64` (integer) | Năm phát hành chính thức của nội dung |
| `rating` | `object` (categorical) | Phân loại độ tuổi đối tượng xem (ví dụ: TV-MA, PG-13, R,...) |
| `duration` | `object` (string) | Thời lượng nội dung (phút đối với Movie, số mùa đối với TV Show) |
| `listed_in` | `object` (string) | Thể loại / Danh mục nội dung |
| `description` | `object` (string) | Tóm tắt ngắn gọn nội dung phim |

---

## 3. Các bước làm sạch dữ liệu thực tế (Data Cleaning Steps)

1. **Khám phá ban đầu (`01_explore_data.ipynb`)**:
   - Tải file CSV, kiểm tra kích thước dataset `(8807, 12)` và xác định kiểu dữ liệu của từng cột.

2. **Kiểm tra lỗi dữ liệu (`02_check_errors.ipynb`)**:
   - **Dòng trùng lặp**: Xác nhận 0 dòng trùng lặp hoàn toàn.
   - **Dữ liệu bị thiếu (Missing Values)**:
     - `director`: Khuyết 2,634 giá trị.
     - `country`: Khuyết 831 giá trị.
     - `cast`: Khuyết 825 giá trị.
     - `date_added`: Khuyết 10 giá trị.
     - `rating`: Khuyết 4 giá trị.
     - `duration`: Khuyết 3 giá trị.

3. **Thực hiện làm sạch (`03_clean_data.ipynb`)**:
   - Điền giá trị `"Unknown"` cho các trường văn bản bị thiếu (`director`, `cast`, `country`, `rating`).
   - Xử lý các giá trị khuyết còn lại và đảm bảo kiểu dữ liệu nhất quán.
   - Xuất dữ liệu đã xử lý ra file mới `example-dataset-clean.csv` với tùy chọn `index=False` (không ghi đè file gốc).

---

## 4. Các con số thống kê cốt lõi cần ghi nhớ

- **Tỷ lệ phân bố loại hình nội dung (`type`)**:
  - Phim điện ảnh (**Movie**): **6,131** nội dung (~69.6%)
  - Phim truyền hình / Chương trình (**TV Show**): **2,676** nội dung (~30.4%)
- **Phạm vi thời gian phát hành (`release_year`)**:
  - Năm phát hành cũ nhất: **1925**
  - Năm phát hành mới nhất: **2021**
- **Điểm lưu ý cho phân tích & biểu đồ tiếp theo**:
  - Cột `duration` cần tách số phút đối với Movie và số Season đối với TV Show nếu muốn vẽ biểu đồ phân phối thời lượng.
  - Cột `country` và `listed_in` chứa nhiều giá trị phân cách bởi dấu phẩy, cần tách chuỗi (split) khi phân tích top quốc gia hoặc top thể loại.
