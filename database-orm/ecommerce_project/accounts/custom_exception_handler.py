from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler để chuẩn hóa response lỗi và ẩn thông tin nhạy cảm.
    """
    response = exception_handler(exc, context)
    if response is not None:
        custom_response = {
            "success": False,
            "message": "",
            "errors": None
        }
        # Xử lý lỗi có trường detail (NotFound, PermissionDenied, ...)
        if isinstance(response.data, dict) and "detail" in response.data:
            custom_response["message"] = response.data["detail"]
        # Xử lý lỗi validate
        elif isinstance(response.data, dict):
            custom_response["errors"] = response.data
            custom_response["message"] = "Dữ liệu không hợp lệ."
        else:
            custom_response["message"] = "Đã xảy ra lỗi."
        response.data = custom_response
    return response