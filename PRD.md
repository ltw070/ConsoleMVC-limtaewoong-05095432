# PRD: ConsoleMVC 스켈레톤

> **PoC 목표**: Model / Controller / View 레이어의 패키지 구조와 역할 분리를 완성한다.  
> **최종 목적지**: 이 구조가 `mission2/SampleOrderSystem` 의 뼈대가 된다.

---

## 1. 개요

반도체 시료 생산주문관리 시스템의 콘솔 기반 MVC 아키텍처를 설계한다.  
각 레이어는 단방향 의존성을 유지하며, 인터페이스(추상 클래스)를 통해 결합도를 낮춘다.

```
View  ←──  Controller  ──→  Model
            (단방향 의존, View는 Controller를 모름)
```

---

## 2. 패키지 구조

```
01_ConsoleMVC/
├── app/
│   ├── model/
│   │   ├── sample.py          # Sample 도메인 객체
│   │   ├── order.py           # Order 도메인 객체
│   │   ├── production.py      # ProductionQueue 도메인 객체
│   │   └── enums.py           # OrderStatus Enum
│   ├── controller/
│   │   ├── base_controller.py # 추상 Controller
│   │   ├── sample_controller.py
│   │   ├── order_controller.py
│   │   └── production_controller.py
│   └── view/
│       ├── base_view.py       # 추상 View (입출력 인터페이스)
│       ├── main_view.py       # 메인 메뉴
│       ├── sample_view.py     # 시료 관리 화면
│       ├── order_view.py      # 주문 화면
│       ├── monitor_view.py    # 모니터링 화면
│       ├── production_view.py # 생산라인 화면
│       └── shipment_view.py   # 출고 처리 화면
├── tests/
│   ├── test_model/
│   ├── test_controller/
│   └── test_view/
├── main.py
└── requirements.txt
```

---

## 3. 도메인 모델 (전체 프로젝트 공통 Interface)

> PoC2 · PoC3 · PoC4 · Mission2 모두 아래 모델을 기준으로 한다.

### 3.1 Sample

```python
@dataclass
class Sample:
    id: str                  # 형식: "S-001" ~ "S-999"
    name: str
    avg_production_time: float   # 단위: min/ea, 양수
    yield_rate: float            # 범위: 0 < yield_rate <= 1
    stock: int                   # 단위: ea, 0 이상
```

### 3.2 OrderStatus (Enum)

```python
class OrderStatus(Enum):
    RESERVED  = "RESERVED"   # 주문 접수
    REJECTED  = "REJECTED"   # 주문 거절 (모니터링 제외)
    PRODUCING = "PRODUCING"  # 재고 부족, 생산 중
    CONFIRMED = "CONFIRMED"  # 출고 대기
    RELEASE   = "RELEASE"    # 출고 완료
```

### 3.3 Order

```python
@dataclass
class Order:
    order_no: str            # 형식: "ORD-YYYYMMDD-XXXX" (4자리 순번)
    sample_id: str           # Sample.id 참조
    customer_name: str
    quantity: int            # 양수
    status: OrderStatus      # 초기값: RESERVED
    created_at: datetime
```

### 3.4 ProductionItem

```python
@dataclass
class ProductionItem:
    order_no: str
    sample_id: str
    shortage: int            # 부족분 = 주문량 - 재고
    actual_qty: int          # 실 생산량 = ceil(shortage / (yield_rate * 0.9))
    total_time: float        # 총 생산 시간 = avg_production_time * actual_qty (min)
```

**생산량 계산식**
```
실 생산량  = ceil(부족분 / (수율 × 0.9))
총 생산시간 = 평균_생산시간(min/ea) × 실_생산량
```

---

## 4. Controller 인터페이스

### 4.1 BaseController

```python
class BaseController(ABC):
    @abstractmethod
    def run(self) -> None: ...
```

### 4.2 SampleController

```python
class SampleController(BaseController):
    def register_sample(self, id, name, avg_time, yield_rate) -> Sample: ...
    def list_samples(self) -> list[Sample]: ...
    def search_samples(self, keyword: str) -> list[Sample]: ...
```

### 4.3 OrderController

```python
class OrderController(BaseController):
    def place_order(self, sample_id, customer, qty) -> Order: ...
    def list_reserved(self) -> list[Order]: ...
    def approve_order(self, order_no: str) -> Order: ...   # 재고 확인 후 CONFIRMED or PRODUCING
    def reject_order(self, order_no: str) -> Order: ...
    def ship_order(self, order_no: str) -> Order: ...      # CONFIRMED → RELEASE
```

### 4.4 ProductionController

```python
class ProductionController(BaseController):
    def get_current(self) -> ProductionItem | None: ...
    def get_queue(self) -> list[ProductionItem]: ...       # FIFO 순
    def complete_production(self, order_no: str) -> None: ... # PRODUCING → CONFIRMED
```

---

## 5. View 인터페이스

```python
class BaseView(ABC):
    @abstractmethod
    def display(self, data: Any) -> str: ...   # 출력 문자열 반환 (테스트 가능)

    @abstractmethod
    def get_input(self, prompt: str) -> str: ...
```

- `display()` 는 `print()` 대신 문자열을 **반환**한다 → 단위 테스트 가능
- `get_input()` 은 테스트 시 Mock으로 대체한다

---

## 6. 메인 메뉴 흐름

```
main.py
  └─ MainView.display()       # 시스템 현황 + 메뉴 출력
       ├─ [1] SampleController.run()
       ├─ [2] OrderController.run()        (주문 접수)
       ├─ [3] OrderController.run()        (승인/거절)
       ├─ [4] MonitorView.display()
       ├─ [5] ProductionController.run()
       ├─ [6] OrderController.run()        (출고 처리)
       └─ [0] 종료
```

---

## 7. 검증 기준 (TDD)

| 테스트 | 검증 내용 |
|--------|----------|
| `test_sample_model` | id 형식, yield_rate 범위, stock 음수 방지 |
| `test_order_model` | order_no 형식, 상태 전이 유효성 |
| `test_production_item` | 생산량 계산식 (`ceil(shortage / (yield * 0.9))`) |
| `test_sample_controller` | register → list → search 흐름 |
| `test_order_controller` | place → approve(재고 충분) → CONFIRMED, place → approve(재고 부족) → PRODUCING |
| `test_view_display` | `display()` 가 문자열을 반환하는지 확인 |

커버리지 목표: **80% 이상**
