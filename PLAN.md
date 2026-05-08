# PLAN: ConsoleMVC 스켈레톤

## 목표

Model / Controller / View 레이어의 패키지 구조와 역할 분리를 완성하여 `mission2/SampleOrderSystem`의 뼈대를 구성한다.

---

## 구현 순서 (TDD: Red → Green → Refactor)

### Phase 1 – 도메인 모델

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_model/test_enums.py` | OrderStatus 5개 멤버(RESERVED/REJECTED/PRODUCING/CONFIRMED/RELEASE) 테스트 |
| Green | `app/model/enums.py` | OrderStatus Enum 구현 |
| Red | `tests/test_model/test_sample.py` | id 형식(`S-\d{3}`), yield_rate 범위(0<v≤1), stock 음수 방지 테스트 |
| Green | `app/model/sample.py` | Sample dataclass 구현 (유효성 검사 포함) |
| Red | `tests/test_model/test_order.py` | order_no 형식(`ORD-YYYYMMDD-XXXX`), 상태 전이 유효성, quantity 양수 테스트 |
| Green | `app/model/order.py` | Order dataclass 구현 |
| Red | `tests/test_model/test_production.py` | `ceil(shortage / (yield_rate × 0.9))` 계산식, total_time 계산 테스트 |
| Green | `app/model/production.py` | ProductionItem dataclass 구현 |
| Refactor | `app/model/` | 공통 유효성 검사 로직 정리 |

### Phase 2 – Controller 인터페이스

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_controller/test_base_controller.py` | BaseController 추상 메서드 `run()` 테스트 |
| Green | `app/controller/base_controller.py` | BaseController ABC 구현 |
| Red | `tests/test_controller/test_sample_controller.py` | `register → list → search` 흐름 테스트 |
| Green | `app/controller/sample_controller.py` | SampleController 구현 |
| Red | `tests/test_controller/test_order_controller.py` | `place → approve(재고 충분) → CONFIRMED` 테스트, `place → approve(재고 부족) → PRODUCING` 테스트 |
| Green | `app/controller/order_controller.py` | OrderController 구현 (approve 시 재고 분기 로직 포함) |
| Red | `tests/test_controller/test_production_controller.py` | FIFO 큐, `complete_production` 상태 전이(PRODUCING→CONFIRMED) 테스트 |
| Green | `app/controller/production_controller.py` | ProductionController 구현 |
| Refactor | `app/controller/` | 의존성 주입 방식 통일 |

### Phase 3 – View 인터페이스

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_view/test_base_view.py` | `display()` 반환 타입 str, `get_input()` 인터페이스 테스트 |
| Green | `app/view/base_view.py` | BaseView ABC 구현 |
| Red | `tests/test_view/test_main_view.py` | `display()` 가 문자열을 반환하는지 확인 (print() 직접 호출 없음) |
| Green | `app/view/main_view.py` | MainView 구현 (시스템 현황 + 메뉴 출력) |
| Red | `tests/test_view/test_sample_view.py` | SampleView display 문자열 반환 테스트 |
| Green | `app/view/sample_view.py` | SampleView 구현 |
| Red | `tests/test_view/test_order_view.py` | OrderView display 문자열 반환 테스트 |
| Green | `app/view/order_view.py` | OrderView 구현 |
| Green | `app/view/monitor_view.py` | MonitorView 구현 (REJECTED 제외) |
| Green | `app/view/production_view.py` | ProductionView 구현 |
| Green | `app/view/shipment_view.py` | ShipmentView 구현 |
| Refactor | `app/view/` | 공통 포맷팅 유틸 분리 |

### Phase 4 – main.py 통합 및 커버리지

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Green | `requirements.txt` | pytest, pytest-cov 의존성 추가 |
| Green | `main.py` | PRD Section 6 메뉴 흐름 연결 (MainView → 각 Controller) |
| 검증 | — | `pytest tests/ -v --cov=app --cov-report=term-missing` 실행 |

---

## 커밋 전략

| prefix | 시점 |
|--------|------|
| `test:` | Red 단계 완료 시 |
| `feat:` | Green 단계 완료 시 |
| `refactor:` | Refactor 단계 완료 시 |

---

## 완료 기준

- [ ] 모든 테스트 통과 (`pytest`)
- [ ] 커버리지 80% 이상 (`pytest --cov`)
- [ ] 패키지 구조 PRD Section 2와 일치
- [ ] `display()` 가 `print()` 대신 문자열 반환
- [ ] Controller 단방향 의존성 유지 (View → Controller → Model)
