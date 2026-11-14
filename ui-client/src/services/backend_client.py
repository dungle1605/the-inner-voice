import requests
from typing import List, Dict, Any, Tuple

class BackendApiClient:
    def __init__(self, dotnet_url: str = "http://localhost:5000/api/chat", fastapi_fallback_url: str = "http://localhost:8000/api/chat"):
        self.dotnet_url = dotnet_url
        self.fastapi_fallback_url = fastapi_fallback_url

    def send_chat_message(self, session_id: str, message: str, history: List[Dict[str, str]]) -> Tuple[str, str, bool]:
        """
        Gửi tin nhắn sang .NET 10 backend với fallback sang FastAPI nếu .NET chưa khởi chạy.
        Trả về: (reply_text, risk_level, is_emergency)
        """
        payload = {
            "sessionId": session_id,
            "message": message,
            "history": history
        }

        # 1. Thử gọi .NET 10 Backend
        try:
            res = requests.post(self.dotnet_url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                return (
                    data.get("response", ""),
                    data.get("riskLevel", "Low"),
                    data.get("isEmergency", False)
                )
        except Exception:
            pass

        # 2. Fallback trực tiếp gọi FastAPI AI Microservice
        try:
            res_py = requests.post(self.fastapi_fallback_url, json=payload, timeout=20)
            if res_py.status_code == 200:
                data_py = res_py.json()
                return (
                    data_py.get("response", ""),
                    data_py.get("risk_level", "Low"),
                    data_py.get("is_emergency", False)
                )
        except Exception:
            pass

        # 3. Phản hồi dự phòng an toàn tuyệt đối
        return (
            "Mình đang gặp chút trục trặc mạng nhưng mình luôn ở đây vì bạn. Bạn hãy hít thở sâu một nhịp nhé.",
            "Low",
            False
        )
