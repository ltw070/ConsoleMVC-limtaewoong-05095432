"""main.py - Entry point for S-Semi console application.

Wires up controllers and views, then runs the main menu loop.
"""
from app.controller.sample_controller import SampleController
from app.controller.production_controller import ProductionController
from app.controller.order_controller import OrderController
from app.view.main_view import MainView
from app.view.sample_view import SampleView
from app.view.order_view import OrderView
from app.view.monitor_view import MonitorView
from app.view.production_view import ProductionView
from app.view.shipment_view import ShipmentView


def _get_system_status(order_ctrl: OrderController, prod_ctrl: ProductionController) -> dict:
    """Collect a summary dict for the main view dashboard."""
    from app.model.enums import OrderStatus

    all_orders = list(order_ctrl._orders.values())
    return {
        "전체 주문": len(all_orders),
        "접수(RESERVED)": sum(1 for o in all_orders if o.status == OrderStatus.RESERVED),
        "생산중(PRODUCING)": sum(1 for o in all_orders if o.status == OrderStatus.PRODUCING),
        "출고대기(CONFIRMED)": sum(1 for o in all_orders if o.status == OrderStatus.CONFIRMED),
        "출고완료(RELEASE)": sum(1 for o in all_orders if o.status == OrderStatus.RELEASE),
        "생산대기 수": len(prod_ctrl.get_queue()),
    }


def run_sample_menu(sample_ctrl: SampleController, view: SampleView) -> None:
    """[1] 시료 관리 submenu."""
    while True:
        print("\n  [시료 관리]")
        print("  [1] 시료 등록")
        print("  [2] 시료 목록")
        print("  [3] 시료 검색")
        print("  [0] 돌아가기")
        choice = view.get_input("  선택 > ").strip()

        if choice == "1":
            sid = view.get_input("  시료 ID (예: S-001) > ").strip()
            name = view.get_input("  시료 이름 > ").strip()
            try:
                avg_time = float(view.get_input("  평균 생산시간 (min/ea) > ").strip())
                yr = float(view.get_input("  수율 (0 < v <= 1) > ").strip())
                s = sample_ctrl.register_sample(id=sid, name=name, avg_time=avg_time, yield_rate=yr)
                print(view.display(s))
            except ValueError as e:
                print(f"  오류: {e}")

        elif choice == "2":
            print(view.display(sample_ctrl.list_samples()))

        elif choice == "3":
            kw = view.get_input("  검색어 > ").strip()
            print(view.display(sample_ctrl.search_samples(kw)))

        elif choice == "0":
            break
        else:
            print("  잘못된 선택입니다.")


def run_order_placement(order_ctrl: OrderController, view: OrderView) -> None:
    """[2] 주문 접수 submenu."""
    sid = view.get_input("  시료 ID > ").strip()
    customer = view.get_input("  고객명 > ").strip()
    try:
        qty = int(view.get_input("  주문 수량 > ").strip())
        order = order_ctrl.place_order(sample_id=sid, customer=customer, qty=qty)
        print(view.display(order))
    except ValueError as e:
        print(f"  오류: {e}")


def run_order_approval(order_ctrl: OrderController, view: OrderView) -> None:
    """[3] 주문 승인/거절 submenu."""
    reserved = order_ctrl.list_reserved()
    print(view.display(reserved))
    if not reserved:
        return
    order_no = view.get_input("  주문번호 > ").strip()
    print("  [1] 승인  [2] 거절")
    action = view.get_input("  선택 > ").strip()
    try:
        if action == "1":
            result = order_ctrl.approve_order(order_no)
        elif action == "2":
            result = order_ctrl.reject_order(order_no)
        else:
            print("  잘못된 선택입니다.")
            return
        print(view.display(result))
    except ValueError as e:
        print(f"  오류: {e}")


def run_production_menu(
    prod_ctrl: ProductionController,
    order_ctrl: OrderController,
    view: ProductionView,
    order_view: OrderView,
) -> None:
    """[5] 생산 라인 submenu."""
    while True:
        print("\n  [생산 라인]")
        print("  [1] 생산 대기 큐 보기")
        print("  [2] 현재 생산 항목")
        print("  [3] 생산 완료 처리")
        print("  [0] 돌아가기")
        choice = view.get_input("  선택 > ").strip()

        if choice == "1":
            print(view.display(prod_ctrl.get_queue()))

        elif choice == "2":
            current = prod_ctrl.get_current()
            print(view.display(current))

        elif choice == "3":
            current = prod_ctrl.get_current()
            if current is None:
                print("  생산 중인 항목이 없습니다.")
                continue
            print(view.display(current))
            confirm = view.get_input("  생산 완료 처리하시겠습니까? (y/n) > ").strip().lower()
            if confirm == "y":
                try:
                    prod_ctrl.complete_production(current.order_no)
                    # Transition the order status PRODUCING → CONFIRMED
                    order = order_ctrl._orders.get(current.order_no)
                    if order:
                        from app.model.enums import OrderStatus
                        object.__setattr__(order, "status", OrderStatus.CONFIRMED)
                        print(order_view.display(order))
                    print("  생산 완료 처리되었습니다.")
                except ValueError as e:
                    print(f"  오류: {e}")

        elif choice == "0":
            break
        else:
            print("  잘못된 선택입니다.")


def run_shipment_menu(
    order_ctrl: OrderController,
    view: ShipmentView,
    order_view: OrderView,
) -> None:
    """[6] 출고 처리 submenu."""
    all_orders = list(order_ctrl._orders.values())
    print(view.display(all_orders))
    order_no = order_view.get_input("  출고할 주문번호 > ").strip()
    try:
        result = order_ctrl.ship_order(order_no)
        print(view.display(result))
    except ValueError as e:
        print(f"  오류: {e}")


def main() -> None:
    """Main application entry point."""
    # Wire up controllers (dependency injection)
    sample_ctrl = SampleController()
    prod_ctrl = ProductionController()
    order_ctrl = OrderController(sample_ctrl=sample_ctrl, prod_ctrl=prod_ctrl)

    # Wire up views
    main_view = MainView()
    sample_view = SampleView()
    order_view = OrderView()
    monitor_view = MonitorView()
    prod_view = ProductionView()
    ship_view = ShipmentView()

    while True:
        status = _get_system_status(order_ctrl, prod_ctrl)
        print(main_view.display(status))

        choice = main_view.get_input("선택 > ").strip()

        if choice == "1":
            run_sample_menu(sample_ctrl, sample_view)
        elif choice == "2":
            run_order_placement(order_ctrl, order_view)
        elif choice == "3":
            run_order_approval(order_ctrl, order_view)
        elif choice == "4":
            all_orders = list(order_ctrl._orders.values())
            print(monitor_view.display(all_orders))
        elif choice == "5":
            run_production_menu(prod_ctrl, order_ctrl, prod_view, order_view)
        elif choice == "6":
            run_shipment_menu(order_ctrl, ship_view, order_view)
        elif choice == "0":
            print("  시스템을 종료합니다.")
            break
        else:
            print("  잘못된 선택입니다.")


if __name__ == "__main__":
    main()
