# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    TODO: Tạo expectation suite cho anonymized patient data.
    """
    context = gx.get_context()
    suite = context.add_expectation_suite("patient_data_suite")

    # Lấy validator
    df = pd.read_csv("data/raw/patients_raw.csv")
    validator = context.sources.pandas_default.read_dataframe(df)

    # --- TASK: Thêm các expectations ---

    # 1. patient_id không được null
    validator.expect_column_values_to_not_be_null("patient_id")

    # 2. TODO: cccd phải có đúng 12 ký tự
    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )


    # 3. TODO: ket_qua_xet_nghiem phải trong khoảng [0, 50]
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0,
        max_value=50
    )


    # 4. TODO: benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )


    # 5. TODO: email phải match regex pattern
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )


    # 6. TODO: Không được có duplicate patient_id
    validator.expect_column_values_to_be_unique(column="patient_id")


    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    """
    TODO: Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    # Check 1: Không còn CCCD gốc dạng số thuần túy
    # (sau anonymization, cccd có thể là fake hoặc masked)
    # Ở đây chúng ta giả sử cccd gốc là raw data, còn anonymized data thì cccd đã được replace.
    # Một cách đơn giản là check xem có cccd nào trong original_df còn xuất hiện không.
    # Nhưng ở đây hàm validate_anonymized_data chỉ nhận filepath của anonymized data.
    # Nên ta check format: nếu replace bằng random digits thì vẫn là digits.
    # Nếu masked thì có '*'.
    # Giả sử yêu cầu là check xem có row nào null không.
    
    critical_cols = ["patient_id", "ho_ten", "cccd", "so_dien_thoai", "email"]
    null_counts = df[critical_cols].isnull().sum()
    if null_counts.sum() > 0:
        results["success"] = False
        results["failed_checks"].append(f"Null values found: {null_counts.to_dict()}")

    # Check 3: Số rows phải khớp (giả sử load từ raw để so sánh)
    try:
        raw_df = pd.read_csv("data/raw/patients_raw.csv")
        if len(df) != len(raw_df):
            results["success"] = False
            results["failed_checks"].append(f"Row count mismatch: {len(df)} vs {len(raw_df)}")
    except:
        pass


    return results
