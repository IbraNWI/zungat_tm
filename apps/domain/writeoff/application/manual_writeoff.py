# apps/writeoff/application/manual_writeoff.py

from dataclasses import dataclass


@dataclass
class ManualWriteoffService:
    bx_client: any
    tm_client: any
    lock_manager: any
    payment_repo: any

    def execute(self, fact_payment_id: int):
        # 1. Idempotency check
        if self.payment_repo.is_processed(fact_payment_id):
            return {"status": "already_processed"}

        # 2. Lock (защита от дублей)
        with self.lock_manager.lock(f"payment:{fact_payment_id}"):

            payment = self.payment_repo.get(fact_payment_id)

            # повторная проверка внутри lock
            if payment.status == "processed":
                return {"status": "already_processed"}

            # 3. Выполняем списание в TM
            result = self.tm_client.writeoff.execute(
                driver_id=payment.driver_id,
                amount=payment.amount,
            )

            # 4. Сохраняем результат в Bitrix
            self.bx_client.fact_payment.update(
                fact_payment_id=fact_payment_id,
                paid_amount=result["paid_amount"],
                arrest_amount=result["arrest_amount"],
                status="processed",
            )

            # 5. Обновляем локальное состояние (если есть)
            self.payment_repo.mark_processed(
                fact_payment_id,
                result=result,
            )

            return {
                "status": "success",
                "result": result,
            }