"""OrderStatus enum for the semiconductor sample order management system."""
from enum import Enum


class OrderStatus(Enum):
    RESERVED = "RESERVED"   # 주문 접수
    REJECTED = "REJECTED"   # 주문 거절 (모니터링 제외)
    PRODUCING = "PRODUCING"  # 재고 부족, 생산 중
    CONFIRMED = "CONFIRMED"  # 출고 대기
    RELEASE = "RELEASE"     # 출고 완료
